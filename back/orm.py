from sqlalchemy import create_engine, select, update, insert  
from database import session_factory
from models import Abstract, Teachers, Students, Workloads, Genders, Subjects, Classes
from schemas import TeachersRelDTO

data_teachers = [
        {
            'name'          :'Мария',                                             
            'surname'       : 'Филимонова', 
            'patronymic'    : 'Олеговна', 
            'gender'        : Genders.women,
            'subject'       : Subjects.literature,
            'workloads'     : Workloads.morning_shift
        },

        {
            'name'         :'Ольга', 
            'surname'      :'Владимировна', 
            'patronymic'   :'Васнецова', 
            'gender'       : Genders.women,
            'subject'      : Subjects.mathematics,
            'workloads'    : Workloads.morning_shift
        }
    ]

def add_teachers(data):
    with session_factory() as session:
        try:
            for item in data:
                object = Teachers(
                    name        =item.get('name'),
                    surname     =item.get('surname'), 
                    patronymic  =item.get('patronymic'), 
                    gender      =item.get('gender'),
                    subject     =item.get('subject'),
                    workloads   =item.get('workloads'))
                
                session.add(object)   
        except ValueError as e:
            session.rollback()
            print("Ошибка")
        else:
            session.commit()
            print('Успех')
            # result_dto = [TeachersRelDTO.model_validate(row, fromattributes=True) for row in result_orm]
            # return result_dto

def delete_teachers():
    with session_factory() as session:
        query = select(Teachers)
        result = session.execute(query)
        for item in result:
            session.delete(item)
        #query = session.get(Teachers)
        try:
            session.delete(query)
        except:
            session.rollback()
            print("Ошибка")
        else:
            session.commit()
            print('Успех')
 
def update_teachers():
    with session_factory() as session:
        try:
            query = select(Teachers).filter(
                Teachers.surname=="Филимонова"
            )
            teacher = session.execute(query).scalars().first()
            teacher.subject = Subjects.literature
            session.flush()
        except:
            session.rollback()
            print("Ошибка")
        else:
            session.commit()

            print('Успех')

def select_teacher():
    with session_factory() as session:
       
        # query = select(Teachers).filter(
        #     Teachers.surname=="Филимонова"
        # )
        query = select(Teachers)
        result_orm = session.execute(query)
        teachers = result_orm.all()
        print(teachers)
        result_dto = [TeachersRelDTO.model_validate(row, fromattributes=True) for row in result_orm]
        return result_dto
    
# add_teachers(data_teachers)

list_teachers = select_teacher()
print(list_teachers)
