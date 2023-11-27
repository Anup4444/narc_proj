from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, TextAreaField, RadioField, IntegerField, FileField, FloatField
from wtforms.validators import DataRequired, Length, Optional, ValidationError, NumberRange, Email, Regexp
from models.plant_diagnostic_form import Status, YesNo


class PlantDiagnosticFormForm(FlaskForm):
    labcenter = SelectField('LabCenter', validators=[
                            DataRequired()], coerce=int)
    specimenpreserved = SelectField('SpecimenPreserved', validators=[
        DataRequired()], coerce=int)

    storagecondition = SelectField('StorageCondition', validators=[
        DataRequired()], coerce=int)

    date = DateField('Date', validators=[DataRequired()])
    specifem_id = IntegerField('Specifem ID', validators=[
        DataRequired(), NumberRange(min=1, max=9999)])
    diagnostictest = SelectField('DiagnosticTest', validators=[
                                 DataRequired()], coerce=int)
    suspectedproblem = SelectField('DiagnosticTest', validators=[
                                   DataRequired()], coerce=int)

    host = SelectField('Host', validators=[DataRequired()], coerce=int)

    field_reference_id = IntegerField('Field Reference ID', validators=[
                                      DataRequired(), NumberRange(min=0, max=99999)], render_kw={"id": "field_reference_id"})
    sample_source = StringField('Sample Source', validators=[
                                Optional()])
    samplematerialssubmitted = SelectField('SampleMaterialsSubmitted', validators=[
        DataRequired()], coerce=int)
    sample_collected_date = DateField(
        'Sample Collected Date', validators=[DataRequired()])
    physical_sample_received_date = DateField(
        'Physical Sample Received Date', validators=[DataRequired()])

    district = SelectField('District', validators=[DataRequired()], coerce=int)
    provincestate = SelectField('ProvinceState', validators=[
                                DataRequired()], coerce=int)
    zip_code = IntegerField('ZIP Code', validators=[
                            Optional(), NumberRange(min=0, max=999999999)], render_kw={"id": "zip_code"})
    altitude = IntegerField('Altitude', validators=[
        Optional(), NumberRange(min=-9999, max=9999)])
    latitude = IntegerField('Latitude', validators=[
        Optional(), NumberRange(min=-90, max=90)])
    longitude = IntegerField('Longitude', validators=[
        Optional(), NumberRange(min=-180, max=180)])
    diagnosisname = SelectField('DiagnosisName', validators=[
        DataRequired()], coerce=int)
    genus = SelectField('genus', validators=[DataRequired()], coerce=int)
    genusspecies = SelectField('GenusSpecies', validators=[
                               DataRequired()], coerce=int)
    genussubspecies = SelectField('GenusSubSpecies', validators=[
                                  DataRequired()], coerce=int)
    genuslabmethods = SelectField('GenusLabMethods', validators=[
                                  DataRequired()], coerce=int)

    nematode = SelectField('Nematode', validators=[DataRequired()], coerce=int)
    nematodespecies = SelectField('NematodeSpecies', validators=[
                                  DataRequired()], coerce=int)
    nematodesubspecies = SelectField('NematodeSubSpecies', validators=[
                                     DataRequired()], coerce=int)
    nematodeextraction = SelectField('NematodeExtraction', validators=[
                                     DataRequired()], coerce=int)

    insect_name = StringField('Insect Name', validators=[
                              Optional(), Length(max=100)])
    causing_damage_insect = SelectField('Insect Causing Damage', validators=[
                                        Optional()], choices=[(e.value, e.name) for e in YesNo])
    insect_notes = TextAreaField('Insect Notes', validators=[Optional()])
    image_path_insect = FileField('Insect Image', validators=[Optional()])

    disease_name = StringField('Disease Name', validators=[
                               Optional(), Length(max=100)])
    causing_damage_disease = SelectField('Disease Causing Damage', validators=[
                                         Optional()], choices=[(e.value, e.name) for e in YesNo])
    disease_notes = TextAreaField('Disease Notes', validators=[Optional()])
    image_path_disease = FileField('Disease Image', validators=[Optional()])
    weeds_name = StringField('Weeds Name', validators=[
                             Optional(), Length(max=100)])
    causing_damage_weeds = SelectField('Weeds Causing Damage', validators=[
                                       Optional()], choices=[(e.value, e.name) for e in YesNo])
    weeds_notes = TextAreaField('Weeds Notes', validators=[Optional()])
    image_path_weeds = FileField('Weeds Image', validators=[Optional()])
    plant_population = IntegerField('Plant Population', validators=[
        Optional(), NumberRange(min=0, max=9999999999)])
    good_plants = IntegerField('Good Plants', validators=[
        Optional(), NumberRange(min=0, max=9999999999)])
    signature = TextAreaField('Signature', validators=[Optional()])
    status = SelectField('Status', validators=[DataRequired()], choices=[
                         (e.value, e.name) for e in Status], default=Status.Saved.value)


class UnifiedMessageForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Regexp(r'^[A-Za-z\s]+$', message="Username must contain only letters")
    ])
    phone_number = StringField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^\d{10}$', message="Phone number should be 10 digits")
    ])
    email = StringField('Email', validators=[Optional(), Email()])
    host = SelectField('Host', validators=[
                       DataRequired()], coerce=int)
    recommended_signature = SelectField(
        'Recommended Signature', coerce=int, choices=[], validators=[Optional()])
    signature = TextAreaField('Signature', validators=[DataRequired()])

    # This radio field allows the user to choose between email or SMS
    contact_method = RadioField('Contact Method', choices=[(
        'email', 'Email'), ('sms', 'SMS')], validators=[DataRequired()])
    submit = SubmitField('Send Message')
