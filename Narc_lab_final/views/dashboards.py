
import re
from flask import send_from_directory
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify, request, send_file
import requests
from flask_login import login_required, current_user
from models.user import User, Message, Signature
from models.plant_diagnostic_form import PlantDiagnosticForm
from models import *
from werkzeug.security import generate_password_hash
from decorators import superuser_required
from forms import PlantDiagnosticFormForm, UnifiedMessageForm
from forms import Status
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask import current_app
from sqlalchemy import func
from models.db_update import *
import json
import pandas as pd
import io
import numpy as np


from email_utils import send_email


dashboards = Blueprint('dashboards', __name__)


SMS_API_ENDPOINT = "https://sms.aakashsms.com/sms/v3/send/"


@dashboards.route('/message_list')
@login_required
def message_list():
    if current_user.role == 'admin':
        messages = Message.query.all()
    else:
        messages = Message.query.filter_by(sender_id=current_user.id).all()
    return render_template('message_list.html', messages=messages)


html_content = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crop Diagnostic Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #e8f5e9; /* Green tint background */
        }}

        .container {{
            margin: 0 auto;
            max-width: 800px;
            padding: 20px;
            background-color: #ffffff;
            border: 2px solid #4caf50; /* Green border */
            border-radius: 8px;
        }}

        .header, .footer {{
            text-align: center;
            color: #4caf50; /* Green text color */
        }}

        label {{
            display: block;
            margin-bottom: 10px;
            font-weight: bold;
            color: #4caf50; /* Green text color */
        }}

        ul {{
            margin-left: 20px;
            margin-bottom: 10px;
            color: #4caf50; /* Green text color */
        }}
        
        .img-left, .img-right {{
            position: absolute;
            top: 20px; /* Adjust as per requirement */
        }}

        .img-left {{
            left: 20px; /* Adjust as per requirement */
        }}

        .img-right {{
            right: 20px; /* Adjust as per requirement */
        }}
    </style>
</head>

<body>

    <div class="container">
        <div class="header">
           <img src="" alt="Left Image" class="img-left">
        <img src="" alt="Right Image" class="img-right">
            <h2>वाणिज्य मंत्रालय खाद्य प्रशासन विभाग</h2>
            <h2>Crop Diagnostic Report</h2>
        </div>

        <div>
            
            <label>कृषक/प्रस्तुतकर्ता नाम (Farmer/submitter’s name):{username}</label>
            <label>कृषक/प्रस्तुतकर्ता ठेगाना (Farmer/Submitter’s address):</label>
            <label>कृषक/प्रस्तुतकर्ता संस्थाको नाम (Organization):</label>
            <label>सम्पर्क नम्बर (Contact number):{phone_number}</label>
            <label>ईमेल (Email):{email}</label>

            <label>फसल (Crop):</label>
            <label>जात (Variety):</label>
            <label>नमूना सुगात (Sample):</label>
            <label>संक्रमित चेत्र (Infected Area):</label>
            <label>संक्रमित बोटको संख्या (Number of plants infected):</label>
            <label>संक्रमित चेत्रको प्रतिशत (Incidence):</label>
            <label>रोगको गंभिरता (Severity):</label>
            <label>प्रति बोट मा किराको संख्या (Number of Insect per plant):</label>
            <label>प्रति वर्ग मिटरमा झारको संख्या (Number of weed per square meter):</label>

            <label>निदानमा प्रयोग गरिएको विधि (Methods used in Diagnosis):</label>
            
          

            <label>नतिजा (Results):</label>

            <label>Recommended Management Strategies (सुझावित प्रबंधन स्ट्राटेजी):</label>

            <div class="footer center">
            <p></p>
                <p>..................</p>
                
                <p>Diagnostician’s Name and Signature</p>
            </div>
        </div>

    </div>

</body>

</html>


