from pydantic import BaseModel

class ServiceProvider(BaseModel):
    name: str = None
    work_type: str = None
    pay_per_hour: float = None
    experience: int = None
    email: str = None
    phone_number: str = None
    nid_number: str = None
    rating: float = 0
    total_review_count: int = 0
    image: str = None
    role: str = "serviceprovider"
    password: str = None
    
class UpdateServiceProviderProfile(BaseModel):
    name: str 
    work_type: str 
    pay_per_hour: float 
    experience: int 
    email: str 
    phone_number: str
    nid_number: str
    image: str
    password: str = None

class AccessToken(BaseModel):
    access_token: str
    token_type: str
    id: str

class Login(BaseModel):
    role: str
    email: str
    password: str