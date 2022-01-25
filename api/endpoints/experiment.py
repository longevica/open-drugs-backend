from typing import List, Optional

from fastapi import APIRouter, HTTPException

from config import Language
from handlers.experiments import search, get, plot
from presenters.experiment import Experiment
from entities.intervention_type import InterventionType

router = APIRouter()
base_route = 'experiment'


@router.get(f'/{base_route}/search')
async def get_experiments_list(
        lang: Language = Language.en,
        page: int = None, pageSize: int = None,
        ##
        interventionType: InterventionType = None,
        intervention: int = None,
        species: int = None,
        strain: int = None,
        maxLifespanChangePercentMin: float = None,
        maxLifespanChangePercentMax: float = None,
        avgLifespanChangePercentMin: float = None,
        avgLifespanChangePercentMax: float = None,
        avgLifespanMin: int = None,
        avgLifespanMax: int = None,
        avgLifespanUnit: str = 'days',
        maxLifespanMin: int = None,
        maxLifespanMax: int = None,
        maxLifespanUnit: int = 'days',
        year: int = None
        ##

):
    ls = search.handler_get_exp_list(lang, page, pageSize)
    return ls


# @router.get(f'/{base_route}/{{idx}}')
# async def get_experiment(
#         lang: Language = Language.en,
#         idx: int = None):
#     if idx is None:
#         raise HTTPException( status_code=404, detail='missing idx arg',)
#     exp = get.handler_get_exp(lang, idx)
#     exp["id"] = idx
#     return exp

@router.get(f'/{base_route}/plot')
async def get_experiment_plot(
        lang: Language = Language.en,
        ids: str = None):
    if ids is None:
        raise HTTPException(status_code=404, detail='missing ids arg', )
    ls = []
    for i in ids.split(','):
        try:
            t = i.strip()
            if t != '':
                ls.append(int(t))
        except:
            raise HTTPException(status_code=404, detail='wrong type parameter ids', )

    pl = plot.handler_plot_exp(lang, ls)
    return pl
