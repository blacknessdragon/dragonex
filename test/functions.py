from sqlalchemy.orm import Session,joinedload
from model import *
from schma import *
def create_session_in_db(db:Session ,teacher:teacher_base):
    db_teacher = teachers_db(
        name= teacher.name,
        session_number= teacher.session_number,
        for_student= teacher.for_student
    )
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher
def get_teacher_by_name(db:Session, teacher_name:str,for_student:str, skip: int = 0, limit: int = 100, **kwargs):
    return db.query(teachers_db).filter(teachers_db.name == teacher_name).filter(teachers_db.for_student == for_student).offset(skip).limit(100).all()
def get_teacher_by_session(db:Session, teacher_name:str,session_number:int, skip: int = 0, limit: int = 100, **kwargs):
    return db.query(teachers_db).filter(teachers_db.name == teacher_name).filter(teachers_db.session_number == session_number).offset(skip).limit(limit).all()
def create_user(db:Session ,user:user_base):
    db_user = users_db(
        username = user.username,
        password= user.passcode,
        role = user.role,
        rights = user.rights
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return "Done"
def user_by_username(db:Session,username:str):
    return db.query(users_db).filter(users_db.username == username).first()
def add_to_user(name:str,db:Session,username:str ):
    user =  db.query(users_db).filter(username == users_db.username).first()
    teacher = db.query(teachers_db).filter(name == teachers_db.name).first()
    try:    
        user.teachers.append(teacher)
        db.commit()
    except Exception as e:
        if "VALUES " in str(e):
            return "this already is added"
        else:
            return "text support for help"
    return "Done"
def user_sesion(username:str,db:Session):
    findings = db.query(users_db).options(
        joinedload(users_db.teachers)
    ).filter(users_db.username == username).first()
    return findings.teachers
def teachers_users(db:Session):
    teachers = db.query(teachers_db).all()
    users= db.query(users_db).all()
    teacher_list= []
    user_list = []
    for i in range(len(teachers)):
        teacher_list.append(teachers[i].name)
    for i in range(len(users)):
        user_list.append(users[i].username)
    
        
    return teacher_list, user_list

def rights_of_user(username:str,db:Session):
    findings = db.query(users_db).filter(users_db.username == username).first()
    return findings.Rights
