from typing import Optional

from pydantic import BaseModel


class Experiment(BaseModel):
    # id: int
    id: Optional[str] = None

