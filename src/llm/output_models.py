from typing import List, Optional, Any

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Action(BaseModel):
    """"Information about the extracted action"""
    action: Optional[str] = Field(description="The complete text of an action")


class AllowedAction(Action):
    permit_needed: Optional[bool] = Field(description="Is a permit needed for this action")


class Actions(BaseModel):
    allowed_action_list: Optional[List[AllowedAction]]
    not_allowed_action_list: Optional[List[Action]]


output_parser= PydanticOutputParser(pydantic_object=Actions)
