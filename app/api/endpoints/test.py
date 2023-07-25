# from typing import Optional
#
# from fastapi import FastAPI, Path, Query, Form, UploadFile, File, Body
# from enum import StrEnum
#
# app = FastAPI()
#
#
# class EducationLevel(StrEnum):
#     # Укажем значения с большой буквы, чтобы они хорошо смотрелись
#     # в документации Swagger.
#     SECONDARY = 'Среднее образование'
#     SPECIAL = 'Среднее специальное образование'
#     HIGHER = 'Высшее образование'
#
#
# class Person(BaseModel):
#     name: str = Field(
#         ..., max_length=20,
#         title='Полное имя', description='Можно вводить в любом регистре'
#     )
#     surname: Union[str, list[str]] = Field(..., max_length=50)
#     age: Optional[int] = Field(None, gt=4, le=99)
#     is_staff: bool = Field(False, alias='is-staff')
#     education_level: Optional[EducationLevel]
#
#     class Config:
#         title = 'Класс для приветствия'
#         min_anystr_length = 2
#
#
#         @validator('name')
#         def name_cant_be_numeric(cls, value: str):
#         # Проверяем, не состоит ли строка исключительно из цифр:
#             if value.isnumeric():
#                 raise ValueError('Имя не может быть числом')
#         # Если проверка пройдена, возвращаем значение поля.
#             return value
#
#         @root_validator(skip_on_failure=True)
#     # К названию параметров функции-валидатора нет строгих требований.
#     # Первым передается класс, вторым — словарь со значениями всех полей.
#         def using_different_languages(cls, values):
#         # Объединяем все фамилии в единую строку.
#         # Даже если values['surname'] — это строка, ошибки не будет,
#         # просто все буквы заново объединятся в строку.
#             surname = ''.join(values['surname'])
#         # Объединяем имя и фамилию в единую строку.
#             checked_value = values['name'] + surname
#         # Ищем хотя бы одну кириллическую букву в строке
#         # и хотя бы одну латинскую букву.
#         # Флаг re.IGNORECASE указывает на то, что регистр не важен.
#             if (re.search('[а-я]', checked_value, re.IGNORECASE)
#                  and re.search('[a-z]', checked_value, re.IGNORECASE)):
#                 raise ValueError(
#                 'Пожалуйста, не смешивайте русские и латинские буквы'
#             )
#         # Если проверка пройдена, возвращается словарь со всеми значениями.
#             return values
#
#         schema_extra = {
#             'examples': {
#                 'single_surname': {
#                     'summary': 'Одна фамилия',
#                     'description': 'Одиночная фамилия передается строкой',
#                     'value': {
#                         'name': 'Taras',
#                         'surname': 'Belov',
#                         'age': 20,
#                         'is_staff': False,
#                         'education_level': 'Среднее образование'
#                     }
#                 },
#                 'multiple_surnames': {
#                     'summary': 'Несколько фамилий',
#                     'description': 'Несколько фамилий передаются списком',
#                     'value': {
#                         'name': 'Eduardo',
#                         'surname': ['Santos', 'Tavares'],
#                         'age': 20,
#                         'is_staff': False,
#                         'education_level': 'Высшее образование'
#                     }
#                 },
#                 'invalid': {
#                     'summary': 'Некорректный запрос',
#                     'description': 'Возраст передается только целым числом',
#                     'value': {
#                         'name': 'Eduardo',
#                         'surname': ['Santos', 'Tavares'],
#                         'age': 'forever young',
#                         'is_staff': False,
#                         'education_level': 'Среднее специальное образование'
#                     }
#                 }
#             }
#         }
#
#
# @app.get('/{name}', tags=['special methods'])
# def greetings(person: Person = Body(
#             ..., examples=Person.Config.schema_extra['examples']
#         )) -> dict[str, str]:
#     if isinstance(person.surname, list):
#         surnames = ' '.join(person.surname)
#     else:
#         surnames = person.surname
#     result = ' '.join([person.name, surnames])
#     if person.age is not None:
#         result += ', ' + str(person.age)
#     if person.education_level is not None:
#         result += ', ' + person.education_level.lower()
#     if person.is_staff:
#         result += ', сотрудник'
#     return {'Hello': result}
#
#
# @app.post('/login')
# def login(
#         username: str = Form(...),
#         password: str = Form(...),
#         some_file: UploadFile = File(...)
# ):
#     return {'username': username}
