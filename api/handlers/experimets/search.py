from config import Language
from presenters.experiment import Experiment


def handler_get_exp_list(
        lang: Language = Language.en,
        page: int = None, pageSize: int = None):
    return {
        "items": [
            {
                "id": 123,
                "species": {
                    "id": 123,
                    "name": "mus musculus"
                },
                "strain": {
                    "id": 123,
                    "name": "UM-HET3"
                },
                "sex": "male",
                "interventionType": {
                    "id": 2,
                    "name": "drug"
                },
                "lifespan": {
                    "med": 781,
                    "avg": None,
                    "max": 985,
                    "unit": "days"
                },
                "doi": "10.1111/j.1474-9726.2007.00311.x",
                "pmid": 27882602,
                "year": 2015,
                "cohortSize": None,
                "survivalDataAvailable": True,
                "rawDataAvailable": True,
                "intervention": {
                    "drugIntervention": {
                        "drug": {
                            "id": 12,
                            "name": "Rapamycin"
                        },
                        "dosage": "10uM",
                        "delivery": {
                            "option": "medium",
                            "mean": "0,3% DMSO",
                            "regime": "repeated/continuous"
                        },
                        "exposure": {
                            "startLifespanPercent": 0,
                            "endLifespanPercent": 100,
                            "startingPoint": "L4 stage"
                        }
                    },
                    "dietIntervention": None
                },
                "conditions": {
                    "feed": "Purina 5LG6",
                    "temperature": {
                        "from": 21,
                        "to": 24
                    },
                    "light": {
                        "light": 16,
                        "dark": 8
                    },
                    "density": {
                        "count": 25,
                        "container": "cage"
                    }
                }
            },
            {
                "id": 123,
                "species": {
                    "id": 123,
                    "name": "mus musculus"
                },
                "strain": {
                    "id": 123,
                    "name": "UM-HET3"
                },
                "sex": "female",
                "interventionType": {
                    "id": 1,
                    "name": "control"
                },
                "lifespan": {
                    "med": 781,
                    "avg": None,
                    "max": 985,
                    "unit": "days"
                },
                "doi": "10.1111/j.1474-9726.2007.00311.x",
                "pmid": 27882602,
                "year": 2015,
                "cohortSize": 25,
                "survivalDataAvailable": True,
                "rawDataAvailable": False,
                "intervention": {
                    "drugIntervention": None,
                    "dietIntervention": None
                },
                "conditions": {
                    "feed": "Purina 5LG6",
                    "temperature": {
                        "from": 21,
                        "to": 24
                    },
                    "light": None,
                    "density": {
                        "count": 25,
                        "container": "cage"
                    }
                }
            }
        ],
        "filters": {
            "interventionType": [
                {
                    "id": 1,
                    "name": "control"
                },
                {
                    "id": 2,
                    "name": "drug"
                },
                {
                    "id": 3,
                    "name": "diet"
                }
            ],
            "intervention": [
                {
                    "id": 1,
                    "name": "Control",
                    "type": "control"
                },
                {
                    "id": 123,
                    "name": "Metformin",
                    "type": "drug"
                },
                {
                    "id": 234,
                    "name": "Glycine",
                    "type": "drug"
                },
                {
                    "id": 345,
                    "name": "Low FODMAP",
                    "type": "diet"
                }
            ],
            "species": [
                {
                    "id": 123,
                    "name": "mus musculus"
                },
                {
                    "id": 234,
                    "name": "c. elegans"
                }
            ],
            "strain": [
                {
                    "id": 123,
                    "name": "UM-HET3"
                },
                {
                    "id": 234,
                    "name": "N2"
                }
            ],
            "avgLifespanChangePercent": {
                "min": -20.3,
                "max": 35.12
            },
            "maxLifespanChangePercent": {
                "min": -22.9,
                "max": 40.56
            },
            "avgLifespan": {
                "min": 15,
                "max": 18,
                "unit": "days"
            },
            "maxLifespan": {
                "min": 23,
                "max": 28,
                "unit": "days"
            },
            "year": [
                1998,
                2001,
                2002,
                2003
            ]
        },
        "options": {
            "objTotal": 2,
            "pagination": {
                "page": 1,
                "pageSize": 15,
                "pagesTotal": 1
            }
        }
    }
