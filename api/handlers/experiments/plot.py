from config import Language
from presenters.experiment import Experiment


def handler_plot_exp(lang: Language = Language.en, ids: [] = None):
    items = []
    for i in ids:
        items.append(
            {
                "id": i,
                "title": "Rapamycin 2005 clinical trials",
                "coordinates": {
                    "x": [
                        1 + i,
                        2 + i,
                        3 + i,
                        4 + i
                    ],
                    "y": [
                        10 + i,
                        15 + i,
                        13 + i,
                        17 + i
                    ],
                    "mode": "lines+markers"
                }
            }

        )

    return {
        "items": items,
        "options": {
            "objTotal": len(ids),
        }
    }
