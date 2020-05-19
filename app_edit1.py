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
import sqlite3
import requests
import csv

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
#conn = psycopg2.connect("host=hbcdm.cdm9kks3s0wa.us-east-1.rds.amazonaws.com dbname=hbcdm user=hbadmin password=hbaccess")
conn = psycopg2.connect("host=hbcdm.cpnsaiphh4ed.us-east-1.rds.amazonaws.com dbname=hbcdm user=hbadmin password=hbaccess")

cur = conn.cursor()
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    requests = db.relationship('RequestForm', backref = 'user', lazy = 'dynamic')

class Dataset(UserMixin, db.Model):
    datasetid = db.Column(db.Integer, primary_key=True)
    nameset = db.Column(db.String(40))
    dataset_risk = db.Column(db.Integer)
    accept_risk = db.Column(db.Integer)
    datasets = db.relationship('RequestForm', backref = 'dataset', lazy = 'dynamic')

class RequestForm(UserMixin, db.Model):
    requestid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    #ownerid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    requestname = db.Column(db.String(40))
    requestDescription = db.Column(db.String(40))
    use = db.Column(db.String(40))
    store = db.Column(db.String(40))
    longdata = db.Column(db.String(40))
    soondata = db.Column(db.String(40))
    typeofdata = db.Column(db.String(40))
    status = db.Column(db.String(40))
    risk_level = db.Column(db.String(40))
    #requestid= db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    ownerid= db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False) 
    datasetid =db.Column(db.Integer, db.ForeignKey('dataset.datasetid'), nullable=False)
    #requests = db.relationship('RequestForm', backref = 'user', lazy = True)
    #datasets = db.relationship('RequestForm', backref = 'dataset', lazy = True)

class trial(UserMixin, db.Model):
    data_set_name=db.Column(db.String(40),primary_key = True)


class IrbInfo(UserMixin, db.Model):
    irbunique = db.Column(db.Integer, primary_key = True, autoincrement = True)
    irb_id = db.Column(db.String(10))

class ItemInfo(UserMixin, db.Model):
    itemid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    itemname = db.Column(db.String(40))
    itemunique = db.Column(db.String(10))

class TrustChoice(UserMixin, db.Model):
    trustchoiceid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    decision = db.Column(db.String(40))
    #trustchoices = db.relationship('TrustCalcForm', backref = 'trust_choice', lazy = 'dynamic')

class TrustCalcForm(UserMixin, db.Model):
    trustid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    #requestid = db.Column(db.Integer, db.ForeignKey('request_form.requestid'), nullable=False)
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
    compliance =db.Column(db.Integer,nullable=False)
    match = db.Column(db.String(10))
    mismatch = db.Column(db.String(10))
    undecided = db.Column(db.String(10))
    #beta = db.Column(db.String(10))
    #dirichlet = db.Column(db.String(10))
    status = db.Column(db.String(10))
    ownerid= db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
   # trustchoiceid = db.Column(db.Integer, db.ForeignKey('trust_choice.trustchoiceid'), nullable=False)
    requestid= db.Column(db.Integer, db.ForeignKey('request_form.requestid'),nullable=False)

class IdentifierCalcForm(UserMixin, db.Model):
    identifier = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(10))
    address = db.Column(db.String(10))
    elements_of_dates = db.Column(db.String(10))
    telephone_numbers = db.Column(db.String(10))
    fax_numbers = db.Column(db.String(10))
    email_address = db.Column(db.String(10))
    ssn = db.Column(db.String(10))
    medical_record_no = db.Column(db.String(10))
    health_plan = db.Column(db.String(10))
    account_no =  db.Column(db.String(10))
    certificate_or_license = db.Column(db.String(10))
    any_vehicle = db.Column(db.String(10))
    web_url =db.Column(db.String(10))
    ip_address = db.Column(db.String(10))
    biometric_identifier = db.Column(db.String(10))
    photographic_image = db.Column(db.String(10))
    any_other_characteristics = db.Column(db.String(10))
    ownerid= db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    
#class SelectFieldtypedata(db.Model):
#    datatype = db.Column(db.String(40))

#class ChoiceOpts(FlaskForm):
#    opts = QuerySelectField(query_factory = choice_dataset, allow_blank =True)


def choice_irb():
    return IrbInfo.query


def choice_request():
    return RequestForm.query

def choice_trustcalc():
    return TrustChoice.query


def choice_dataset():
    return Dataset.query


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()



#def choice_typeofdata():
#    return SelectFieldtypedata.query

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length( max=45)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])

class FeedbackForm(FlaskForm):
    receival = StringField('Did you receive the data', validators=[InputRequired(), Length(min=4, max=45)])
    Input =StringField('Are you satisfied with the data', validators=[InputRequired(), Length(min=4, max=40)])
    time_taken=StringField('How much time did it take to receive the data', validators=[InputRequired(), Length(min=4, max=40)])
    feedback_user=StringField('Rate the data provider with : positive,negative,neutral', validators=[InputRequired(), Length(min=4, max=40)])


