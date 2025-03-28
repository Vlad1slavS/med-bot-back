from pydantic import BaseModel


class ConsultationOut(BaseModel):
    id: int
    specialization: str
    academic_degree: str
    type_visit: str
    price: int

    class Config:
        from_attributes = True  # Новый параметр в Pydantic v2