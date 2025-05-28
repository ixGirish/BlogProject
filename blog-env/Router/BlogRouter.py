from Security.auth import verify_token
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from Connection.connection import get_db
from Models.BlogModel import CreateBlog, User
from Schemas.baseSchema import BlogResponse, setBlog, BlogUpdate

router = APIRouter(prefix="/blog", tags=["Blogs"])

@router.post('/send')
def create_blog(request: setBlog, db: Session = Depends(get_db), current_user: User = Depends(verify_token)):
    new_blog = CreateBlog(title=request.title, content=request.content,userId=current_user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/{id}', response_model=BlogResponse, status_code=status.HTTP_200_OK)
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(CreateBlog).filter(CreateBlog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The id: {id} is not present')
    return blog

@router.get('/', status_code=status.HTTP_200_OK)
def get_all_posts(db: Session = Depends(get_db)):
    blogs = db.query(CreateBlog).all()
    return blogs

@router.patch('/update/{id}')
def update_blog(id: int, request: BlogUpdate, db: Session = Depends(get_db)):
    blog = db.query(CreateBlog).filter(CreateBlog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The id: {id} not found')
    updated_data = request.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(blog, key, value)

    db.commit()
    return {"message": "Blog updated successfully", "updated_fields": updated_data}

@router.delete('/delete/{id}')
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(CreateBlog).filter(CreateBlog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The id: {id} not found')
    val = blog.title
    db.delete(blog)
    db.commit()
    return {"message": f"The blog with title '{val}' is deleted"}
