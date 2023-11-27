# from setup.dbsetup import db
from datetime import datetime
from . import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def update(cls, filter, data):
        cls.query.filter_by(**filter).update(data)
        db.session.commit()

    @classmethod
    def search(cls, filter):
        return cls.query.filter_by(**filter).all()

    @classmethod
    def addData(cls, data):
        new_record = cls(**data)
        db.session.add(new_record)
        db.session.commit()
        return new_record


class Host(BaseModel):
    __tablename__ = 'host'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(255), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    diagnostic_forms = relationship('PlantDiagnosticForm', backref='host')


class DiagnosticTest(BaseModel):
    __tablename__ = 'diagnostictest'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    diagnostic_forms = relationship(
        'PlantDiagnosticForm', backref='diagnostictest')


class SuspectedProblem(BaseModel):
    __tablename__ = 'suspectedproblem'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    # This establishes the relationship so you can get associated forms for a host
    diagnostic_forms = relationship(
        'PlantDiagnosticForm', backref='suspectedproblem')


class SampleMaterialsSubmitted(BaseModel):
    __tablename__ = 'samplematerialssubmitted'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    # This establishes the relationship so you can get associated forms for a host
    diagnostic_forms = relationship(
        'PlantDiagnosticForm', backref='samplematerialsubmitted')


class ProvinceState(BaseModel):
    __tablename__ = 'provincestate'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    # This establishes the relationship so you can get associated forms for a host
    diagnostic_forms = relationship(
        'PlantDiagnosticForm', backref='provincestate')


class District(BaseModel):
    __tablename__ = 'district'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    # This establishes the relationship so you can get associated forms for a host
    diagnostic_forms = relationship('PlantDiagnosticForm', backref='district')


class DiagnosisName(BaseModel):
    __tablename__ = 'diagnosisname'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    # This establishes the relationship so you can get associated forms for a host
    diagnostic_forms = relationship(
        'PlantDiagnosticForm', backref='diagnosisname')


class Genus(BaseModel):
    __tablename__ = 'genus'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    # This establishes the relationship so you can get associated forms for a host
    diagnostic_forms = relationship('PlantDiagnosticForm', backref='genus')


class GenusSpecies(BaseModel):
    __tablename__ = 'genusspecies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    # This establishes the relationship so you can get associated forms for a host
    diagnostic_forms = relationship(
        'PlantDiagnosticForm', backref='genusspecies')


class GenusSubSpecies(BaseModel):
    __tablename__ = 'genussubspecies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    # This establishes the relationship so you can get associated forms for a host
    diagnostic_forms = relationship(
        'PlantDiagnosticForm', backref='genussubspecies')


class GenusLabMethods(BaseModel):
    __tablename__ = 'genuslabmethods'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    # This establishes the relationship so you can get associated forms for a host
    diagnostic_forms = relationship(
        'PlantDiagnosticForm', backref='genuslabmethods')


class Nematode(BaseModel):
    __tablename__ = 'nematode'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    # This establishes the relationship so you can get associated forms for a host
    diagnostic_forms = relationship('PlantDiagnosticForm', backref='nematode')


class NematodeSpecies(BaseModel):
    __tablename__ = 'nematodespecies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    # This establishes the relationship so you can get associated forms for a host
    diagnostic_forms = relationship(
        'PlantDiagnosticForm', backref='nematodespecies')


class NematodeSubSpecies(BaseModel):
    __tablename__ = 'nematodesubspecies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    # This establishes the relationship so you can get associated forms for a host
    diagnostic_forms = relationship(
        'PlantDiagnosticForm', backref='nematodesubspecies')


class NematodeExtraction(BaseModel):
    __tablename__ = 'nematodeextraction'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)

    status = db.Column(db.Integer, nullable=False)
    # This establishes the relationship so you can get associated forms for a host
    diagnostic_forms = relationship(
        'PlantDiagnosticForm', backref='nematodeextraction')


class LabCenter(BaseModel):
    __tablename__ = 'labcenter'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    # This establishes the relationship so you can get associated forms for a host
    diagnostic_forms = relationship('PlantDiagnosticForm', backref='labcenter')
    users = db.relationship('User', back_populates='labcenter')



class SpecimenPreserved(BaseModel):
    __tablename__ = 'specimenpreserved'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    # This establishes the relationship so you can get associated forms for a host
    diagnostic_forms = relationship(
        'PlantDiagnosticForm', backref='specimenpreserved')


class StorageCondition(BaseModel):
    __tablename__ = 'storagecondition'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    # This establishes the relationship so you can get associated forms for a host
    diagnostic_forms = relationship(
        'PlantDiagnosticForm', backref='storagecondition')

    