class CreateRequestForm(FlaskForm):
    requestname = StringField('Title', validators=[InputRequired(), Length(min=4, max=15)])
    requestDescription =  StringField('Description', validators=[InputRequired(), Length(min=4, max=40)])
    #datasetname =StringField('Which dataset are you trying to access', validators=[InputRequired(), Length(min=4, max=60)]) 
    datasetname = QuerySelectField(query_factory=choice_dataset, allow_blank=True, get_label = 'nameset')
    use =StringField('How will you use the data', validators=[InputRequired(), Length(min=4, max=40)])
    store=StringField('How will you store data', validators=[InputRequired(), Length(min=4, max=40)])
    longdata=StringField('How long data needs to be accessible', validators=[InputRequired(), Length(min=4, max=40)])
    soondata=StringField('How soon data needs to be accessible', validators=[InputRequired(), Length(min=4, max=40)])
    #dstype = QuerySelectField(query_factory=choice_typeofdata, allow_blank=True)
    typeofdata=StringField('What type of data would you like to receive', validators=[InputRequired(), Length(min=4, max=40)])

class CreateTrustCalcForm(FlaskForm):
    #CaStatus = QuerySelectField('Enter your choice', choices=[('Yes', 'Yes'), ('No', 'No'), ('Uncertain', 'Uncertain')])i
     irb_id = QuerySelectField(query_factory=choice_irb, allow_blank=True, get_label = 'irb_id')
     #requestid = QuerySelectField(query_factory=choice_request, allow_blank=True, get_label = 'requestid')
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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user, remember=form.remember.data)
                return redirect(url_for('intro'))
        return '<h1> Invalid Username or password </h1>'

        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        flash("Registration successful!", "success")
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return '<h1> New user has been registered</h1>'

        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/intro')
@login_required
def intro():
    return render_template('intro.html')


@app.route('/dashboard/', methods=['GET','POST'])
@login_required

def dashboard():
    #conn = psycopg2.connect("host=hbcdm.ce9qkwq3sggt.us-east-1.rds.amazonaws.com dbname=hbcdm user=hbadmin password=hbaccess")
    cur = conn.cursor()
    
    #result =cur.execute("SELECT dataset_risk FROM data_catalog where 'dataset_name' = %s", [datasetname])
    #stmt = "SELECT * FROM data_catalog WHERE dataset_name = %s"
   # cur.execute('SELECT * FROM data_catalog where "dataset_name" = %s', [datasetname])
    #resulset = cur.fetchone()
    #cur.execute('SELECT * FROM data_catalog where data_catalog.dataset_name = "datasetname" ')
    #resulset = cur.fetchall()
    cur.execute('SELECT * FROM data_catalog')
    resultset = cur.fetchall()
    f = open("requestid.txt","r")
    requestid_domain=f.read()
    
    #requestid_domain = session.get('requestId')
    get_data_params = {"requestId":str(requestid_domain)}
    result_get = requests.get("http://3.81.13.0:3000/api/Dataset", params=get_data_params)
    print("Final Result",result_get.content)
    b=result_get.content
    b =json.loads(b)
    app_req = [ x for x in b if x['decision'] == 'approved' and x['last_requester'] == 'resource:org.honestchain.User#'+str(current_user.username)]
    deny_req = [ x for x in b if x['decision'] == 'denied'  and x['last_requester'] == 'resource:org.honestchain.User#'+str(current_user.username)]
    manual_req = [x for x in b if x['decision'] == 'manual approval required' and x['last_requester'] == 'resource:org.honestchain.User#'+str(current_user.username)]
    #rows = cur.rowcount
    #query = cur.query

    #print('Rows: ', rows)
    #print('Query: ', query)

    #cur.close()


    #conn.close()
    

    pendingreq_info = RequestForm.query.filter_by(status= 'pending').all()
    approvedreq_info = RequestForm.query.filter_by(status= 'approved').all()
    denyreq_info = RequestForm.query.filter_by(status= 'denied').all()
    #b=b
    for i in pendingreq_info:
        print("pending request id is",i.requestid)

    
   # if(current_user.username == 'Admin'):
    #    return render_template('dashboard_admin.html',name=current_user.username, pending_req= pending_req, approvedreq_info= approvedreq_info, denyreq_info=denyreq_info, resultset=resultset)
       

        #apprInternal_info = RequestForm.query.filter_by(ownerid=current_user.id ,status = 'approved').all()
        #pendingreq_info = RequestForm.query.filter_by(ownerid=current_user.id ,status = 'pending').all()
        #deniedInternal_info = RequestForm.query.filter_by(ownerid=current_user.id ,status = 'denied').all()
        #for i in pendingreq_info: 
           # print("Request Id is ",i.requestid)
            #print("Internal user approved request is ",i.requestname)
        
    return render_template('request_status.html',name = current_user.username, b=b, app_req = app_req, deny_req = deny_req, manual_req = manual_req)
        
        #return render_template('dashboard.html', name = current_user.username, apprInternal_info= apprInternal_info, pendingreq_info=pendingreq_info, deniedInternal_info = deniedInternal_info, resultset = resultset)
        #return render_template('dashboard.html', pendingreq_info=pendingreq_info, apprInternal_info=apprInternal_info, deniedInternal_info=deniedInternal_info,data=data,b=b,requestid_domain=requestid_domain,len=len(b),a=a,c=c,d=d,e=e, app_req = app_req, deny_req = deny_req, manual_req = manual_req, reqid_table = reqid_table)
    
    #else:
        #print('external user dashboard')
        #apprInternal_info = RequestForm.query.filter_by(ownerid=current_user.id ,status = 'approved').all()
        #print('Id for external user is Hi',current_user.id)
        #request_info = RequestForm.query.filter_by(ownerid=current_user.id ,status = 'pending').all()
        #deniedInternal_info = RequestForm.query.filter_by(ownerid=current_user.id ,status = 'denied').all()
        #for i in apprInternal_info:
         #   print("Internal user approved request is ",i.requestname)
        #return render_template('dashboard_external.html', name = current_user.username, apprInternal_info= apprInternal_info, pendingreq_info=pendingreq_info, deniedInternal_info = deniedInternal_info, resultset = resultset)
