# from pydentic import BaseModel, ConfigDict
# from typing import Optional

from pydantic import BaseModel, ConfigDict

from models import Workloads, Genders, Subjects

class TeachersAddDTO(BaseModel):
    name: str
    surname: str     
    patronymic: str  
    gender: Genders
    subject: Subjects
    workloads: Workloads
    initials: str

class TeachersDTO(TeachersAddDTO):
    id: int
    # initials: str
    

class StudentsAddDTO(BaseModel):
    name: str
    surname: str     
    patronymic: str  
    gender: Genders
    level_fk: int
    leadership_fk: int
    workloads: Workloads
    initials: str

class StudentsDTO(StudentsAddDTO):
    id: int
    # initials: str

class ClassesDTO(BaseModel):
    id: int

class TeachersRelDTO(TeachersDTO):
    students: list['StudentsDTO']

class StudentsRelDTO(StudentsDTO):
    level: 'ClassesDTO'
    leadership: 'TeachersDTO'



# Без relationship
# result_dto = [TeachersDTO.model_validate(row, fromattributes=True) for row in result_orm]

# С relationship
# result_dto = [TeachersRelDTO.model_validate(row, fromattributes=True) for row in result_orm]