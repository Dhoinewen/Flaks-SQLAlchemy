from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

conn = create_engine("postgresql+psycopg2://postgres:123456@localhost/test", echo=False)
Session = sessionmaker()
session = Session(bind=conn)

Base = declarative_base()


association = Table(
    'association',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('courses.id')),
    Column('course_id', Integer, ForeignKey('students.id'))
)


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    students = relationship('Student', backref='group', lazy=True)

    def __repr__(self):
        return f'{self.name}'


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    first_name = Column(String(250), nullable=False)
    last_name = Column( String(250), nullable=False)
    courses = relationship(
        'Course', secondary=association,
        back_populates='students', lazy=True
    )

    def __repr__(self):
        return f'{self.first_name}'


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(1024))
    students = relationship(
        'Student', secondary=association,
        back_populates='courses', lazy=True
    )

    def __repr__(self):
        return f'{self.name}'


Base.metadata.create_all(bind=conn)