#@app.route('/dashboard_admin')
#@login_required
#def dashboad_admin():
 #   return render_template('dashboard_admin.html', name = current_user.username)

@app.route('/logout') 
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/hipaaform/<requestid_domain>/<dataset_id_final>/<dataset_risk>', methods=['GET','POST'])
def hipaaform(requestid_domain,dataset_id_final,dataset_risk):
    print(requestid_domain)
    print(dataset_id_final)     
    print('in trust form')
    form = CreateTrustCalcForm()
    if form.validate_on_submit():
        print('Form validated')
    else:
        print(form.errors)
    return render_template('example2.html',form=form,requestid_domain=requestid_domain,dataset_id_final=dataset_id_final,dataset_risk=dataset_risk)


@app.route('/pendrequest', methods=['GET','POST'])
def pendrequest():
    print('in trust form')
    form = CreateTrustCalcForm()
    if form.validate_on_submit():
        print('Form validated')
    else:
        print(form.errors)
    return render_template('example2.html',form=form)

@app.route('/submithipaaform/<requestid_domain>/<dataset_id_final>/<dataset_risk>', methods=['GET','POST'])
def submithipaaform(requestid_domain,dataset_id_final,dataset_risk):
     print(current_user.username)
     print(requestid_domain)
     #print('global variable value is',requestid_domain)
     #print('Domain id', requestid_domain)
     form = CreateTrustCalcForm()
     if form.validate_on_submit:
         print('Form is validated')
         print(form.irb_id.data.irb_id)
     print('form irb_id and form radiology image is',form.irb_id.data, form.radiology_imaging_reports.data.decision)
     irb_id = form.irb_id.data.irb_id
     #requestid = form.requestid.data.requestid   
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
     
     #reqvar =  User.query.filter_by(ownerid=current_user.id) 
     templist = [radiology_images, radiology_imaging_reports, ekg, progress_notes, history_phy, oper_report, path_report, lab_report, photographs, discharge_summaries, health_care_billing, consult, medication, emergency, dental, demographic, question, audiotape]
     if (current_user.username == 'internaluser'):
         userrole = 'internal_user'
     elif (current_user.username == 'externaluser'):
         userrole = 'external_user'

         
     #item_select_query = "select itemunique from item_info  where itemname = radiology_images";
     #item_info = ItemInfo.query.filter_by(itemname=radiology_images).all()

     #print('after item info')
     #print(item_info)
     #for i in item_info:
     #    print('item details',i)

     postgreSQL_select_Query = "select * from data_policy_domain  where data_policy_domain.irb_number = %s"
     cur.execute(postgreSQL_select_Query, [irb_id])
     resultset = cur.fetchone()
     #dataset_id = resultset[0]
     #print('resultset is',resultset)
     d = resultset[1:]
     print(d[0])
     si=0      
     #countmismatch = 0
     #countundecided = 0
     #countmatch = 0
     for a,b in zip(templist, d):
         if (a == 'Yes' and b == '1'):
             si+= 1
         elif (a == 'No' and b == '1'):
             si+= 1
         elif (a == 'No' and b == 'None'):
             si+= 1
         elif (a == 'No' and b == '1'):
             si+= 0
         
         print(si)
         sum=0
         com=sum+(si*10)
         print(com)
     N=18
     com=com/N
     compliance=com
     print("Compliance is", compliance)
     # beta model trust calculation
     #alpha_c = floor(countmatch + ((countundecided*countmatch)/(countmatch+countmismatch)));
     #beta_c = N - alpha_c;
     #Ei = float(alpha_c + 1)/float(alpha_c + beta_c + 2);
     #Ei = format(Ei, '.2f')
     #print('Beta model is',Ei)
    
     
     # Formula 7 of trust model
     #a = 0.7
     #Eb = float(countmatch+1.0) / float(countmatch+countmismatch+countundecided+3.0)
     #Eu = float(countundecided+1.0) / float(countmatch+countmismatch+countundecided+3.0)
     #Ew = (Eb + a*Eu)
     
     #rEw = log(Ew)/log((1-Ew))
     #print('rEw',rEw)
     #rEw = log(c)
     #if rEw > 0:
      #   wi = 1 - exp(-abs(rEw))
     #elif rEw < 0:
      #   wi = -(1 - exp(-abs(rEw)))
     #else:
      #   wi = 0
     #wi = format(wi, '.2f')
     #print('dirichlet model is', wi)
     
     cur.execute('SELECT dataset_id FROM data_catalog')
     resultset = cur.fetchall()   
     dataset_id1 = dataset_id_final
     print("Dataset id value is", dataset_id1)


     print("Request id value is ", str(requestid_domain))
     #db.session.execute("select requestname from request_form where requestid=requestid")     
     #print(a)
     
     #datasetprint=form.datasetname.data.nameset
     #postgreSQL_select_Query = "select * from data_catalog  where data_catalog.dataset_name = %s"
     #cur.execute(postgreSQL_select_Query, [datasetprint])
     #resultset = cur.fetchone()
     #dataset_id = resultset[0]
     #print('The rows of selected dataset in domain form are',resultset[0])

     #tasklist =1
     #task_id=1
     dr=dataset_risk
     status = 'pending'
     risk_level='low'
     reputation=10
     decision='NA'
     #user_id = current_user.id
     #dataset = '{"dataset_id": %s, "risk_level": %s, "decision": %s, "reputation": %s, "user": %s}' % (dataset_id, risk_level, status, reputation, user)
     #trans = '{"inputcs": %s, "inputdr": %s, "dataset": %s, "user": %s}' % (compliance, dr, dataset, user)
     #r_get = requests.post("http://3.81.13.0:3000/api/TaskList", json=task_json_obj)
     #print(r_get.status_code)
     #r_post = requests.post("http://3.81.13.0:3000/api/User", json=user_json_obj)
     #print(r_post.status_code)
     #status = 'pending'
     print(current_user.username)
     print(current_user.id)
     get_user_params = {"userId":current_user.id }
     get_data_params = {"requestId":str(requestid_domain)}
     f= open("requestid.txt","w+")
     f.write(requestid_domain)
     f.close()
     #get_trans_params = {"request_id":requestid_domain}
     user = requests.get("http://3.81.13.0:3000/api/User", params=get_user_params)
     data = requests.get("http://3.81.13.0:3000/api/Dataset", params=get_data_params)
     #trans = requests.get("http://3.81.13.0:3000/api/ChainTransaction",params=get_trans_params)
     #print(trans.content)
     #print(trans.status_code)
     #print(data.content)
     #print(data.status_code)
     #print(user.content)
     #print(user.status_code)
     #print(requestid_domain)
     #user_json = '{"userId": %s, "username" : %s}' % (current_user.id,current_user.username)
     user_json = {"userId": current_user.id, "username" : current_user.username}
     #a=json.loads(user_json)
     #print(user_json)
     dataset_json = {"requestId":str(requestid_domain),"datasetId" : dataset_id1,"risk_level": risk_level, "decision": decision, "reputation": reputation,"last_requester" :"resource:org.honestchain.User#" +str(current_user.username) }
     #dataset_json = {"datasetId": dataset_id1}   
     print("Dataset details",dataset_json)
     #trans = '{"inputcs": %s, "inputdr": %s, "dataset": %s, "user": %s}' % (compliance, dr, dataset_json, user.content)
     #print(dataset)
     #print(trans)
     if user.status_code == '200' or user.content != '[]':
         r_post_user = requests.post("http://3.81.13.0:3000/api/User", json=user_json)
     print(user.content)
     if data.status_code == '200' or data.content != '[]':
         data = requests.post("http://3.81.13.0:3000/api/Dataset", json=dataset_json)
     print(data.content)
    # trans = '{"request_id": %s, "inputcs": %s, "inputdr": %s, "dataset": %s, "user": %s}' % (requestid_domain,compliance, dr, data.content , "resources:org.honestchain.User#" +str(current_user.id))
     #if trans.status_code == '200' or trans.content == '[]': i
     #trans_json = {"requestid": str(requestid_domain),"datasetId": dataset_id1, "inputcs": compliance, "inputdr": dr, "dataset": "resource:org.honestchain.Dataset#"+ dataset_id1[0], "user" : "resource:org.honestchain.User#" +str(current_user.username)}
     trans_json = {"requestId": str(requestid_domain),"datasetId": dataset_id1, "inputcs": compliance, "inputdr": dr, "dataset": "resource:org.honestchain.Dataset#"+ str(requestid_domain), "user" : "resource:org.honestchain.User#" +str(current_user.username)}
     
     print("Trans details" , trans_json)
     #if trans.status_code == '200' or trans.content == '[]':
     trans_post = requests.post("http://3.81.13.0:3000/api/ChainTransaction", json=trans_json)
     print("Posted content",trans_post.content)
     result_get = requests.get("http://3.81.13.0:3000/api/Dataset", params=get_data_params)
     print("Final Result",result_get.content)
     #print(trans_post.content)
     #print(result_get.content.decision)
        
        # r_post_task = requests.post("http://3.81.13.0:3000/explorer/TaskList", json=task_json_obj)
     #    a =request.form['data']
    #print type(a)
    #a=a.encode("utf-8")
    #print type(a)
     b=result_get.content
     
     #print(b)
     #b=b.encode("utf-8")
     b =json.loads(b)
     for i in b:
        a=i['requestId']
        print(a)
        print(len(i))
        print(len(b))
        c=i['requestId'],i['datasetId'],i['risk_level'],i['reputation'],i['decision']
        d=i['decision']
        e = i['datasetId']
    
        app_req = [ x for x in b if x['decision'] == 'approved' and x['last_requester'] == 'resource:org.honestchain.User#'+str(current_user.username)]
        deny_req = [ x for x in b if (x['decision'] == 'denied')  and x['last_requester'] == 'resource:org.honestchain.User#'+str(current_user.username)]
        manual_req = [x for x in b if x['decision'] == 'manual approval required' and x['last_requester'] == 'resource:org.honestchain.User#'+str(current_user.username)]
        reqid_table=RequestForm.query.filter_by(requestid=a ).all()
        #for i in app_req:
            #print('app req is',app_req['requestId'])
        print('approved request printed before') 
        for i in reqid_table:
            print(i.requestname)
            print(i.requestDescription)

    
        print(c)
        #print[i['requestId'],i['datasetId'],i['risk_level'],i['reputation'],i['decision']]
        #print(i['requestId'])
        #a=i['requestId']
        
        #print(i['requestId'])   

   
        #print(a)
        #for i['requestId'] in b:
         #   print[i['requestId'],i['datasetId'],i['risk_level'],i['reputation'],i['decision']]
     #print("1st element :" b[requestId])
     #with open('b') as f:
      #   file=json.load(f)
     #print(file['requestId'])    
        
     #print(b[requestId])
     #print type(dic)
     #print dic
     #with open('data.csv', 'w') as csv_file:
         #for requestId in b:
         #csv_writer = csv.writer(csv_file,lineterminator='\n')
         #csv_writer.writerow(b)
    # pendingreq_info = RequestForm.query.filter_by(ownerid=current_user.id, status = 'pending').all()
    # pendingreq_info.requestid=requestId 
    
         #pendingreq_info = RequestForm.query.filter_by(ownerid=current_user.id, status = 'pending').all()
         #pendingreq_info.requestid=requestId
         #print(requestId)
     #content=request.get_json()
     #value1=content.get('decision')
     #print(value1)
     #text = dic[(datasetId)]
     #print type(text)
     #print text
     
     

        
     new_hipaa_request = TrustCalcForm(ownerid =  current_user.id, requestid = requestid_domain, radiology_images = radiology_images, radiology_imaging_reports = radiology_imaging_reports, ekg = ekg, progress_notes = progress_notes, history_phy = history_phy, oper_report = oper_report, path_report = path_report, lab_report = lab_report, photographs = photographs, discharge_summaries = discharge_summaries,  health_care_billing= health_care_billing, consult = consult, medication = medication, emergency = emergency, dental  = dental, demographic = demographic,question = question, audiotape = audiotape, compliance=compliance, status = status)
     db.session.add(new_hipaa_request)
     db.session.commit()
    
     pendingreq_info = TrustCalcForm.query.filter_by(ownerid=current_user.id, status = 'pending').all()
     #for i in request_info:
    #     print("the trust id is", i.trustid)
     apprInternal_info = TrustCalcForm.query.filter_by(ownerid=current_user.id, status = 'approved').all()
     deniedInternal_info = TrustCalcForm.query.filter_by(ownerid=current_user.id, status= 'denied').all()
     
     con=sqlite3.connect("database.db")
     c = con.cursor()
     c.execute("SELECT * FROM trust_calc_form")
     data = cur.fetchall()         
     

     pendingreq_info = RequestForm.query.filter_by(ownerid=current_user.id, status = 'pending').all()
     apprInternal_info = RequestForm.query.filter_by(ownerid=current_user.id, status = 'approved').all()
     deniedInternal_info = RequestForm.query.filter_by(ownerid=current_user.id, status= 'denied').all()

     #cursor = db.execute('SELECT * FROM trust_calc_form')
     #items = cursor.fetchall()
    
        # return render_template('hipaa.html',items=items)
     
     #return render_template('dashboard.html', form=form, pendingreq_info=pendingreq_info, apprInternal_info=apprInternal_info, deniedInternal_info=deniedInternal_info,data=data,b=b,requestid_domain=requestid_domain,len=len(b),a=a,c=c,d=d)
     #return render_template('request_status.html',form=form,name = current_user.username, pendingreq_info=pendingreq_info, apprInternal_info=apprInternal_info, deniedInternal_info=deniedInternal_info,data=data,b=b,requestid_domain=requestid_domain,len=len(b),a=a,c=c,d=d,e=e, app_req = app_req, deny_req = deny_req, manual_req = manual_req, reqid_table = reqid_table)
     
     return render_template('request_status.html', name = current_user.username, form=form, pendingreq_info=pendingreq_info, apprInternal_info=apprInternal_info, deniedInternal_info=deniedInternal_info,data=data,b=b,requestid_domain=requestid_domain,len=len(b),a=a,c=c,d=d,e=e, app_req = app_req, deny_req = deny_req, manual_req = manual_req, reqid_table = reqid_table)


