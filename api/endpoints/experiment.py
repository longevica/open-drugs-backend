from typing import List

from fastapi import APIRouter, HTTPException

from config import Language
from presenters.experiment import Experiment

router = APIRouter()


@router.get('/search')
async def get_experiments_list(lang: Language = Language.en):
    raise HTTPException(status_code=404, detail='Not implemented', )
    return DiseaseDAO().get()