"""


@dashboards.route('/send_message', methods=['GET', 'POST'])
@login_required
def send_message():
    form = UnifiedMessageForm()

    hosts = Host.query.all()
    host_choices = [(host.id, host.value) for host in hosts]

    form.host.choices = host_choices

    if request.method == 'POST':

        host_id = form.host.data
        if host_id:

            recommended_signatures = Signature.query.filter_by(
                host_id=host_id).all()

            signature_choices = [(sig.id, sig.recommended_text)
                                 for sig in recommended_signatures]
            form.recommended_signature.choices = signature_choices

    if form.validate_on_submit():
        username = form.username.data

        phone_number = form.phone_number.data
        email = form.email.data
        host_id = form.host.data
        contact_method = form.contact_method.data

        signature = form.signature.data

        if signature:
            existing_signature = Signature.query.filter_by(
                recommended_text=signature, host_id=host_id).first()
            if not existing_signature:
                host = Host.query.get(host_id)
                if not host:
                    flash("Invalid host ID. Please try again.", 'error')
                    return redirect(url_for('dashboards.send_message'))
                new_signature = Signature(
                    recommended_text=signature, host=host, status=1)
                db.session.add(new_signature)
                db.session.commit()
                signature_id = new_signature.id
            else:
                signature_id = existing_signature.id
        else:
            signature_id = form.recommended_signature.data
            signature_obj = Signature.query.get(signature_id)
            if signature_obj:
                signature = signature_obj.recommended_text
            else:
                flash("Invalid signature ID. Please try again.", 'error')
                return redirect(url_for('dashboards.send_message'))

        signature = form.signature.data

        host_obj = Host.query.get(host_id)

        if host_obj is None:
            flash("Invalid host ID. Please try again.", 'error')

            return redirect(url_for('dashboards.send_message'))

        # Use the username in your HTML content
        formatted_html_content = html_content.format(
            username=username, phone_number=phone_number, email=email, signature=signature)

        if contact_method == "email":
            subject = f"Message from {username}"
            recipients = [email]
            text_body = f"Farmer Name: {username}\nEmail: {email}\nHost: {host_obj.value}\nRemark: {signature}"

            message = Message(
                username=username,
                phone_number='',
                email=email,
                host=host_obj,
                message_type='Email',
                signature=signature,
                sender=current_user

            )

            try:
                db.session.add(message)
                db.session.commit()

                # Modify this line to add the html_content as an attachment
                send_email(subject, current_user.email,
                           recipients, text_body, formatted_html_content)
                flash("Email sent successfully!", 'success')
                return redirect(url_for('dashboards.send_message'))
            except Exception as e:
                db.session.rollback()
                flash(f"Failed to send email: {str(e)}", 'error')

        elif contact_method == "sms":
            message = Message(
                username=username,
                phone_number=phone_number,
                email='',
                host=host_obj,
                message_type='SMS',
                signature=signature,
                sender=current_user
            )

            db.session.add(message)
            db.session.commit()

            message_body = f"Farmer Name: {username}\nEmail: {email}\nHost: {host_obj.value}\nRemark: {signature}"
            payload = {
                'auth_token': '04a5bf6ec8718ea81d1edfc041f01abcbfa698a95a62356eecbcac8beaa3bf64',
                'to': phone_number,
                'text': message_body
            }
            response = requests.post(SMS_API_ENDPOINT, data=payload)
            if response.status_code == 200:
                flash("SMS sent successfully!", 'success')
            else:
                flash(f"Failed to send SMS. {response.text}", 'error')
            return redirect(url_for('dashboards.send_message'))

    return render_template('unified_message_form.html', form=form, hosts=hosts)


@dashboards.route('/get_recommended_signatures', methods=['GET'])
@login_required
def get_recommended_signatures():
    host_id = request.args.get('host_id')
    if host_id:
        recommended_signatures = Signature.query.filter_by(
            host_id=host_id).all()
        signature_data = [{'id': sig.id, 'text': sig.recommended_text}
                          for sig in recommended_signatures]
        return jsonify(signature_data)

    return jsonify([]), 400


@dashboards.route('/display_and_download/<int:form_id>', methods=['GET'])
@login_required
def display_and_download(form_id):
    form_entry = PlantDiagnosticForm.query.get_or_404(form_id)

    labcenter = LabCenter.query.get(form_entry.labcenter_id)
    diagnostictest = DiagnosticTest.query.get(form_entry.diagnostictest_id)
    suspectedproblem = SuspectedProblem.query.get(
        form_entry.suspectedproblem_id)
    host = Host.query.get(form_entry.host_id)
    samplematerialssubmitted = SampleMaterialsSubmitted.query.get(
        form_entry.samplematerialssubmitted_id)
    district = District.query.get(form_entry.district_id)
    provincestate = ProvinceState.query.get(form_entry.provincestate_id)
    diagnosisname = DiagnosisName.query.get(form_entry.diagnosisname_id)
    genus = Genus.query.get(form_entry.genus_id)
    genusspecies = GenusSpecies.query.get(form_entry.genusspecies_id)
    genussubspecies = GenusSubSpecies.query.get(form_entry.genussubspecies_id)
    genuslabmethods = GenusLabMethods.query.get(form_entry.genuslabmethods_id)
    nematode = Nematode.query.get(form_entry.nematode_id)
    nematodespecies = NematodeSpecies.query.get(form_entry.nematodespecies_id)
    nematodesubspecies = NematodeSubSpecies.query.get(
        form_entry.nematodesubspecies_id)
    nematodeextraction = NematodeExtraction.query.get(
        form_entry.nematodeextraction_id)

    return render_template('display_and_download.html',
                           form=form_entry,
                           labcenter=labcenter,
                           diagnostictest=diagnostictest,
                           suspectedproblem=suspectedproblem,
                           host=host,
                           samplematerialssubmitted=samplematerialssubmitted,
                           district=district,
                           provincestate=provincestate,
                           diagnosisname=diagnosisname,
                           genus=genus,
                           genusspecies=genusspecies,
                           genussubspecies=genussubspecies,
                           genuslabmethods=genuslabmethods,
                           nematode=nematode,
                           nematodespecies=nematodespecies,
                           nematodesubspecies=nematodesubspecies,
                           nematodeextraction=nematodeextraction
                           )


@dashboards.route('/media/<filename>')
def serve_media(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


def save_image(image):

    filename = secure_filename(image.filename)

    if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
        os.makedirs(current_app.config['UPLOAD_FOLDER'])

    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    return os.path.join('media', filename)


@dashboards.route('/create_admin', methods=['GET', 'POST'])
@superuser_required
def create_admin():
    message = None
    labcenters = LabCenter.query.all()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        labcenter_id = request.form['department']
        labcenter = LabCenter.query.get(labcenter_id)
        phone_number = request.form['phone_number']
        password = request.form['password']

        if not labcenter:
            message = 'Please select Lab center'
            return render_template('create_admin.html', message=message)

        if not username.isalpha():
            message = 'Username should only contain letters.'
            return render_template('create_admin.html', message=message)

        import re
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            message = 'Invalid email address.'
            return render_template('create_admin.html', message=message)

        if not (phone_number.isdigit() and len(phone_number) == 10):
            message = 'Phone number should be 10 digits.'
            return render_template('create_admin.html', message=message)

        existing_user = User.query.filter((User.email == email) | (
            User.phone_number == phone_number)).first()
        if existing_user:
            message = 'An account already exists with this email or phone number. Please choose different credentials.'
            return render_template('create_admin.html', message=message)

        new_admin = User(username=username, email=email,
                         labcenter=labcenter, phone_number=phone_number, password=password, role='admin')

        new_admin.password = password
        db.session.add(new_admin)
        db.session.commit()
        return redirect(url_for('dashboards.dashboard'))

    return render_template('create_admin.html', message=message, labcenters=labcenters)


@dashboards.route('/api/labcenters', methods=['GET'])
@superuser_required
def get_labcenters():
    labcenters = LabCenter.query.all()
    return jsonify([{'id': lc.id, 'value': lc.value} for lc in labcenters])


@dashboards.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    message = None
    if request.method == 'POST':
        email = request.form['email']
        phone_number = request.form['phone_number']
        username = request.form['username']
        password = request.form['password']

        if not username.isalpha():
            message = 'Username should only contain letters.'
            return render_template('create_user.html', message=message)

        if not (phone_number.isdigit() and len(phone_number) == 10):
            message = 'Phone number should be 10 digits.'
            return render_template('create_user.html', message=message)

        existing_user = User.query.filter((User.email == email) | (
            User.phone_number == phone_number)).first()
        if existing_user:
            message = 'An account already exists with this email or phone number. Please choose different credentials.'
            return render_template('create_user.html', message=message)

        new_user = User(email=email, phone_number=phone_number,
                        username=username, role='user', creator_id=current_user.id)
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('dashboards.dashboard'))

    return render_template('create_user.html', message=message)


@dashboards.route('/dashboard')
@login_required
def dashboard():

    forms = PlantDiagnosticForm.query.filter_by(user_id=current_user.id).all()
    total_forms_filled = PlantDiagnosticForm.query.count()
    admins = User.query.filter_by(role='admin').all()
    users = User.query.filter_by(role='user').all()
    total_admins = User.query.filter_by(role='admin').count()
    total_users = User.query.filter_by(role='user').count()
    forms_user = PlantDiagnosticForm.query.filter_by(
        user_id=current_user.id).count()

    return render_template('dashboard.html', forms=forms, admins=admins, users=users, total_admins=total_admins, total_users=total_users, total_forms_filled=total_forms_filled, forms_user=forms_user)


@dashboards.route('/get-users-for-admin/<int:admin_id>')
@login_required
def get_users_for_admin(admin_id):

    users = User.query.filter_by(creator_id=admin_id).all()

    users_data = [{
        'id': user.id,
        'username': user.username,
        'phone_number': user.phone_number,
        'email': user.email,
        'is_active': user.is_active
    } for user in users]

    return jsonify({'users': users_data})


@dashboards.route("/download_excel_admin")
def download_excel_admin():

    form_query = PlantDiagnosticForm.query.all()

    forms = [
        {
            'formID': form.id,

            'fieldReferenceId': getattr(form, 'field_reference_id', np.nan),
            'diagnosisName': getattr(form.diagnosisname, 'value', np.nan),
            'labCenter': getattr(form.labcenter, 'value', np.nan),
            'date': form.date.strftime('%Y-%m-%d') if form.date else np.nan,
            'diagnosticTest': getattr(form.diagnostictest, 'value', np.nan),
            'suspectedProblem': getattr(form.suspectedproblem, 'value', np.nan),
            'host': getattr(form.host, 'value', np.nan),
            'sampleSource': getattr(form, 'sample_source', np.nan),



            'sampleCollectedDate': form.sample_collected_date.strftime('%Y-%m-%d') if form.sample_collected_date else np.nan,
            'physicalSampleReceivedDate': form.physical_sample_received_date.strftime('%Y-%m-%d') if form.physical_sample_received_date else np.nan,
            'district': getattr(form.district, 'value', np.nan),
            'provinceState': getattr(form.provincestate, 'value', np.nan),
            'zipCode': getattr(form, 'zip_code', np.nan),
            'altitude': getattr(form, 'altitude', np.nan),
            'latitude': getattr(form, 'latitude', np.nan),
            'longitude': getattr(form, 'longitude', np.nan),
            'genus': getattr(form.genus, 'value', np.nan),
            'genusSpecies': getattr(form.genusspecies, 'value', np.nan),
            'genusSubspecies': getattr(form.genussubspecies, 'value', np.nan),
            'genusLabMethods': getattr(form.genuslabmethods, 'value', np.nan),
            'nematode': getattr(form.nematode, 'value', np.nan),
            'nematodeSpecies': getattr(form.nematodespecies, 'value', np.nan),
            'nematodeSubspecies': getattr(form.nematodesubspecies, 'value', np.nan),
            'nematodeExtraction': getattr(form.nematodeextraction, 'value', np.nan),
            'insectName': getattr(form, 'insect_name', np.nan),
            'causingDamageInsect': getattr(form, 'causing_damage_insect', np.nan),
            'insectNotes': getattr(form, 'insect_notes', np.nan),
            'diseaseName': getattr(form, 'disease_name', np.nan),
            'causingDamageDisease': getattr(form, 'causing_damage_disease', np.nan),
            'diseaseNotes': getattr(form, 'disease_notes', np.nan),
            'weedsName': getattr(form, 'weeds_name', np.nan),
            'causingDamageWeeds': getattr(form, 'causing_damage_weeds', np.nan),
            'weedsNotes': getattr(form, 'weeds_notes', np.nan),
            'plantPopulation': getattr(form, 'plant_population', np.nan),
            'goodPlants': getattr(form, 'good_plants', np.nan),
            'remark': getattr(form, 'signature', np.nan),
            'status': getattr(form, 'status', np.nan),

        }
        for form in form_query


    ]

    df = pd.DataFrame(forms)

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1')
    output.seek(0)

    return send_file(output, download_name="data.xlsx", as_attachment=True, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@dashboards.route('/get_user_forms/<int:user_id>', methods=['GET'])
def get_user_forms(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    forms = PlantDiagnosticForm.query.filter_by(user_id=user_id).all()

    forms_list = [{
        "id": form.id,

        "fieldreferenceid": form.field_reference_id,
        "diagnosisname": form.diagnosisname.value,
        "labcenter": form.labcenter.value,
        "date": form.date.strftime('%Y-%m-%d'),

        "status": form.status,
        "insect_name": form.insect_name,
        "disease_name": form.disease_name,
        "weeds_name": form.weeds_name,
        "image_path_insect": form.image_path_insect,
        "image_path_disease": form.image_path_disease,
        "image_path_weeds": form.image_path_weeds,

    } for form in forms]

    return jsonify(forms_list)


@dashboards.route('/get_user_all_forms', methods=['GET'])
@login_required
def get_user_all_forms():

    user_id = current_user.id

    user = User.query.get(user_id)

    if not user:
        return jsonify(error="User not found."), 404

    forms = [
        {
            'formID': form.id,
            "fieldreferenceid": form.field_reference_id,
            'diagnosisname': form.diagnosisname.value,
            'labcenter': form.labcenter.value,
            'date': form.date.strftime('%Y-%m-%d'),
            'status': form.status,
            "insect_name": form.insect_name,
            "disease_name": form.disease_name,
            "weeds_name": form.weeds_name,
            "image_path_insect": form.image_path_insect,
            "image_path_disease": form.image_path_disease,
            "image_path_weeds": form.image_path_weeds,
        }
        for form in user.forms
    ]

    return jsonify(forms)


@dashboards.route("/download_excel")
def download_excel():

    user_id = current_user.id

    user = User.query.get(user_id)

    if not user:
        return jsonify(error="User not found."), 404

    forms = [
        {
            'formID': form.id,
            "fieldReferenceId": form.field_reference_id,
            'diagnosisName': form.diagnosisname.value,
            'labCenter': form.labcenter.value,
            'date': form.date.strftime('%Y-%m-%d'),
            'diagnosticTest': form.diagnostictest.value,
            'suspectedProblem': form.suspectedproblem.value,
            'host': form.host.value,
            'sampleSource': form.sample_source,

            'sampleCollectedDate': form.sample_collected_date.strftime('%Y-%m-%d'),
            'physicalSampleReceivedDate': form.physical_sample_received_date.strftime('%Y-%m-%d'),
            'district': form.district.value,
            'provinceState': form.provincestate.value,
            'zipCode': form.zip_code,
            'altitude': form.altitude,
            'latitude': form.latitude,
            'longitude': form.longitude,
            'genus': form.genus.value,
            'genusSpecies': form.genusspecies.value,
            'genusSubspecies': form.genussubspecies.value,
            'genusLabMethods': form.genuslabmethods.value,
            'nematode': form.nematode.value,
            'nematodeSpecies': form.nematodespecies.value,
            'nematodeSubspecies': form.nematodesubspecies.value,
            'nematodeExtraction': form.nematodeextraction.value,




            "insectName": form.insect_name,
            "casuingDamageInsect": form.causing_damage_insect,
            "insectNotes": form.insect_notes,



            "diseaseName": form.disease_name,
            "causingDamageDisease": form.causing_damage_disease,
            "diseaseNotes": form.disease_notes,


            "weedsName": form.weeds_name,
            "causingDamageWeeds": form.causing_damage_weeds,
            "weedsNotes": form.weeds_notes,
            "plantPopulation": form.plant_population,
            "goodPlants": form.good_plants,
            "remark": form.signature,

            'status': form.status
        }
        for form in user.forms
    ]

    df = pd.DataFrame(forms)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1')
    output.seek(0)

    return send_file(output, download_name="data.xlsx", as_attachment=True, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@dashboards.route('/new_form', methods=['GET', 'POST'])
@dashboards.route('/new_form/<int:form_id>', methods=['GET', 'POST'])
@login_required
def new_form(form_id=None):
    entry = None
    if form_id:

        entry = PlantDiagnosticForm.query.get_or_404(form_id)
    form = PlantDiagnosticFormForm(obj=entry)

    specimenpreserveds = SpecimenPreserved.query.all()
    specimenpreserved_choices = [(specimenpreserved.id, specimenpreserved.value)
                                 for specimenpreserved in specimenpreserveds]
    form.specimenpreserved.choices = specimenpreserved_choices

    storageconditions = StorageCondition.query.all()
    storagecondition_choices = [(storagecondition.id, storagecondition.value)
                                for storagecondition in storageconditions]
    form.storagecondition.choices = storagecondition_choices

    labcenters = LabCenter.query.all()
    labcenter_choices = [(labcenter.id, labcenter.value)
                         for labcenter in labcenters]
    form.labcenter.choices = labcenter_choices

    diagnostictests = DiagnosticTest.query.all()
    diagnostictest_choices = [(diagnostictest.id, diagnostictest.value)
                              for diagnostictest in diagnostictests]
    form.diagnostictest.choices = diagnostictest_choices

    suspectedproblems = SuspectedProblem.query.all()
    suspectedproblem_choices = [(suspectedproblem.id, suspectedproblem.value)
                                for suspectedproblem in suspectedproblems]
    form.suspectedproblem.choices = suspectedproblem_choices

    hosts = Host.query.all()
    host_choices = [(host.id, host.value) for host in hosts]
    form.host.choices = host_choices

    samplematerialssubmitteds = SampleMaterialsSubmitted.query.all()
    samplematerialssubmitted_choices = [(samplematerialssubmitted.id, samplematerialssubmitted.value)
                                        for samplematerialssubmitted in samplematerialssubmitteds]
    form.samplematerialssubmitted.choices = samplematerialssubmitted_choices

    districts = District.query.all()
    district_choices = [(district.id, district.value)
                        for district in districts]
    form.district.choices = district_choices

    provincestates = ProvinceState.query.all()
    provincestate_choices = [(provincestate.id, provincestate.value)
                             for provincestate in provincestates]
    form.provincestate.choices = provincestate_choices

    diagnosisnames = DiagnosisName.query.all()
    diagnosisname_choices = [(diagnosisname.id, diagnosisname.value)
                             for diagnosisname in diagnosisnames]
    form.diagnosisname.choices = diagnosisname_choices

    genuss = Genus.query.all()
    genus_choices = [(genus.id, genus.value) for genus in genuss]
    form.genus.choices = genus_choices

    genusspeciess = GenusSpecies.query.all()
    genusspecies_choices = [(genusspecies.id, genusspecies.value)
                            for genusspecies in genusspeciess]
    form.genusspecies.choices = genusspecies_choices

    genussubspeciess = GenusSubSpecies.query.all()
    genussubspecies_choices = [(genussubspecies.id, genussubspecies.value)
                               for genussubspecies in genussubspeciess]
    form.genussubspecies.choices = genussubspecies_choices

    genuslabmethodss = GenusLabMethods.query.all()
    genuslabmethods_choices = [(genuslabmethods.id, genuslabmethods.value)
                               for genuslabmethods in genuslabmethodss]
    form.genuslabmethods.choices = genuslabmethods_choices

    nematodes = Nematode.query.all()
    nematode_choices = [(nematode.id, nematode.value)
                        for nematode in nematodes]
    form.nematode.choices = nematode_choices

    nematodespeciess = NematodeSpecies.query.all()
    nematodespecies_choices = [(nematodespecies.id, nematodespecies.value)
                               for nematodespecies in nematodespeciess]
    form.nematodespecies.choices = nematodespecies_choices

    nematodesubspeciess = NematodeSubSpecies.query.all()
    nematodesubspecies_choices = [(nematodesubspecies.id, nematodesubspecies.value)
                                  for nematodesubspecies in nematodesubspeciess]
    form.nematodesubspecies.choices = nematodesubspecies_choices

    nematodeextractions = NematodeExtraction.query.all()
    nematodeextraction_choices = [(nematodeextraction.id,  nematodeextraction.value)
                                  for nematodeextraction in nematodeextractions]
    form.nematodeextraction.choices = nematodeextraction_choices

    if form.validate_on_submit():
        if not entry and not form_id:
            entry = PlantDiagnosticForm(user_id=current_user.id)
            db.session.add(entry)
        elif form_id and not entry:
            entry = PlantDiagnosticForm.query.get_or_404(
                form_id)

        entry.labcenter_id = form.labcenter.data

        entry.date = form.date.data
        entry.specimenpreserved_id = form.specimenpreserved.data
        entry.storagecondition_id = form.storagecondition.data

        entry.specifem_id = form.specifem_id.data

        entry.diagnostictest_id = form.diagnostictest.data

        entry.suspectedproblem_id = form.suspectedproblem.data

        entry.host_id = form.host.data

        entry.field_reference_id = form.field_reference_id.data

        entry.sample_source = form.sample_source.data

        entry.samplematerialssubmitted_id = form.samplematerialssubmitted.data

        entry.sample_collected_date = form.sample_collected_date.data

        entry.physical_sample_received_date = form.physical_sample_received_date.data

        entry.district_id = form.district.data

        entry.provincestate_id = form.provincestate.data

        entry.zip_code = form.zip_code.data
        entry.altitude = form.altitude.data
        entry.latitude = form.latitude.data
        entry.longitude = form.longitude.data

        entry.diagnosisname_id = form.diagnosisname.data

        entry.genus_id = form.genus.data

        entry.genusspecies_id = form.genusspecies.data

        entry.genussubspecies_id = form.genussubspecies.data

        entry.genuslabmethods_id = form.genuslabmethods.data

        entry.nematode_id = form.nematode.data

        entry.nematodespecies_id = form.nematodespecies.data

        entry.nematodesubspecies_id = form.nematodesubspecies.data

        entry.nematodeextraction_id = form.nematodeextraction.data

        entry.insect_name = form.insect_name.data
        entry.causing_damage_insect = form.causing_damage_insect.data
        entry.insect_notes = form.insect_notes.data

        if form.image_path_insect.data:

            entry.image_path_insect = save_image(
                form.image_path_insect.data)

        entry.disease_name = form.disease_name.data
        entry.causing_damage_disease = form.causing_damage_disease.data
        entry.disease_notes = form.disease_notes.data

        if form.image_path_disease.data:
            entry.image_path_disease = save_image(form.image_path_disease.data)

        entry.weeds_name = form.weeds_name.data
        entry.causing_damage_weeds = form.causing_damage_weeds.data
        entry.weeds_notes = form.weeds_notes.data

        if form.image_path_weeds.data:
            entry.image_path_weeds = save_image(form.image_path_weeds.data)

        entry.plant_population = form.plant_population.data
        entry.good_plants = form.good_plants.data
        entry.signature = form.signature.data
        entry.status = form.status.data

        if "temp_save" in request.form:
            entry.status = "Saved"
            flash('Your data has been saved temporarily.', 'info')
        elif "finish" in request.form:
            entry.status = "Completed"
            flash('Your data has been saved and completed.', 'success')

        db.session.commit()

        if entry.status == "Saved":
            return redirect(url_for('dashboards.new_form', form_id=entry.id))
        else:
            return redirect(url_for('dashboards.dashboard'))

    # Prefill the labcenter
    if not form_id:
        if current_user.creator:
            form.labcenter.data = current_user.creator.labcenter_id

    return render_template('new_form.html', form=form, form_id=form_id)


@dashboards.route('/edit_form/<int:form_id>', methods=['GET', 'POST'])
def edit_form(form_id):
    entry = PlantDiagnosticForm.query.get_or_404(form_id)
    form = PlantDiagnosticFormForm(obj=entry)

    specimenpreserveds = SpecimenPreserved.query.all()
    specimenpreserved_choices = [(specimenpreserved.id, specimenpreserved.value)
                                 for specimenpreserved in specimenpreserveds]
    form.specimenpreserved.choices = specimenpreserved_choices

    storageconditions = StorageCondition.query.all()
    storagecondition_choices = [(storagecondition.id, storagecondition.value)
                                for storagecondition in storageconditions]
    form.storagecondition.choices = storagecondition_choices

    labcenters = LabCenter.query.all()
    labcenter_choices = [(labcenter.id, labcenter.value)
                         for labcenter in labcenters]
    form.labcenter.choices = labcenter_choices

    diagnostictests = DiagnosticTest.query.all()
    diagnostictest_choices = [(diagnostictest.id, diagnostictest.value)
                              for diagnostictest in diagnostictests]
    form.diagnostictest.choices = diagnostictest_choices

    suspectedproblems = SuspectedProblem.query.all()
    suspectedproblem_choices = [(suspectedproblem.id, suspectedproblem.value)
                                for suspectedproblem in suspectedproblems]
    form.suspectedproblem.choices = suspectedproblem_choices

    hosts = Host.query.all()
    host_choices = [(host.id, host.value) for host in hosts]
    form.host.choices = host_choices

    samplematerialssubmitteds = SampleMaterialsSubmitted.query.all()
    samplematerialssubmitted_choices = [(samplematerialssubmitted.id, samplematerialssubmitted.value)
                                        for samplematerialssubmitted in samplematerialssubmitteds]
    form.samplematerialssubmitted.choices = samplematerialssubmitted_choices

    districts = District.query.all()
    district_choices = [(district.id, district.value)
                        for district in districts]
    form.district.choices = district_choices

    provincestates = ProvinceState.query.all()
    provincestate_choices = [(provincestate.id, provincestate.value)
                             for provincestate in provincestates]
    form.provincestate.choices = provincestate_choices

    diagnosisnames = DiagnosisName.query.all()
    diagnosisname_choices = [(diagnosisname.id, diagnosisname.value)
                             for diagnosisname in diagnosisnames]
    form.diagnosisname.choices = diagnosisname_choices

    genuss = Genus.query.all()
    genus_choices = [(genus.id, genus.value) for genus in genuss]
    form.genus.choices = genus_choices

    genusspeciess = GenusSpecies.query.all()
    genusspecies_choices = [(genusspecies.id, genusspecies.value)
                            for genusspecies in genusspeciess]
    form.genusspecies.choices = genusspecies_choices

    genussubspeciess = GenusSubSpecies.query.all()
    genussubspecies_choices = [(genussubspecies.id, genussubspecies.value)
                               for genussubspecies in genussubspeciess]
    form.genussubspecies.choices = genussubspecies_choices

    genuslabmethodss = GenusLabMethods.query.all()
    genuslabmethods_choices = [(genuslabmethods.id, genuslabmethods.value)
                               for genuslabmethods in genuslabmethodss]
    form.genuslabmethods.choices = genuslabmethods_choices

    nematodes = Nematode.query.all()
    nematode_choices = [(nematode.id, nematode.value)
                        for nematode in nematodes]
    form.nematode.choices = nematode_choices

    nematodespeciess = NematodeSpecies.query.all()
    nematodespecies_choices = [(nematodespecies.id, nematodespecies.value)
                               for nematodespecies in nematodespeciess]
    form.nematodespecies.choices = nematodespecies_choices

    nematodesubspeciess = NematodeSubSpecies.query.all()
    nematodesubspecies_choices = [(nematodesubspecies.id, nematodesubspecies.value)
                                  for nematodesubspecies in nematodesubspeciess]
    form.nematodesubspecies.choices = nematodesubspecies_choices

    nematodeextractions = NematodeExtraction.query.all()
    nematodeextraction_choices = [(nematodeextraction.id,  nematodeextraction.value)
                                  for nematodeextraction in nematodeextractions]
    form.nematodeextraction.choices = nematodeextraction_choices

    # Set the default LabCenter when first loading the page (i.e., HTTP GET)
    if request.method == 'GET' and current_user.creator:
        form.labcenter.data = current_user.creator.labcenter_id

    if form.validate_on_submit():
        if not entry and not form_id:
            entry = PlantDiagnosticForm(user_id=current_user.id)
            db.session.add(entry)
        elif form_id and not entry:
            entry = PlantDiagnosticForm.query.get_or_404(
                form_id)

        entry.labcenter_id = form.labcenter.data

        entry.date = form.date.data

        entry.specifem_id = form.specifem_id.data

        entry.specimenpreserved_id = form.specimenpreserved.data
        entry.storagecondition_id = form.storagecondition.data

        entry.diagnostictest_id = form.diagnostictest.data

        entry.suspectedproblem_id = form.suspectedproblem.data

        entry.host_id = form.host.data

        entry.field_reference_id = form.field_reference_id.data

        entry.sample_source = form.sample_source.data

        entry.samplematerialssubmitted_id = form.samplematerialssubmitted.data

        entry.sample_collected_date = form.sample_collected_date.data

        entry.physical_sample_received_date = form.physical_sample_received_date.data

        entry.district_id = form.district.data

        entry.provincestate_id = form.provincestate.data

        entry.zip_code = form.zip_code.data
        entry.altitude = form.altitude.data
        entry.latitude = form.latitude.data
        entry.longitude = form.longitude.data

        entry.diagnosisname_id = form.diagnosisname.data

        entry.genus_id = form.genus.data

        entry.genusspecies_id = form.genusspecies.data

        entry.genussubspecies_id = form.genussubspecies.data

        entry.genuslabmethods_id = form.genuslabmethods.data

        entry.nematode_id = form.nematode.data

        entry.nematodespecies_id = form.nematodespecies.data

        entry.nematodesubspecies_id = form.nematodesubspecies.data

        entry.nematodeextraction_id = form.nematodeextraction.data

        entry.insect_name = form.insect_name.data
        entry.causing_damage_insect = form.causing_damage_insect.data
        entry.insect_notes = form.insect_notes.data

        if form.image_path_insect.data:

            entry.image_path_insect = save_image(
                form.image_path_insect.data)

        entry.disease_name = form.disease_name.data
        entry.causing_damage_disease = form.causing_damage_disease.data
        entry.disease_notes = form.disease_notes.data

        if form.image_path_disease.data:
            entry.image_path_disease = save_image(form.image_path_disease.data)

        entry.weeds_name = form.weeds_name.data
        entry.causing_damage_weeds = form.causing_damage_weeds.data
        entry.weeds_notes = form.weeds_notes.data

        if form.image_path_weeds.data:
            entry.image_path_weeds = save_image(form.image_path_weeds.data)

        entry.plant_population = form.plant_population.data
        entry.good_plants = form.good_plants.data
        entry.signature = form.signature.data
        entry.status = form.status.data

        if "temp_save" in request.form:
            entry.status = "Saved"
        elif "finish" in request.form:
            entry.status = "Completed"

        db.session.commit()
        flash('Your data has been updated.',
              'success' if entry.status == "Completed" else 'info')

        if entry.status == "Saved":
            return redirect(url_for('dashboards.edit_form', form_id=entry.id))

        return redirect(url_for('dashboards.dashboard'))

    return render_template('edit_form.html', form=form)


@dashboards.route('/chart')
@login_required
def chart_series():
    forms_per_day = db.session.query(func.date(PlantDiagnosticForm.date), func.count(
        PlantDiagnosticForm.id)).group_by(func.date(PlantDiagnosticForm.date)).all()

    dates = [item[0].strftime('%Y-%m-%d') for item in forms_per_day]
    counts = [item[1] for item in forms_per_day]
    return render_template('chart.html', dates=dates, counts=counts)


@dashboards.route('/toggle-user-active/<int:user_id>', methods=['POST'])
@login_required
def toggle_user_active(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active  # toggle the is_active status
    db.session.commit()
    return jsonify({'status': 'success', 'is_active': user.is_active})


@dashboards.route('/document', methods=['GET'])
def Document():
    return render_template('docs.html')
