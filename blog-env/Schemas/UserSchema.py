
from pydantic import BaseModel
from .baseSchema import BlogResponse
from .fileSchema import fileresponse

class setUser(BaseModel):
  name:str
  email:str
  password:str

class getUser(BaseModel):
  name:str
  email:str
  blogs:list[BlogResponse]
  fileUser:list[fileresponse]

  class Config():
    orm_mode=True

class login(BaseModel):
  username:str
  password:str

