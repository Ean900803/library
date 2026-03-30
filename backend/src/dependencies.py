from typing import Annotated
from fastapi import Depends
from src.core.database import get_cursor
import aiomysql

CursorDep = Annotated[aiomysql.DictCursor, Depends(get_cursor)]