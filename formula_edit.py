from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from flask_bootstrap import Bootstrap
from math import log, exp, floor
from decimal import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, RadioField, SelectField
from wtforms.validators import InputRequired, Email, Length
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy.engine import Engine
from sqlalchemy import event
import os
import psycopg2
import json

from wtforms_sqlalchemy.fields import QuerySelectField
#from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:////flask-application/building_user_login_system/start/database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
#conn = psycopg2.connect("host=hbcdm.ce9qkwq3sggt.us-east-1.rds.amazonaws.com dbname=hbcdm user=hbadmin password=hbaccess")
#cur = conn.cursor()
#conn = psycopg2.connect("host=hbcdm.ce9qkwq3sggt.us-east-1.rds.amazonaws.com dbname=hbcdm user=hbadmin password=hbaccess")
conn = psycopg2.connect("host=hbcdm.cdm9kks3s0wa.us-east-1.rds.amazonaws.com dbname=hbcdm user=hbadmin password=hbaccess")
cur = conn.cursor()



class TrustChoice(UserMixin, db.Model):
    trustchoiceid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    decision = db.Column(db.String(40))
    #trustchoices = db.relationship('TrustCalcForm', backref = 'trust_choice', lazy = 'dynamic')

class TrustCalcForm(UserMixin, db.Model):
    trustid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    radiology_images = db.Column(db.String(10))
    radiology_imaging_reports = db.Column(db.String(10))
    ekg = db.Column(db.String(10))
    progress_notes = db.Column(db.String(10))
    history_phy = db.Column(db.String(10))
    oper_report = db.Column(db.String(10))
    path_report = db.Column(db.String(10))
    lab_report = db.Column(db.String(10))
    photographs = db.Column(db.String(10))
    #ssn = db.Column(db.String(10))
    discharge_summaries = db.Column(db.String(10))
    health_care_billing = db.Column(db.String(10))
    consult = db.Column(db.String(10))
    medication = db.Column(db.String(10))
    emergency = db.Column(db.String(10))
    dental = db.Column(db.String(10))
    demographic = db.Column(db.String(10))
    question = db.Column(db.String(10))
    audiotape = db.Column(db.String(10))
    #other = db.Column(db.String(10))
    match = db.Column(db.String(10))
    mismatch = db.Column(db.String(10))
    undecided = db.Column(db.String(10))
    beta = db.Column(db.String(10))
    dirichlet = db.Column(db.String(10))
    status = db.Column(db.String(10))
    ownerid= db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
   # trustchoiceid = db.Column(db.Integer, db.ForeignKey('trust_choice.trustchoiceid'), nullable=False)



def choice_irb():
    return IrbInfo.query

def choice_trustcalc():
    return TrustChoice.query


def choice_dataset():
    return Dataset.query



class CreateTrustCalcForm(FlaskForm):
    #CaStatus = QuerySelectField('Enter your choice', choices=[('Yes', 'Yes'), ('No', 'No'), ('Uncertain', 'Uncertain')])
     irb_id = QuerySelectField(query_factory=choice_irb, allow_blank=True, get_label = 'irb_id')
     radiology_images = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     radiology_imaging_reports = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     ekg = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     progress_notes = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     history_phy = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     oper_report = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     path_report = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     lab_report = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     photographs  = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     #ssn = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     discharge_summaries = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     health_care_billing = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     consult = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     medication = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     emergency = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     dental = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     demographic = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     question = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     audiotape = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')
     #other = QuerySelectField(query_factory=choice_trustcalc, allow_blank=True, get_label = 'decision')



def submithipaa():
    print(current_user.username)
    form = CreateTrustCalcForm()
    irb_id = form.irb_id.data.irb_id

    radiology_images = form.radiology_images.data.decision
    radiology_imaging_reports = form.radiology_imaging_reports.data.decision
    ekg = form.ekg.data.decision
    progress_notes = form.progress_notes.data.decision
    history_phy = form.history_phy.data.decision
    oper_report = form.oper_report.data.decision
    path_report = form.path_report.data.decision
    lab_report = form.lab_report.data.decision
    photographs = form.photographs.data.decision
     #ssn = form.ssn.data.decision
        #ssn = form.ssn.data.decision
    discharge_summaries = form.discharge_summaries.data.decision
    health_care_billing = form.health_care_billing.data.decision
    consult = form.consult.data.decision
    medication = form.medication.data.decision
    emergency  = form.emergency.data.decision
    dental = form.dental.data.decision
    demographic = form.demographic.data.decision
    question = form.question.data.decision
    audiotape = form.audiotape.data.decision
    #other = form.other.data.decision


    templist = [radiology_images, radiology_imaging_reports, ekg, progress_notes, history_phy, oper_report, path_report, lab_report, photographs, discharge_summaries, health_care_billing, consult, medication, emergency, dental, demographic, question, audiotape]
    if (current_user.username == 'internaluser'):
        userrole = 'internal_user'
    elif (current_user.username == 'externaluser'):
        userrole = 'external_user'


    postgreSQL_select_Query = "select * from data_policy_domain"
    cur.execute(postgreSQL_select_Query, [irb_id])
    resultset = cur.fetchone()
    print('resultset is',resultset)
    d = resultset[1:]



     
    for a,b in zip(templist, d):
        if (a == 'Yes' and b==1):
            print("si", 1)
        elif (a == 'No' and b == '0'):
            si= 1
        elif (a == 'No' and b == '1'):
            si= 1
        else:
            si= 0
    N=18

    #complaince_score
    complaince_score=si*10/N;
    print('complaince_score is', complaince_score)
    print(Ramya)        







