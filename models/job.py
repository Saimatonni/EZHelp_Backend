from typing import List, Optional
from pydantic import BaseModel


class Coordinates(BaseModel):
    latitude: float
    longitude: float


class Job(BaseModel):
    userId: str = None
    workType: str
    address: str
    GPSCoordinates: Coordinates
    emergency: bool
    payAmount: float
    shortTitle: str
    description: str
    images: List[str]
    startDate: str
    endDate: str
    bidded_sp_ids: List[int]=[]
