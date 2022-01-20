from config import Language
from presenters.experiment import Experiment


def handler_get_exp(
        lang: Language = Language.en,
        idx: int = None):
    return {
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
           }
