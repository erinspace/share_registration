import ast
import json
import logging
from django.utils import timezone
from datetime import date, timedelta


import requests
from lxml import etree
from nameparser import HumanName
from requests_oauthlib import OAuth1

from shareregistration import settings

NAMESPACES = {'dc': 'http://purl.org/dc/elements/1.1/',
              'oai_dc': 'http://www.openarchives.org/OAI/2.0/',
              'ns0': 'http://www.openarchives.org/OAI/2.0/'}
BASE_SCHEMA = ['title', 'contributor', 'creator', 'subject', 'description']

logger = logging.getLogger(__name__)

DESK_BASE = 'https://openscience.desk.com/api/v2/'


def format_set_choices(pre_saved_data):

    sets = pre_saved_data.approved_sets
    sets = ast.literal_eval(sets)
    approved_set_set = set((item[0].replace('publication:', ''), item[1]) for item in sets)

    return approved_set_set


def get_session_item(request, item):
    return request.session[item]


def get_oai_properties(base_url):
    """ Makes 2 requests to the provided base URL:
        1 for the sets available
        1 for the list of properties

        returns a dict with list of properties, and set_groups.

        Set groups is a list of tuples - first element is short name,
        second element is the long descriptive name.

        The sets available are added as multiple selections for the next form,
        the properties are pre-loaded into the properties field.
    """
    try:
        # request 1 for the setSpecs available
        set_url = base_url.strip() + '?verb=ListSets'
        set_data_request = requests.get(set_url)
        all_content = etree.XML(set_data_request.content)

        all_sets = all_content.xpath('//oai_dc:set', namespaces=NAMESPACES)
        all_set_info = [one.getchildren() for one in all_sets]

        set_groups = []
        for item in all_set_info:
            one_group = (item[0].text, item[1].text)
            set_groups.append(one_group)

        # request 2 for records 30 days back just in case
        start_date = str(date.today() - timedelta(30))
        prop_url = base_url + '?verb=ListRecords&metadataPrefix=oai_dc&from={}T00:00:00Z'.format(start_date)
        prop_data_request = requests.get(prop_url)
        all_prop_content = etree.XML(prop_data_request.content)
        try:
            pre_names = all_prop_content.xpath('//ns0:metadata', namespaces=NAMESPACES)[0].getchildren()[0].getchildren()
        except IndexError:
            prop_url = base_url + '?verb=ListRecords&metadataPrefix=oai_dc&from={}'.format(start_date)
            prop_data_request = requests.get(prop_url)
            all_prop_content = etree.XML(prop_data_request.content)
            pre_names = all_prop_content.xpath('//ns0:metadata', namespaces=NAMESPACES)[0].getchildren()[0].getchildren()

        all_names = [name.tag.replace('{' + NAMESPACES['dc'] + '}', '') for name in pre_names]
        property_names = list({name for name in all_names if name not in BASE_SCHEMA})

        return {'properties': property_names, 'sets': set_groups}

    # If anything at all goes wrong, just render a blank form...
    except Exception as e:
        logger.info(e)
        raise ValueError('OAI Processing Error - {}'.format(e))


def get_desk_customer(email):

    # authorize the request with OAuth1 maybe
    auth = OAuth1(settings.YOUR_APP_KEY, settings.YOUR_APP_SECRET,
                  settings.USER_OAUTH_TOKEN, settings.USER_OAUTH_TOKEN_SECRET)

    customer_search_route = DESK_BASE + 'customers/search?email={}'.format(email)
    customer_search = requests.post(customer_search_route, auth=auth)

    return json.loads(customer_search)


def create_desk_customer(name, email):

    # check to see if the person exists on desk
    customer_search = get_desk_customer(email)

    # If the customer does not exist, make one
    if customer_search['total_entries'] == 0:
        parsed_name = HumanName(name)
        customer = {
            "first_name": parsed_name.first,
            "last_name": parsed_name.last,
            "emails": [
                {
                    "type": "work",
                    "value": email
                }
            ]
        }

        requests.post(DESK_BASE, json=customer, auth=settings.DESK_AUTH)


def create_desk_case(email, metadata_complete):

    if metadata_complete:
        status = 'Complete'
        subject = 'SHARE - Registration Confirmation'
        body = 'Registration complete message'
    else:
        status = 'Metadata Incomplete'
        subject = 'SHARE Registration Follow-up'
        body = 'Registration incomplete message'

    customer = get_desk_customer(email)
    customer_object = customer['_embedded']['entries'][0]['_links']['self']

    case_post = {
        "type": "email",
        "subject": "SHARE Registration {}".format(status),
        "priority": 4,
        "status": "new",
        "created_at": timezone.now(),
        "_links": {
            "customer": customer_object,
            "assigned_group": {
                "href": "/api/v2/groups/1",
                "class": "group"
            }
        },
        "message": {
            "direction": "out",
            "status": "draft",
            "to": email,
            "from": "Contact@cos.io",
            "subject": subject,
            "body": body,
            "created_at": timezone.now()
        }
    }

    requests.post(json=case_post, auth=settings.DESK_AUTH)
