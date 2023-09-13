from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Person(Base):
    __tablename__ = "user"
    required = ["name"]

    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True)

    def __init__(self, **kwargs):
        for key in kwargs:
            if key in Person.required:
                setattr(self, key, kwargs[key])

    def to_dict(self):
        obj_dict = self.__dict__
        obj_dict.pop("_sa_instance_state", None)
        return obj_dict
