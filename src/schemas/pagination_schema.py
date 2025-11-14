from pydantic import BaseModel
from typing import List, TypeVar, Generic

DataType = TypeVar('DataType')

class PaginatedResponse(BaseModel, Generic[DataType]):
    total_count: int
    data: List[DataType]
