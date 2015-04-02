json = {
    "definitions": {
        "sponsor": {
            "required": [
                "sponsorName"
            ],
            "type": "object",
            "properties": {
                "sponsorName": {
                    "type": "string"
                },
                "sponsorIdentifier": {
                    "type": "string",
                    "format": "uri"
                }
            }
        },
        "person": {
            "required": [
                "name"
            ],
            "type": "object",
            "properties": {
                "affiliation": {
                    "type": "string"
                },
                "givenName": {
                    "type": "string"
                },
                "additionalName": {
                    "type": "string"
                },
                "name": {
                    "type": "string"
                },
                "sameAs": {
                    "items": {
                        "type": "string",
                        "format": "uri"
                    },
                    "type": "array"
                },
                "familyName": {
                    "type": "string"
                },
                "email": {
                    "type": "string",
                    "format": "email"
                }
            }
        },
        "institution": {
            "required": [
                "name"
            ],
            "type": "object",
            "properties": {
                "sameAs": {
                    "items": {
                        "type": "string",
                        "format": "uri"
                    },
                    "type": "array"
                },
                "name": {
                    "type": "string"
                },
                "email": {
                    "type": "string",
                    "format": "uri"
                }
            }
        },
        "award": {
            "required": [
                "awardName"
            ],
            "type": "object",
            "properties": {
                "awardIdentifier": {
                    "type": "string",
                    "format": "uri"
                },
                "awardName": {
                    "type": "string"
                }
            }
        },
        "sponsorship": {
            "required": [
                "sponsor"
            ],
            "type": "object",
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
        "creator",
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
            "type": "string"
        },
        "creator": {
            "items": {
                "anyOf": [
                    {
                        "$ref": "#/definitions/person"
                    },
                    {
                        "$ref": "#/definitions/institution"
                    }
                ]
            },
            "type": "array"
        },
        "directLink": {
            "type": "string",
            "format": "uri"
        },
        "licenseRef": {
            "items": {
                "required": [
                    "uri"
                ],
                "type": "object",
                "properties": {
                    "startDate": {
                        "type": "string",
                        "format": "date"
                    },
                    "endDate": {
                        "type": "string",
                        "format": "date"
                    },
                    "uri": {
                        "type": "string",
                        "format": "uri"
                    }
                }
            },
            "type": "array"
        },
        "releaseDate": {
            "type": "string",
            "format": "date"
        },
        "raw": {
            "type": "string",
            "format": "uri"
        },
        "versionOfRecord": {
            "type": "string",
            "format": "uri"
        },
        "relation": {
            "items": {
                "type": "string",
                "format": "uri"
            },
            "type": "array"
        },
        "freeToRead": {
            "type": "object",
            "properties": {
                "startDate": {
                    "type": "string",
                    "format": "date"
                },
                "endDate": {
                    "type": "string",
                    "format": "date"
                }
            }
        },
        "sponsorship": {
            "items": {
                "$ref": "#/definitions/sponsorship"
            },
            "type": "array"
        },
        "revisionTime": {
            "type": "string",
            "format": "date-time"
        },
        "publisher": {
            "type": "string"
        },
        "creationDate": {
            "type": "string",
            "format": "date"
        },
        "language": {
            "type": "string"
        },
        "title": {
            "type": "string"
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
            "format": "uri"
        },
        "notificationLink": {
            "type": "string",
            "format": "uri"
        },
        "source": {
            "type": "string"
        },
        "journalArticleVersion": {
            "enum": [
                "AO",
                "SMUR",
                "AM",
                "P",
                "VoR",
                "CVoR",
                "EVoR",
                "NA"
            ]
        }
    }
}
