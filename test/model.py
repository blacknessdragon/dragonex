from db_setup import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column,String, Integer,ForeignKey,Table

m_t_m =Table(
    "courses",
    Base.metadata,
    Column("teacher_name", ForeignKey("teachers.name"),primary_key=True),
    Column("users_name", ForeignKey("users.username"),primary_key=True)
)

class teachers_db(Base):
    __tablename__ = "teachers"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    session_number = Column(Integer,unique=True)
    for_student = Column(String)
    user = relationship("users_db", secondary=m_t_m,back_populates="teachers")
class users_db(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String)
    rights = Column(String)
    teachers = relationship("teachers_db", secondary=m_t_m,back_populates="user")
