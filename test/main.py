from schma import *
from model import *
from functions import *
from db_setup import get_db,engine
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends, Request ,HTTPException,status
from fastapi.responses import StreamingResponse
import qrcode
from io import BytesIO
Base.metadata.create_all(engine)

from starlette.middleware.sessions import SessionMiddleware
app = FastAPI(title='a7a project')
def check_auth(req:Request):
    user =  req.session.get("username")
    if not user :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
def check_auth_and_admin(req:Request):
    user =  req.session.get("username")
    if not user or req.session.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
"""domain=None,
    secure=True,  # HTTPS only
    httponly=True,  # No JavaScript access
    samesite="lax"  # CSRF protection"""
app.add_middleware(
    SessionMiddleware,
    "nigga",
    max_age=50000,
    path="/"
)
@app.post('/create_teacher_session/')
def create_session(req:Request,teacher:teacher_base,db:Session = Depends(get_db)):
    check_auth_and_admin(req)
    if_sesion = get_teacher_by_session(db=db,teacher_name=teacher.name,session_number=teacher.session_number)
    if if_sesion:
        return "already exist"
    else:
        try:
            create_session_in_db(db=db,teacher=teacher)
            return "complete the op"
        except Exception as e:
            if "sqlite3.IntegrityError" in str(e):
                return "this session number already exist"
            else:
                return str(e)
@app.get('/')
async def home(req:Request):
    if req.session:
        person =req.session.get('username')
    else:
        person = "nobody"
    return "hello amigo %s"%(person)
@app.post('/login')
async def login(user:user_base,request:Request,db:Session= Depends(get_db)):
    if_user= user_by_username(db=db,username=user.username)
    if if_user:
        if  user.passcode == if_user.password:
            request.session['username'] = user.username
            request.session['role'] = if_user.role
            return "loged in:%s"%(if_user.rights)
        else:
            return "wrong password"
@app.post('/signup')
async def signup(request:Request,user:user_base,db:Session= Depends(get_db)):
    user.role = "user"
    if_user= user_by_username(db=db, username=user.username)
    if if_user:
        return "was there"
    responed = create_user(db=db,user=user)
    request.session['username'] = user.username
    request.session['role'] = user.role
    return "%s:%s"%(responed, user.rights)
@app.post('/signup/admin9595')
async def signup(request:Request, user:user_base,db:Session= Depends(get_db)):
    user.role = "admin"
    if_user= user_by_username(db=db, username=user.username)
    if if_user:
        return "was there"
    responed = create_user(db=db,user=user)
    request.session['username'] = user.username
    request.session['role'] = user.role
    return  responed
@app.get('/session/{teacher}/{for_student}')
async def session(req:Request,teacher:str,for_student:str,db:Session = Depends(get_db)):
    #check_auth(req)
    data=get_teacher_by_name(db,teacher,for_student)
    return data[0]
@app.get('/code/')
async def code_gen(req:Request,teacher:str,for_student:str):
    #check_auth(req)
    data = 'http://127.0.0.1:8000/session/%s/%s'%(teacher,for_student)
    if data:
        img = qrcode.make(data)
        img_buffer = BytesIO()
        img.save(img_buffer,format='PNG')
        img_buffer.seek(0)
        return StreamingResponse(img_buffer,media_type='image/png')
    else:
        return "check the url right"

@app.post('/linker')
async def linker(req:Request,name:str,username:str,db:Session = Depends(get_db)):
    check_auth_and_admin(req)
    check = add_to_user(name,db,username)
    return check
@app.get('/courses')
async def sessions(req:Request,db:Session = Depends(get_db)):
    check_auth(req)
    username = req.session.get("username")
    findings = list(user_sesion(username,db))
    return findings
@app.get('/all')
async def all_data(req:Request,db:Session = Depends(get_db)):
    check_auth(req)
    teachers ,users = teachers_users(db)
    data = {"teachers":teachers ,"users":users}
    return data