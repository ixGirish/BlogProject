from typing import Optional
from Security.auth import verify_token
from fastapi import APIRouter, Depends, Query, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy.orm import Session
from Connection.connection import get_db
from Models.BlogModel import CreateBlog, User
from Schemas.baseSchema import BlogOut, BlogResponse, setBlog, BlogUpdate

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

@router.get("/")
def get_all_posts(
    skip: Optional[int] = Query(None, ge=0),
    limit: Optional[int] = Query(None, ge=1),
    db: Session = Depends(get_db)
):
    # Apply default values if not provided
    actual_skip = skip if skip is not None else 0
    actual_limit = limit if limit is not None else 10

    total = db.query(CreateBlog).count()
    blogs = db.query(CreateBlog).order_by(CreateBlog.id).offset(actual_skip).limit(actual_limit).all()

    data = [
        BlogOut.model_validate({
            "id": blog.id,
            "title": blog.title,
            "content": blog.content,
            "user": {"id": blog.userId}
        })
        for blog in blogs
    ]

    page_info = {
        "pageNo": (actual_skip // actual_limit) + 1,
        "totalPages": (total + actual_limit - 1) // actual_limit,
        "totalElements": total
    }

    # Conditionally include skip and limit if they were passed in query
    if skip is not None:
        page_info["skip"] = skip
    if limit is not None:
        page_info["limit"] = limit

    return {   "pageInfo": page_info,
        "data": data}

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
