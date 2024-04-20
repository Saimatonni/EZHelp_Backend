import os
from jose import jwt, JWTError
from fastapi import HTTPException

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")

def validate_access_token(access_token: str):
    try:
        if not access_token:
            raise HTTPException(status_code=401, detail="Unauthorized")

        payload = jwt.decode(access_token, JWT_SECRET, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if not user_email:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_email
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



