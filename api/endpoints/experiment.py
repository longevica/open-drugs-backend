from typing import List

from fastapi import APIRouter, HTTPException

from config import Language
from handlers.experimets import search, get
from presenters.experiment import Experiment

router = APIRouter()
base_route = 'experiment'

@router.get(f'/{base_route}/search')
async def get_experiments_list(
        lang: Language = Language.en,
        page: int = None, pageSize: int = None):
    ls = search.handler_get_exp_list(lang, page, pageSize)
    return ls

@router.get(f'/{base_route}/{{idx}}')
async def get_experiment(
        lang: Language = Language.en,
        idx: int = None):
    if idx is None:
        raise HTTPException( status_code=404, detail='missing idx arg',)
    exp = get.handler_get_exp(lang, idx)
    exp["id"] = idx
    return exp

