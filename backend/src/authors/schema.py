from pydantic import BaseModel, field_validator

class AuthorCreate(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str):
        if not v:
            raise ValueError("作者名稱不可為空")
        return v

class AuthorUpdate(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str):
        if not v:
            raise ValueError("作者名稱不可為空")
        return v

class Author(BaseModel):
    id: int
    name: str

class AuthorListResponse(BaseModel):
    data: list[Author]