@app.route('/print_items')
def print_items():
    con=sqlite3.connect("database.db")
    co = con.cursor()
    co.execute("SELECT radiology_images,radiology_imaging_reports,progress_notes,compliance FROM trust_calc_form")
    items=co.fetchall()
    return render_template('print_items.html', items=items)


@app.route('/identifierform', methods=['GET','POST'])
def identifierform():
    print('in trust form')
    form = CreateTrustCalcForm()
    if form.validate_on_submit():
        print('Form validated')
    else:
        print(form.errors)
    return render_template('identifier_form.html',form=form)


@app.route('/submitrequest', methods=['GET','POST'])
def submitrequest():
     #print(current_user.username)
     form = CreateRequestForm()
     #print("user id is", current_user.id)
     #if form.validate_on_submit()

     datasetprint=form.datasetname.data.nameset
     print('dataset is', datasetprint)
     postgreSQL_select_Query = "select * from data_catalog  where data_catalog.dataset_name = %s"
     cur.execute(postgreSQL_select_Query, [datasetprint])
     resultset = cur.fetchone()
     print(resultset)
     dataset_id_final = resultset[0]
     postgreSQL_select_Query = "select dataset_score from data_catalog  where data_catalog.dataset_name = %(dataset_name)s"
     #print(type(dataset_id_final))     
     cur.execute(postgreSQL_select_Query,{'dataset_name':datasetprint})
     resultset1 = cur.fetchone()
        
     print(resultset1[0])
     dataset_risk=resultset1[0]
     print('Data risk score is', dataset_risk)
     print('The rows of selected dataset are',dataset_id_final)
     #print('datasetrisk',resultset[2])
     #print('User selected',datasetprint)
    
     
     #sel_dataset=resultset[0]
     #print("Selected dataset is", sel_dataset)   

     input_risk = list([1,3,3]);
     if(current_user.username == 'internal'):
         input_risk[0] = 1
     elif(current_user.username== 'external'):
         input_risk[0] = 90
     

    #determining input_risk for data_type
     if(form.typeofdata.data == 'identified'):
         input_risk[1] = 95;
     elif(form.typeofdata.data == 'deidentified'):
         input_risk[1] = 30;

     elif(form.typeofdata.data== 'limited'):
         input_risk[1] = 45;
     elif(form.typeofdata.data == 'aggregated'):
         input_risk[1] = 3;
     #dataset_risk = resultset[2];
    # accept_risk = resultset[3];
    # input_risk[2] = dataset_risk;
     #total_risk = 0;
