from pydantic import BaseModel, field_validator


class PublisherCreate(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("名稱不可為空白")
        if len(v) > 255:
            raise ValueError("名稱不可超過 255 個字元")
        return v


class PublisherUpdate(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("名稱不可為空白")
        if len(v) > 255:
            raise ValueError("名稱不可超過 255 個字元")
        return v


class Publisher(BaseModel):
    id: int
    name: str


class PublisherListResponse(BaseModel):
    data: list[Publisher]
