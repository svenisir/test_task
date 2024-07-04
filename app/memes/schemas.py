from pydantic import BaseModel, ConfigDict


class SMem(BaseModel):
    id: int
    description: str
    file_name: str

    model_config = ConfigDict(from_attributes=True)


class SPagination(BaseModel):
    page: int
    per_page: int

    model_config = ConfigDict(from_attributes=True)
