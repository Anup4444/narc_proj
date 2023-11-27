from . import db
from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

# Define Python enums


class Status(PyEnum):
    Saved = "Saved"
    Completed = "Completed"


class YesNo(PyEnum):
    Yes = "Yes"
    No = "No"

# Define SQLAlchemy model


class PlantDiagnosticForm(db.Model):
    __tablename__ = 'plant_diagnostic_form'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Use the string values of the Python enums in the SQLAlchemy Enum type constructor
    labcenter_id = db.Column(db.Integer, db.ForeignKey(
        'labcenter.id'), nullable=False)
    specifem_id = db.Column(String(255), nullable=False)
    specimenpreserved_id = db.Column(db.Integer, db.ForeignKey(
        'specimenpreserved.id'), nullable=False)
    storagecondition_id = db.Column(db.Integer, db.ForeignKey(
        'storagecondition.id'), nullable=False)

    date = db.Column(Date, nullable=False)
    diagnostictest_id = db.Column(db.Integer, db.ForeignKey(
        'diagnostictest.id'), nullable=False)
    suspectedproblem_id = db.Column(db.Integer, db.ForeignKey(
        'suspectedproblem.id'), nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'), nullable=False)

    field_reference_id = db.Column(String(255), nullable=False)
    sample_source = db.Column(String(255), nullable=False)
    samplematerialssubmitted_id = db.Column(db.Integer, db.ForeignKey(
        'samplematerialssubmitted.id'), nullable=False)
    sample_collected_date = db.Column(Date, nullable=False)
    physical_sample_received_date = db.Column(Date, nullable=False)

    district_id = db.Column(db.Integer, db.ForeignKey(
        'district.id'), nullable=False)
    provincestate_id = db.Column(db.Integer, db.ForeignKey(
        'provincestate.id'), nullable=False)
    zip_code = db.Column(String(255), nullable=True)
    altitude = db.Column(String(255), nullable=True)
    latitude = db.Column(String(255), nullable=True)
    longitude = db.Column(String(255), nullable=True)
    diagnosisname_id = db.Column(db.Integer, db.ForeignKey(
        'diagnosisname.id'), nullable=False)
    genus_id = db.Column(db.Integer, db.ForeignKey('genus.id'), nullable=False)
    genusspecies_id = db.Column(db.Integer, db.ForeignKey(
        'genusspecies.id'), nullable=False)
    genussubspecies_id = db.Column(db.Integer, db.ForeignKey(
        'genussubspecies.id'), nullable=False)
    genuslabmethods_id = db.Column(db.Integer, db.ForeignKey(
        'genuslabmethods.id'), nullable=False)
    nematode_id = db.Column(db.Integer, db.ForeignKey(
        'nematode.id'), nullable=False)
    nematodespecies_id = db.Column(db.Integer, db.ForeignKey(
        'nematodespecies.id'), nullable=False)
    nematodesubspecies_id = db.Column(db.Integer, db.ForeignKey(
        'nematodesubspecies.id'), nullable=False)
    nematodeextraction_id = db.Column(db.Integer, db.ForeignKey(
        'nematodeextraction.id'), nullable=False)
    insect_name = db.Column(String(100), nullable=False)
    causing_damage_insect = db.Column(
        db.Enum(*[e.value for e in YesNo]), nullable=False)
    insect_notes = db.Column(Text, nullable=True)
    image_path_insect = db.Column(String(500), nullable=True)

    disease_name = db.Column(String(100), nullable=False)
    causing_damage_disease = db.Column(
        db.Enum(*[e.value for e in YesNo]), nullable=False)
    disease_notes = db.Column(Text, nullable=True)
    image_path_disease = db.Column(String(500), nullable=True)

    weeds_name = db.Column(String(100), nullable=False)
    causing_damage_weeds = db.Column(
        db.Enum(*[e.value for e in YesNo]), nullable=False)
    weeds_notes = db.Column(Text, nullable=True)
    image_path_weeds = db.Column(String(500), nullable=True)

    plant_population = db.Column(String(100), nullable=True)
    good_plants = db.Column(String(100), nullable=True)
    signature = db.Column(Text, nullable=True)
    status = db.Column(db.Enum(*[e.value for e in Status]),
                       nullable=False, default=Status.Saved.value)
    user = db.relationship('User', back_populates='forms')

    def __init__(self, user_id, specifem_id=None, specimenpreserved_id=None, storagecondition_id=None, labcenter_id=None, date=None, diagnostictest_id=None, suspectedproblem_id=None, host_id=None, field_reference_id=None, sample_source=None, samplematerialssubmitted_id=None, sample_collected_date=None, physical_sample_received_date=None,  district_id=None, provincestate_id=None, zip_code=None, altitude=None, latitude=None, longitude=None, diagnosisname_id=None, genus_id=None, genusspecies_id=None, genussubspecies_id=None, genuslabmethods_id=None, nematode_id=None, nematodespecies_id=None, nematodesubspecies_id=None, nematodeextraction_id=None, insect_name=None, causing_damage_insect=None, insect_notes=None, image_path_insect=None, disease_name=None, causing_damage_disease=None, disease_notes=None, image_path_disease=None, weeds_name=None, causing_damage_weeds=None, weeds_notes=None, image_path_weeds=None, plant_population=None, good_plants=None, signature=None, status=Status.Saved.value):
        self.user_id = user_id
        self.labcenter_id = labcenter_id
        self.specifem_id = specifem_id
        self.specimenpreserved_id = specimenpreserved_id
        self.storagecondition_id = storagecondition_id

        self.date = date
        self.diagnostictest_id = diagnostictest_id
        self.suspectedproblem_id = suspectedproblem_id
        self.host_id = host_id

        self.field_reference_id = field_reference_id
        self.sample_source = sample_source
        self.samplematerialssubmitted_id = samplematerialssubmitted_id
        self.sample_collected_date = sample_collected_date
        self.physical_sample_received_date = physical_sample_received_date

        self.district_id = district_id
        self.provincestate_id = provincestate_id
        self.zip_code = zip_code
        self.altitude = altitude
        self.latitude = latitude
        self.longitude = longitude
        self.diagnosisname_id = diagnosisname_id
        self.genus_id = genus_id
        self.genusspecies_id = genusspecies_id
        self.genussubspecies_id = genussubspecies_id
        self.genuslabmethods_id = genuslabmethods_id
        self.nematode_id = nematode_id
        self.nematodespecies_id = nematodespecies_id
        self.nematodesubspecies_id = nematodesubspecies_id
        self.nematodeextraction_id = nematodeextraction_id

        self.insect_name = insect_name
        self.causing_damage_insect = causing_damage_insect
        self.insect_notes = insect_notes
        self.image_path_insect = image_path_insect
        self.disease_name = disease_name
        self.causing_damage_disease = causing_damage_disease
        self.disease_notes = disease_notes
        self.image_path_disease = image_path_disease
        self.weeds_name = weeds_name
        self.causing_damage_weeds = causing_damage_weeds
        self.weeds_notes = weeds_notes
        self.image_path_weeds = image_path_weeds
        self.plant_population = plant_population
        self.good_plants = good_plants
        self.signature = signature
        self.status = status

    def __repr__(self):
        return f"<PlantDiagnosticForm {self.id}>"
