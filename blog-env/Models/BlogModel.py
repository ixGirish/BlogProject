from datetime import date
from sqlalchemy import Column, Integer, String ,ForeignKey,Date,LargeBinary
from Connection.connection import Base
from sqlalchemy.orm import relationship

class CreateBlog(Base):
    __tablename__ = 'GD_BLOG'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    content=Column(String(1000))
    userId=Column(Integer, ForeignKey('Gd_BLOG_USER.id'))
    Creator=relationship("User",back_populates="blogs")

class User(Base):
    __tablename__= 'Gd_BLOG_USER'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255)) 
    
    blogs=relationship("CreateBlog", back_populates="Creator")
    fileUser=relationship("FileHandling" , back_populates="files")

class FileHandling(Base):
    __tablename__= 'GD_FILE_HANDLE'
    id = Column(Integer, primary_key=True, index=True)
    name=Column(String(255))
    type=Column(String(255))
    createdAt=Column(Date,default=date.today)
    creatorId=Column(Integer,ForeignKey("Gd_BLOG_USER.id"))
    content=Column(LargeBinary,nullable=False)

    files=relationship("User",back_populates="fileUser")