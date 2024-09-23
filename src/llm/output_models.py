from langchain_core.pydantic_v1 import BaseModel, Field


# TODO: Make real output formats
class MockOutput(BaseModel):
    mock_var: str = Field(description="The output description")
