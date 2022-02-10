from typing import List, Optional

from fastapi import APIRouter, HTTPException

from config import Language, Order, SortVariant
from handlers.experiments import search, get, plot
from presenters.experiment import Experiment
from entities.intervention_type import InterventionType

router = APIRouter()
base_route = 'experiment'


@router.get(f'/{base_route}/search')
async def get_experiments_list(
        lang: Language = Language.en,
        page: int = None, pageSize: int = None,
        # filters
        byInterventionType: InterventionType = None,
        byIntervention: int = None,
        byStrain: int = None,
        byMaxLifespanChangePercentMin: float = None,
        byMaxLifespanChangePercentMax: float = None,
        byAvgLifespanChangePercentMin: float = None,
        byAvgLifespanChangePercentMax: float = None,
        byAvgLifespanMin: int = None,
        byAvgLifespanMax: int = None,
        byAvgLifespanUnit: str = 'days',
        byMaxLifespanMin: int = None,
        byMaxLifespanMax: int = None,
        byMaxLifespanUnit: int = 'days',
        byYear: int = None,
        # sort
        sortBy: SortVariant = SortVariant.default,
        sortOrder: Order = Order.desc,

):
    ls = search.handler_get_exp_list(locals())
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
