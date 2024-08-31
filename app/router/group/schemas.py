from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.utils.enum import Strategy


class GroupBaseDTO(BaseModel):
    name: str
    strategy: Strategy
    value_strategy: Optional[int]


class GroupDTO(GroupBaseDTO):
    model_config = ConfigDict(from_attributes=True)
    id: int


class GroupCreateDTO(GroupBaseDTO):
    pass


class GroupUpdateDTO(GroupCreateDTO):
    pass


class GroupUpdatePartialDTO(GroupCreateDTO):
    pass
