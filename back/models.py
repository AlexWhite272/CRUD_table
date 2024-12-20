import enum
# from sqlalchemy_events import listen_events, on
from sqlalchemy import ForeignKey 
from sqlalchemy.orm import Mapped, mapped_column, relationship, as_declarative


def createInitials(name, surname, patronomic):
    return f'{surname} {name[0]}.{patronomic[0]}.'


@as_declarative()
class Abstract:
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

class Workloads(str, enum.Enum):
    morning_shift = "Дневная смена"
    evening_shift = "Вечерняя смена"
    
    def get_dict():
        return {
                "morning_shift"   : "Дневная смена",
                "evening_shift"   : "Вечерняя смена"
            }

class Genders(str, enum.Enum):
    man     = "М"
    women   = "Ж"

   

    def get_dict():
        return {
            "man"     : "М",
            "women"   : "Ж"
        }

class Subjects(str, enum.Enum):
    mathematics     = "Математика"
    language        = "Языковедение"
    literature      = "Литература"

    def get_dict():
        return {
            "mmathematicsan"    : "Математика",
            "language"          : "Языковедение",
            "literature"        : "Литература"
        }

class Teachers(Abstract):
    __tablename__ = 'teachers'
    name: Mapped[str]        
    surname: Mapped[str]     
    patronymic: Mapped[str]  
    gender: Mapped[Genders]
    workloads: Mapped[Workloads]
    subject: Mapped[Subjects]
    students: Mapped[list['Students']] = relationship(back_populates='leadership')
    initials: Mapped[str]

class Students(Abstract):
    __tablename__ = 'students'
    name: Mapped[str]     
    surname: Mapped[str]   
    patronymic: Mapped[str]  
    gender: Mapped[Genders] 
    workloads: Mapped[Workloads]
    level: Mapped['Classes']        = relationship(back_populates='students', uselist=False)
    level_fk: Mapped[int]           = mapped_column(ForeignKey('classes.id'))
    leadership_fk: Mapped[int]      = mapped_column(ForeignKey('teachers.id'))
    leadership: Mapped['Teachers']  = relationship(back_populates='students', uselist=False)
    initials: Mapped[str]
    
    # def __init__(self, name, surname, patronymic):
    #     self.initials = createInitials(name, surname, patronymic)
    
class Classes(Abstract):
    __tablename__ = 'classes'
    students: Mapped[list['Students']] = relationship(back_populates='level') 
   

