from typing import Optional
from pydantic import BaseModel, ConfigDict

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

class userOut(BaseModel):
    id:int
    model_config = ConfigDict(from_attributes=True)

class BlogOut(BaseModel):
    id: int
    title: str
    content: str
    user:userOut  # include this if you want to expose userId

    model_config = ConfigDict(from_attributes=True)

class PageInfo(BaseModel):
    pageNo: int
    totalPages: int
    total: int
    skip: Optional[int] = None
    limit: Optional[int] = None