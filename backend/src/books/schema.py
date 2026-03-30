from pydantic import BaseModel, field_validator


class BookCreate(BaseModel):
    title: str
    publisher_id: int
    author_ids: list[int]
    prefix: str
    copies: int = 1

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("書名不可為空")
        return v

    @field_validator("prefix")
    @classmethod
    def validate_prefix(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("前綴不可為空")
        if len(v) > 20:
            raise ValueError("前綴不可超過 20 個字元")
        return v

    @field_validator("copies")
    @classmethod
    def validate_copies(cls, v: int) -> int:
        if v < 1:
            raise ValueError("冊數至少為 1")
        if v > 100:
            raise ValueError("單次新增冊數不可超過 100")
        return v


class BookUpdate(BaseModel):
    title: str
    publisher_id: int
    author_ids: list[int]
    prefix: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("書名不可為空")
        return v

    @field_validator("prefix")
    @classmethod
    def validate_prefix(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("前綴不可為空")
        return v


class Book(BaseModel):
    id: int
    title: str
    prefix: str


class BookListResponse(BaseModel):
    data: list[Book]
