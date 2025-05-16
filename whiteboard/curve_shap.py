from pydantic import BaseModel
from typing import List, Tuple
from .point import Point

class CurveShap(BaseModel):
    type: str  # 'curve'
    points: List[Point]
    color: str