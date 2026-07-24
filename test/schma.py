from pydantic import BaseModel
class teacher_base(BaseModel):
    name:str
    session_number:int
    for_student:str
    
    class Config:
        from_attributes = True

class user_base(BaseModel):
    username:str
    passcode:str
    role:str = None
    rights:str = "both"
    sessions:list[teacher_base] = []
    class Config:
        from_attributes = True
