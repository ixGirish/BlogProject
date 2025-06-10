from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from Security.auth import verify_token
from fastapi import APIRouter, Depends,UploadFile,File,HTTPException,status
from fastapi.responses import StreamingResponse
from sqlalchemy import text
from sqlalchemy.orm import Session
from Connection.connection import get_db,SessionLocal
from Models.BlogModel import FileHandling, User
from datetime import date

router=APIRouter(prefix="/file", tags=["File"])

@router.post('/upload')
def fileUpload(db:Session=Depends(get_db),file:UploadFile=File(...), current_user: User= Depends(verify_token)):
    data=file.file.read()
    db_file=FileHandling(
        name=file.filename,
        type=file.content_type,
        createdAt=date.today(),
        creatorId=current_user.id,
        content=data
    )
    db.add(db_file)
    db.commit()

    db.refresh(db_file)
    return f"file added with id: {db_file.id}"


@router.get('/{id}')
def fileDownload(id:int,db:Session=Depends(get_db)):
    db_file=db.query(FileHandling).filter(FileHandling.id==id).first()
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'File not found with id:{id}')
    return StreamingResponse(
        BytesIO(db_file.content),
        media_type=db_file.type,
        headers={"Content-Disposition": f"attachment; filename={db_file.name}"}
    )

