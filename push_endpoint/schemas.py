share = {
    "definitions": {
        "person": {
            "required": [
                "name"
            ],
            "type": "object",
            "description": "A person that is a contributor to the research object.",
            "properties": {
                "affiliation": {
                    "items": [
                        {
                            "$ref": "#/definitions/organization"
                        }
                    ],
                    "type": "array",
                    "description": "The organization(s) that this person is affiliated with. For example, a school/university."
                },
                "givenName": {
                    "type": "string",
                    "description": "Also called the \"first name\",this element is preferred over using the combined \"name\" field."
                },
                "additionalName": {
                    "type": "string",
                    "description": "Also called the \"middle name\",this element will be derived from the creator.name by SHARE if not supplied by the source."
                },
                "name": {
                    "type": "string",
                    "description": "The name of the person if familyName, givenName, and/or additionalName."
                },
                "sameAs": {
                    "items": {
                        "type": "string",
                        "description": "An HTTP URI that describes the person.",
                        "format": "uri"
                    },
                    "type": "array",
                    "description": "An array of identifiers expressed as HTTP URIs that describe the person. For example, an ORCID, ResearcherID, arXiv author ID, ScopusID,  ISNI, or other unique identifier expressed as an HTTP URI."
                },
                "familyName": {
                    "type": "string",
                    "description": "Also called the \"last name\",this element is preferred over using the combined \"name\" field."
                },
                "email": {
                    "type": "string",
                    "description": "The email address for this person.",
                    "format": "email"
                }
            }
        },
        "organization": {
            "required": [
                "name"
            ],
            "type": "object",
            "description": "An organization or institution.",
            "properties": {
                "sameAs": {
                    "items": {
                        "type": "string",
                        "description": "A single HTTP URI that describes this organization",
                        "format": "uri"
                    },
                    "type": "array",
                    "description": "Identifiers that describe this organization"
                },
                "name": {
                    "type": "string",
                    "description": "The name of the organization."
                },
                "email": {
                    "type": "string",
                    "description": "An email address for this organization",
                    "format": "uri"
                }
            }
        },
        "sponsor": {
            "required": [
                "sponsorName"
            ],
            "type": "object",
            "description": "This describes the sponsor of the resource.",
            "properties": {
                "sponsorName": {
                    "type": "string",
                    "description": "The name of the entity responsible for sponsoring the resource, recorded here as text."
                },
                "sponsorIdentifier": {
                    "type": "string",
                    "description": "A globally unique identifier for the sponsor of the resource should be recorded here.",
                    "format": "uri"
                }
            }
        },
        "award": {
            "required": [
                "awardName"
            ],
            "type": "object",
            "description": "The award made to support the creation of the resource.",
            "properties": {
                "awardIdentifier": {
                    "type": "string",
                    "description": "An HTTP URI for the award, issued by the sponsor, that relates to the resource.",
                    "format": "uri"
                },
                "awardName": {
                    "type": "string",
                    "description": "The textual representation of the award identifier, issued by the sponsor, that relates to the resource."
                }
            }
        },
        "sponsorship": {
            "required": [
                "sponsor"
            ],
            "type": "object",
            "description": "A sponsorship associated with the resource.",
            "properties": {
                "sponsor": {
                    "$ref": "#/definitions/sponsor"
                },
                "award": {
                    "$ref": "#/definitions/award"
                }
            }
        }
    },
    "$schema": "http://json-schema.org/draft-04/schema#",
    "required": [
        "contributor",
        "directLink",
        "releaseDate",
        "notificationLink",
        "raw",
        "resourceIdentifier",
        "source",
        "title"
    ],
    "type": "object",
    "properties": {
        "description": {
            "type": "string",
            "description": "A textual description of the resource."
        },
        "directLink": {
            "type": "string",
            "description": "A persistent HTTP URI that points to the research object.",
            "format": "uri"
        },
        "releaseDate": {
            "type": "string",
            "description": "The date of public release when the research object is freely available.",
            "format": "date"
        },
        "raw": {
            "type": "string",
            "description": "The URL of the raw record either harvested or pushed to SHARE by the source. These raw records are provided exactly as it was delivered to SHARE, which means they are widely varying in format and content.",
            "format": "uri"
        },
        "versionOfRecord": {
            "type": "string",
            "description": "This field MUST contain an HTTP URI which is a persistent identifier for the published version of the resource. If a DOI has been issued by the publisher then this MUST be used. Such a DOI MUST be represented as an HTTP URI. ",
            "format": "uri"
        },
        "relation": {
            "items": {
                "type": "string",
                "description": "An HTTP URI which points to a related resource.",
                "format": "uri"
            },
            "type": "array",
            "description": "Related resources"
        },
        "freeToRead": {
            "required": [
                "startDate"
            ],
            "type": "object",
            "description": "A date range specifying when this research object will be free to read.",
            "eroperties": {
                "startDate": {
                    "type": "string",
                    "description": "The start date of the free to read period. If the resource was always free to read, then this date can be the same as creationDate or the date \"0000-00-00\"",
                    "format": "date"
                },
                "endDate": {
                    "type": "string",
                    "description": "The date on which this resource will no longer be free to read",
                    "format": "date"
                }
            }
        },
        "contributor": {
            "items": {
                "anyOf": [
                    {
                        "$ref": "#/definitions/person"
                    },
                    {
                        "$ref": "#/definitions/organization"
                    }
                ]
            },
            "type": "array",
            "description": "The people or organizations responsible for making contributions to an object."
        },
        "sponsorship": {
            "items": {
                "$ref": "#/definitions/sponsorship"
            },
            "type": "array",
            "description": "Sponsorships associated with the array"
        },
        "revisionTime": {
            "type": "string",
            "description": "The time this record was last revised by the provider",
            "format": "date-time"
        },
        "publisher": {
            "type": "string",
            "description": "This element contains the name of the entity, typically a 'publisher', responsible for making the version of record of the resource available. This could be a person, organisation or service"
        },
        "creationDate": {
            "type": "string",
            "description": "Creation date of the research object.",
            "format": "date"
        },
        "language": {
            "type": "string"
        },
        "license": {
            "items": {
                "required": [
                    "uri",
                    "startDate"
                ],
                "type": "object",
                "properties": {
                    "startDate": {
                        "type": "string",
                        "description": "The start date of the license period. If the resource was always licensed this way, then this date can be the same as creationDate or the date \"0000-00-00\"",
                        "format": "date"
                    },
                    "endDate": {
                        "type": "string",
                        "description": "The date on which this resource will no longer be licensed in this way,",
                        "format": "date"
                    },
                    "uri": {
                        "type": "string",
                        "description": "The HTTP URI of the license in effect during the period describe by this lincenseRef",
                        "format": "uri"
                    }
                }
            },
            "type": "array",
            "description": "The licenses under which the object has been released."
        },
        "title": {
            "type": "string",
            "description": "The title and any sub-titles of the resource."
        },
        "shareProperties": {
            "type": "object",
            "properties": {
                "collectionDateTime": {
                    "type": "string",
                    "format": "date-time"
                }
            }
        },
        "otherProperties": {
            "type": "object"
        },
        "resourceIdentifier": {
            "type": "string",
            "description": "An HTTP URI which unambiguously and persistently indicates the resource's identifier at a specific location.",
            "format": "uri"
        },
        "notificationLink": {
            "type": "string",
            "description": "The persistent HTTP URI at which the individual record of this research release event can be retrieved in the future. (Same as @id.)",
            "format": "uri"
        },
        "version": {
            "enum": [
                "AO",
                "SMUR",
                "AM",
                "P",
                "VoR",
                "CVoR",
                "EVoR",
                "NA"
            ],
            "type": "string",
            "description": "This element indicates which 'version' of the resource is being described. While intended primarily for journal articles, it might be applicable to other types of resources as well."
        }
    }
}
