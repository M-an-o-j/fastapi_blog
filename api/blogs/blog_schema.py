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
    title:str = None
    summary:str = None
    paragraph:str = None
    author_id:int = None

class updateblogresponse(BaseModel):
    title:str = None
    summary:str = None
    paragraph:str = None