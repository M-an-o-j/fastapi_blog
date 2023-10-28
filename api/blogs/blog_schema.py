from pydantic import BaseModel
from datetime import datetime


class blogresponse(BaseModel):
    id:int
    title:str
    summary:str
    paragraph:str
    author_id:int
    created_at:datetime

class postblogresponse(BaseModel):
    title:str
    summary:str
    paragraph:str
    author_id:int