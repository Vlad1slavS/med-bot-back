import logging
from typing import List

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from DB.database import SessionLocal
from Models.doctor import Doctor
from Schemas.DoctorSchema import ConsultationOut

router = APIRouter()

class TextRequest(BaseModel):
    text: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/doctors-list", response_model=List[ConsultationOut])
async def get_doctors_by_specialization(request: TextRequest, db: Session = Depends(get_db)):

    normalized_text = request.text.capitalize()

    try:
        # Ищем врачей в БД
        doctors = db.query(Doctor).filter(
            Doctor.specialization.ilike(f"%{normalized_text}%")
        ).all()

        if not doctors:
            raise HTTPException(
                status_code=404,
                detail="Врачи с такой специализацией не найдены"
            )

        return doctors

    except Exception as e:
        # Обработка ошибок БД
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка сервера: {str(e)}"
        )