#     data_risk = accept_risk;
     #for i in input_risk:

      #   total_risk += log(i);
     #print('total risk is', total_risk)


     #risk_factor = exp(total_risk);
     #print('risk factor is', risk_factor)
     #risk_level = "low";

     #if(risk_factor >= (1.25 * data_risk)):

     #    risk_level = "high";
     #elif((risk_factor >= (0.75 * data_risk)) and (risk_factor <= (1.25 * data_risk))):

      #   risk_level = "medium";
     #else:

       #  risk_level = "low";
    

     new_request = RequestForm(ownerid =  current_user.id, requestname=form.requestname.data,datasetid = form.datasetname.data.datasetid, requestDescription=form.requestDescription.data, use=form.use.data, store=form.store.data, longdata = form.longdata.data, soondata = form.soondata.data, typeofdata = form.typeofdata.data, status = 'pending')
     db.session.add(new_request)
    # print(new_request.requestid)
     db.session.commit()
     print(new_request.requestid)

     print("Dataset id is" , new_request.datasetid)
     #request_info = RequestForm.query.filter_by( ownerid = current_user.id).all()
     #for request in request_info:
      #   requestObject = { 'status'  : request.status,
       #                    'requestname' : request.requestname
        #         }
        
         #print("Here at 3",request.status)
     #print(requests.user.email)
     pendingreq_info = RequestForm.query.filter_by(ownerid=current_user.id, status = 'pending').all()
     apprInternal_info = RequestForm.query.filter_by(ownerid=current_user.id, status = 'approved').all()
     deniedInternal_info = RequestForm.query.filter_by(ownerid=current_user.id, status= 'denied').all() 
    # datasetid = resultset[0]
    # p=result_get.content

     #if(current_user.username == 'internaluser'):
      #   return render_template('dashboard.html',name = current_user.username, form=form, pendingreq_info=pendingreq_info, apprInternal_info=apprInternal_info, deniedInternal_info=deniedInternal_info,requestid_domain=new_request.requestid,dataset_id_final=dataset_id_final,dataset_risk=dataset_risk)
         #return redirect('jupyter notebook')
     #elif(current_user.username == 'externaluser'):
      #   return render_template('dashboard.html', name = current_user.username, form=form, pendingreq_info=pendingreq_info, apprInternal_info=apprInternal_info, deniedInternal_info=deniedInternal_info,requestid_domain=new_request.requestid,dataset_id_final=dataset_id_final,dataset_risk=dataset_risk)
     f = open('requestid.txt','r')
     requestid_domain=f.read()

    #requestid_domain = session.get('requestId')
     get_data_params = {"requestId":str(requestid_domain)}
     result_get = requests.get("http://3.81.13.0:3000/api/Dataset", params=get_data_params)
     print("Final Result",result_get.content)
     b=result_get.content
     b =json.loads(b)
     app_req = [ x for x in b if x['decision'] == 'approved' and x['last_requester'] == 'resource:org.honestchain.User#'+str(current_user.username)]
     deny_req = [ x for x in b if x['decision'] == 'denied'  and x['last_requester'] == 'resource:org.honestchain.User#'+str(current_user.username)]
     manual_req = [x for x in b if x['decision'] == 'manual approval required' and x['last_requester'] == 'resource:org.honestchain.User#'+str(current_user.username)]
     return render_template('request_status.html',requestid_domain=new_request.requestid,dataset_id_final=dataset_id_final,dataset_risk=dataset_risk, name = current_user.username, b=b, app_req = app_req, deny_req = deny_req, manual_req = manual_req)
   # return redirect('jupyter notebook')

