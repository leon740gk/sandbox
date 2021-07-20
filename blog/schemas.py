from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BlogCreate(BaseModel):
    title: str
    body: str
    pub_date: Optional[datetime]
