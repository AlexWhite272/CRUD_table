from sqlalchemy import event, create_engine, select, update, insert  
from sqlalchemy.orm import sessionmaker
from models import Abstract, Teachers, Students, Workloads, Genders, Subjects, Classes, createInitials
from schemas import TeachersRelDTO, StudentsRelDTO, StudentsAddDTO, ClassesDTO


engine = create_engine('sqlite:///project.db?charset=utf8', echo = False)

session_factory = sessionmaker(engine, expire_on_commit=True, autoflush=False)

# @event.listens_for(session_factory, 'before_flush')
# def event_after_commit(session, flush_context, instances):
#     arrayObject = session.execute(select(Teachers)).scalars().all()
#     for element in arrayObject:
#         if isinstance(element, Teachers):
#             element.initials = createInitials(element.name, element.surname, element.patronymic)

    

def add_classes():
    i = 0 
    with session_factory() as session:
        try:    
            while i <= 11:
                object = Classes()
                session.add(object)
                i += 1

        except ValueError as e:
            session.rollback()
            print("Ошибка")
        else:
            session.commit()
            # print('Успех') 


def create_data_answer(code, data):
    body = {
        "code": code,
        "result": data 
    }
    return body



def add_teachers(data):
    data = data.get('data_object')
    array_new_teacher = []
    with session_factory() as session:
        i = 0
        try:
            while i < len(data):
                new_teacher = Teachers()
                for key in data[i]:
                    if hasattr(new_teacher, key):
                        setattr(new_teacher, key, data[i].get(key))
                    else:
                        session.rollback()
                        raise AttributeError( f"Неверный параметр: '{key}'!")
                new_teacher.initials = createInitials(new_teacher.name, new_teacher.surname, new_teacher.patronymic)
                session.add(new_teacher) 
                array_new_teacher.append(new_teacher)
                i += 1
              
        except Exception as error:
            session.rollback()
            data = create_data_answer(400, error)
            
            return data
        else:

            session.commit()
            result_dto = [TeachersRelDTO.model_validate(row, from_attributes=True).model_dump() for row in array_new_teacher]
            data = create_data_answer(200, result_dto)
            
            return data

def delete_teacher(teacher_id):
    with session_factory() as session:

        teacher = session.get(Teachers, teacher_id)
        
        try:
            if teacher == None:
                data = create_data_answer(404,  f"Преподаватель c id={teacher_id} не найден!")
                return data
            
            session.delete(teacher)
        
        except Exception as error:
            session.rollback()
            data = create_data_answer(400, error)

            return data
        else:
            session.commit()
       
            data = create_data_answer(200, True)

            return data
 
def update_teachers(data):
    if "new_values" not in data:
        return create_data_answer(400, "Bad request")
    
    new_values = data.get("new_values")

    with session_factory() as session:
        try:
            teacher = session.get(Teachers, data.get("id"))
            
            if teacher == None:
                result = create_data_answer(404, f"Преподаватель c id={data.get("id")} не найден!")
                return result
            
            for key in new_values:
                if hasattr(Teachers, key):
                    setattr(teacher, key, new_values.get(key))
                else:
                    session.rollback()
                    raise AttributeError(f"Неверный параметр: '{key}'!")
            
            session.flush()

        except Exception as error:
            session.rollback()
            result = create_data_answer(400, error)

            return result
        
        else:
            session.commit()
            result_dto = [TeachersRelDTO.model_validate(row, from_attributes=True).model_dump() for row in [teacher]]

            result = create_data_answer(201, result_dto)
            return result

def select_teacher(teacher_id = None):
    with session_factory() as session:
        if teacher_id != None:
            query = select(Teachers).filter(
                Teachers.id == teacher_id
            )
            result_orm = session.execute(query)
            teacher = result_orm.scalars().one_or_none()
            
            if teacher == None:
                data = create_data_answer(404, f"Teacher with id={teacher_id} is not founded!")
                return data
                 
            teacher = [teacher]
        else:
            query = select(Teachers)
            result_orm = session.execute(query)
            teacher = result_orm.scalars().all()

        
        result_dto = [TeachersRelDTO.model_validate(row, from_attributes=True).model_dump() for row in teacher]

        data = create_data_answer(200, result_dto)
        
        return data
    

