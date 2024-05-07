from pydantic import BaseModel, EmailStr

class Client(BaseModel):
    name: str = None
    email: str = None
    phone_number: str = None
    total_posts: int = None 
    image: str = None
    password: str = None
    role: str = "client"
    
    
class UpdateClient(BaseModel):
    name: str = None
    email: str = None
    phone_number: str = None
    image: str = None
    password: str = None
    
class RatingReview(BaseModel):
    provider_id: str
    client_name: str
    client_image: str
    rating: float
    review: str