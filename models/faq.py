from pydantic import BaseModel

class FAQ(BaseModel):
    id: str
    name: str
    contact: str
    question: str

class QuestionAnswer(BaseModel):
    question: str
    answer: str
    
class Testimonial(BaseModel):
    id: str
    name: str
    rate: int
    details: str