@app.route('/viewmyreq/<req_id>', methods = ['GET',' POST'])
@login_required
def viewmyreq(req_id):
    
    #searchword = request.args.get('req_id', '')
    print("req id for internal user is",req_id)
    #print(request.url)
    #print(request.__dict__.items())
    #number = request.args.get('req_id')
    #print("Here at 4",number)
    

    return render_template('viewRequests.html')
@app.route('/viewpendingreq/<req_id>', methods = ['GET',' POST'])
@login_required
def viewpendingreq(req_id):
    
    pendingreq_info = RequestForm.query.filter_by(requestid=req_id, status = 'pending').all()
    for i in pendingreq_info:
        print('The dataset id is',i.datasetid)
    #postgreSQL_select_Query = "select * from data_catalog  where data_catalog.dataset_name = %s"
    #cur.execute(postgreSQL_select_Query, [datasetprint])
    #resultset = cur.fetchone()
    jupyter= RequestForm.query.filter_by(requestid=req_id).all()
    pendingreq_info = RequestForm.query.filter_by(requestid=req_id).all()
    for i in pendingreq_info:
        datasetinfo = Dataset.query.filter_by(datasetid = i.datasetid).all()
    for j in datasetinfo:
        dataset_name = j.nameset
    pg_query = 'select * from data_catalog where dataset_name = %s'
    cur.execute(pg_query,[dataset_name])
    record = cur.fetchone()
    print("Result",record)

    approvedreq_info = RequestForm.query.filter_by(status= 'approved').all()
    denyreq_info = RequestForm.query.filter_by(status= 'denied').all()

    return render_template('viewpendingreq.html', name = current_user.username,jupyter=jupyter, pendingreq_info = pendingreq_info, record=record)
