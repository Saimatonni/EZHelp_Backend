from pydantic import BaseModel

class ServiceProvider(BaseModel):
    name: str = None
    work_type: str = None
    pay_per_hour: float = None
    experience: int = None
    email: str = None
    phone_number: str = None
    nid_number: str = None
    rating: float = None
    total_review_count: int = None
    image: str = None
    role: str = "serviceprovider"
    password: str = None

class AccessToken(BaseModel):
    access_token: str
    token_type: str

class Login(BaseModel):
    role: str
    email: str
    password: str