def add_students(data):
    data = data.get('data_object')
    array_new_student = []
    with session_factory() as session:
        i = 0
        try:
            while i < len(data):
                new_student = Students()
                for key in data[i]: 
                    if hasattr(new_student, key):
                        setattr(new_student, key, data[i].get(key))
                    else:
                        session.rollback()
                        raise AttributeError( f"Колонка '{key}' отсутствует в таблице!")
                new_student.initials = createInitials(new_student.name, new_student.surname, new_student.patronymic)    
                session.add(new_student) 
                array_new_student.append(new_student)
                i += 1  

        except Exception as error:
            session.rollback()
            data = create_data_answer(400, error)
            
            return data
        else:

            session.commit()
            result_dto = [ StudentsRelDTO.model_validate(row, from_attributes=True).model_dump() for row in array_new_student]
            data = create_data_answer(200, result_dto)
            
            return data

def select_students(student_id = None):
    
    with session_factory() as session:
        if student_id != None:
            query = select(Students).filter(
                Students.id == student_id
            )
            result_orm = session.execute(query)
            student = result_orm.scalars().one_or_none()

            if student == None:
                data = create_data_answer(404, f"Преподаватель c id={student_id} не найден!)")

                return data

            student = [student]
        else:
            query = select(Students)
            result_orm = session.execute(query)
            student = result_orm.scalars().all()
        
        result_dto = [StudentsRelDTO.model_validate(row, from_attributes=True).model_dump() for row in student]
        
        data = {
            "code": 200,
            "result": result_dto
        }
        return data

def update_student(data):
    new_values = data.get("new_values")

    with session_factory() as session:
        try:
            student = session.get(Students, data.get("id"))
            
            if student == None:
                data = create_data_answer(404, f"Студент c id={data.get("id")} не найден!")

                return data
        
            for key in new_values:
                if hasattr(Students, key):
                    setattr(student, key, new_values.get(key))
                else:
                    session.rollback()
                    raise AttributeError( f"Неверный параметр: '{key}'!")
            
            session.flush()

        except Exception as error:
            session.rollback()
            data = create_data_answer(400,  error)

            return data
        
        else:
            session.commit()
            result_dto = [TeachersRelDTO.model_validate(row, from_attributes=True).model_dump() for row in [student]]

            data = create_data_answer(201, result_dto)

            return data   

def delete_student(student_id):
    with session_factory() as session:

        student = session.get(Students, student_id)
        
        try:
            if student == None:
                data = create_data_answer(404, f"Студент c id={student_id} не найден!")
                return data
            
            session.delete(student)
        except Exception as error:
            session.rollback()
            data = create_data_answer(400, error)
  
            return data
        else:
            session.commit()
            data = create_data_answer(200, True) 

            return data 


def select_subjects():

    return create_data_answer(200, Subjects.get_dict())

def select_workloads():
    
    return create_data_answer(200, Workloads.get_dict())

def select_genders():
    
    return create_data_answer(200, Genders.get_dict())
    
def select_classes(id = None):
       with session_factory() as session:
       
        query = select(Classes)
        res = session.execute(query)
        result_orm = res.scalars().all()
  
        result_dto = [ClassesDTO.model_validate(row, from_attributes=True).model_dump() for row in result_orm]
        
        result = create_data_answer(200, result_dto)
        return result

# curl -i -H "Content-Type: application/json" -X POST -d "{"""data_teachers""": [{"""name""":"""Анна""","""surname""":"""Белова""","""patronymic""":"""Александровна""", """gender""":"""women""","""subject""":"""language""","""workloads""":"""evening_shift"""}]}" http://localhost:5000/api/teachers


#  {"name":"Анна","surname":"Белова", "patronymic":"Александровна", "gender": "women","subject": "language","workloads": "evening_shift"}
data_teachers = {"data_object": [
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
    }

data_students = {"data_object": [
        {
            'name'          : 'Саша',                                             
            'surname'       : 'Филимонов', 
            'patronymic'    : 'Олегович', 
            'gender'        : Genders.man,
            'workloads'     : Workloads.morning_shift,
            'level_fk'      : 5,
            'leadership_fk' : 1
        },
        {
            'name'          : 'Аня',                                             
            'surname'       : 'Кержакова', 
            'patronymic'    : 'Олеговна', 
            'gender'        : "women",
            'workloads'     : Workloads.morning_shift,
            'level_fk'      : 5,
            'leadership_fk' : 1
        }
    ]
}

update_data_teacher = {
    "id"            : 2,
    "new_values"    :   {
        "name"      : "111",
        "subject"   : "literature"
    }

}




def createDB():
    Abstract.metadata.drop_all(engine)
    Abstract.metadata.create_all(engine)

    add_classes()

    add_teachers(data_teachers)

    add_students(data_students)

# createDB()

# list_teachers = select_teacher()
# print(list_teachers)

# list_students = select_students()
# print(list_students)

# list_classes = select_classes(5)
# print(list_classes)

# update_teachers(update_data_teacher)
