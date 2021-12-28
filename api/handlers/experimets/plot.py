from config import Language
from presenters.experiment import Experiment

def handler_plot_exp(
        lang: Language = Language.en,
        idx: int = None):
    return {
        "items": [
            {
                "title": "Rapamycin 2005 clinical trials",
                "coordinates": {
                    "x": [
                        1,
                        2,
                        3,
                        4
                    ],
                    "y": [
                        10,
                        15,
                        13,
                        17
                    ],
                    "mode": "lines+markers"
                }
            },
            {
                "title": "Male mice on rapamycin with calorie restriction diet",
                "coordinates": {
                    "x": [
                        1,
                        2,
                        3,
                        4
                    ],
                    "y": [
                        12,
                        9,
                        15,
                        12
                    ],
                    "mode": "lines+markers"
                }
            }
        ],
        "options": {
            "objTotal": 2,
            "pagination": {
                "page": 1,
                "pageSize": 15,
                "pagesTotal": 1
            }
        }
    }
