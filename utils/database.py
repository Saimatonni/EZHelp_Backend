from config.db import db

def get_user_id_by_email(email):
    user = db.get_collection("clients").find_one({"email": email})
    if user:
        return user["_id"]
    else:
        return None
    
def get_sp_id_by_email(email):
    user = db.get_collection("service_providers").find_one({"email": email})
    if user:
        return user["_id"]
    else:
        return None
