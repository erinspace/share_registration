import requests
from lxml import etree

from datetime import date, timedelta


NAMESPACES = {'dc': 'http://purl.org/dc/elements/1.1/',
              'oai_dc': 'http://www.openarchives.org/OAI/2.0/',
              'ns0': 'http://www.openarchives.org/OAI/2.0/'}
BASE_SCHEMA = ['title', 'contributor', 'creator', 'subject', 'description']


def get_oai_properties(base_url):
    """ Makes 2 requests to the provided base URL:
        1 for the sets available
        1 for the list of properties

        returns a dict with list of properties, and sets
        The sets available are added as multiple selections for the next form,
        the properties are pre-loaded into the properties field.
    """

    # request 1 for the setSpecs available
    set_url = base_url + '?verb=ListSets'
    set_data_request = requests.get(set_url)
    all_content = etree.XML(set_data_request.content)
    set_names = all_content.xpath('//oai_dc:setSpec/node()', namespaces=NAMESPACES)
    set_names = [name.replace('publication:', '') for name in set_names]

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
    pre_names = all_prop_content.xpath('//ns0:metadata', namespaces=NAMESPACES)[0].getchildren()[0].getchildren()
    all_names = [name.tag.replace('{' + NAMESPACES['dc'] + '}', '') for name in pre_names]
    property_names = list({name for name in all_names if name not in BASE_SCHEMA})

    return {'properties': property_names, 'sets': set_groups}
