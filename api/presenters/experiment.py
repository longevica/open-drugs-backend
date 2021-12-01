from pydantic import Field
from pydantic.dataclasses import dataclass
from typing import Optional

@dataclass
class Experiment:
    id: Optional[int] = Field(title="Unique ID")
