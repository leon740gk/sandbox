from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BlogSchema(BaseModel):
    title: str
    body: str

    def to_dict(self):
        return dict(self)
