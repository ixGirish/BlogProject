from typing import Optional
from pydantic import BaseModel

class setBlog(BaseModel):
    title:str
    content:str

class BlogResponse(setBlog):  
    class Config():
        orm_mode:True

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    class Config():
        orm_mode:True