# have to modify

@app.route('/jupyter', methods = ['GET',' POST'])
@login_required
def jupyter():
     #return redirect('http://127.0.0.1:8888/notebooks/Untitled%20Folder%201/Request_data.ipynb')
     return redirect('https://colab.research.google.com/drive/1MMRUuABHO0T-gx17dx4Lo-7Dzu21oGue')

@app.route('/viewappInternal/<req_id>', methods = ['GET',' POST'])
@login_required
def viewappInternal(req_id):
    
    approvedreq_info = RequestForm.query.filter_by(status = 'pending').all()
    #denyreq_info = RequestForm.query.filter_by(status= 'denied').all()
    #pending_req = RequestForm.query.filter_by(status= 'pending').all()
    for j in approvedreq_info:
        print("Approved request is",j.requestname)

    for i in approvedreq_info:
        datasetinfo = Dataset.query.filter_by(datasetid = i.datasetid).all()
    for j in datasetinfo:
        dataset_name = j.nameset
    pg_query = 'select * from data_catalog where dataset_name = %s'
    cur.execute(pg_query,[dataset_name])
    record = cur.fetchone()
    print("Result",record)
    cur.execute(record[4])
    data = cur.fetchall() 
    rowcount = cur.rowcount
    print('row count', cur.rowcount)
    #for v in data:
        #for column, value in v.items()
            #print('{0}: {1}'.format(column, value))

    return render_template('viewdatauser.html',name = current_user.username, rowcount=rowcount, approvedreq_info = approvedreq_info, data = data)
# Have to modify
@app.route('/viewdenied/<req_id>', methods = ['GET',' POST'])
@login_required
def viewdenied(req_id):

    pendingreq_info = RequestForm.query.filter_by(requestid=req_id).all()
    for i in pendingreq_info:
        print(i.requestname)


    return render_template('viewRequests.html', name = current_user.username, pendingreq_info = pendingreq_info)


@app.route('/approvereq/<req_id>', methods = ['GET',' POST'])
@login_required
def approvereq(req_id):
    

    pendingreq_info = TrustCalcForm.query.filter_by(requestid=req_id).all()
    for i in pendingreq_info:
        i.status = 'approved'
        db.session.commit()
    approvedreq_info = TrustCalcForm.query.filter_by(status = 'approved').all()
    denyreq_info = TrustCalcForm.query.filter_by(status= 'denied').all()
    pending_req = TrustCalcForm.query.filter_by(status= 'pending').all()
    #for j in approvedreq_info:
     #   print("Approved request is",j.requestname)
    
    #for i in pendingreq_info:
     #   datasetinfo = Dataset.query.filter_by(datasetid = i.datasetid).all()
    #for j in datasetinfo:
     #   dataset_name = j.nameset
    #pg_query = 'select * from data_catalog where dataset_name = %s'
    #cur.execute(pg_query,[dataset_name])
    #record = cur.fetchone()
    #print("Result",record)

    return render_template('dashboard_admin.html',name = current_user.username, pending_req=pending_req, record = record, denyreq_info =denyreq_info, approvedreq_info = approvedreq_info)

@app.route('/approvedadmin/<req_id>', methods = ['GET',' POST'])
@login_required
def approvedadmin(req_id):

    approvedreq_info = RequestForm.query.filter_by(status = 'approved').all()
    for i in approvedreq_info:
        datasetinfo = Dataset.query.filter_by(datasetid = i.datasetid).all()
    for j in datasetinfo:
        dataset_name = j.nameset
    print('Datasetname selected is',dataset_name)
    pg_query = 'select * from data_catalog where dataset_name = %s'
    cur.execute(pg_query,[dataset_name])
    record = cur.fetchone()
    print("Result",record)
    cur.execute(record[4])
    data = cur.fetchall()
    rowcount = cur.rowcount
    return render_template('viewdataadmin.html',name = current_user.username, rowcount=rowcount, data = data, approvedreq_info = approvedreq_info)

@app.route('/denyreq/<req_id>', methods = ['GET',' POST'])
@login_required
def denyreq(req_id):

    pendingreq_info = TrustCalcForm.query.filter_by(requestid=req_id).all()
    pending_req = TrustCalcForm.query.filter_by(status= 'pending').all()
    approvedreq_info = TrustCalcForm.query.filter_by(status= 'approved').all()
    for i in pendingreq_info:
        i.status = 'denied'
        db.session.commit()
    #denyreq_info = RequestForm.query.filter_by(status = 'denied').all()
    denyreq_info = TrustCalcForm.query.filter_by(status = 'denied').all()

    return render_template('dashboard_admin.html', name = current_user.username, pending_req= pending_req, approvedreq_info=approvedreq_info, denyreq_info = denyreq_info)

@app.route('/request',methods=['GET','POST'])
def request_form():
    form = CreateRequestForm()
    return render_template('request.html', form=form)
   # return render_template('bot/index_bot.html', form=form)

@app.route('/viewdata/<dataid>',methods=['GET','POST'])
def viewdata(dataid):
    
    print(dataid)
    a=dataid
    postgreSQL_select_Query = "select * from data_catalog where data_catalog.dataset_id = %(dataset_id)s"
    cur.execute(postgreSQL_select_Query,{'dataset_id':dataid})
    record = cur.fetchone()
    #print("Result",record)
    cur.execute(record[4])
    data = cur.fetchall()
    rowcount = cur.rowcount
    return render_template('viewapprovedata.html',name = current_user.username, dataid=dataid, data = data, rowcount = rowcount, record=record)



@app.route('/feedbackform',methods=['GET','POST'])
def feedback_form():
    form = FeedbackForm()
    return render_template('feedback.html',form=form)

@app.route('/submitfeedbackform',methods=['GET','POST'])
def submitfeedbackform():
    return render_template('end.html')

@app.route('/')
def bc():
    return redirect("http://128.163.232.85:8080/test", code=302)

@app.route('/enter_request',methods=['GET','POST'])
def enter_request():
    form = CreateRequestForm()
    return render_template('request.html', form=form)

@app.route('/save_dialog', methods=['POST'])			
def save_dialog():
    a =request.form['data']
    print type(a)
    a=a.encode("utf-8")
    print type(a)
    dic =json.loads(a)
    print type(dic)
    print dic
    text = dic[u'result'][u'resolvedQuery']
    print type(text)
    print text

    #with sql.connect("database.db") as con:
    # cur = con.cursor()
        #cur.execute("INSERT data into trial (text, time) values (?,?)",(data, int(time())))
    record=trial(data_set_name=text)
    db.session.add(record)
    db.session.commit()
    return "Saved successfully"
    #return "Failed to save."


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)
