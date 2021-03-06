#!/usr/bin/env python
import os
from flask import Flask, render_template, url_for, redirect, session, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import requests
from flask_script import Manager
from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Required
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']=\
 #       'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI']= "postgresql://varoon:varoon@localhost:5432/population"
app.config['SQLALCHMEY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#manager = Manager(app)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'secretkey'

# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     users = db.relationship('User', backref='role')

#     def __repr__ (self):
#         return '<Role %r>' % self.name

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True, index=True)
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

#     def __repr__(self):
#         return '<User %r>' % self.name

class Country(db.Model):
    __tablename__ = 'country'
    countryid = db.Column(db.Integer, primary_key=True)
    countryname = db.Column(db.String(64), unique=True)


    def __repr__ (self):
        return '<Country %r>' % self.countryname

class populationdata(db.Model):
    __tablename__ = 'populationdata'
    populationid = db.Column(db.Integer, primary_key=True)
    countryid = db.Column(db.Integer, index=True)
    age = db.Column(db.Integer)
    male = db.Column(db.Integer)
    female = db.Column(db.Integer)
    year = db.Column(db.Integer)

    def __repr__(self):
        return '<populationdata %r>' % self.countryid




class populationRequest(Form):
    year = IntegerField('Enter Year (1950 and 2100)', validators=[Required()])
    age = IntegerField('Enter age (0-100)', validators=[Required()])
    gender = SelectField('Select Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
    country = SelectField('Select a country', choices=[('Guyana', 'Guyana'), 
                            ('Jamaica', 'Jamaica'), ('Trinidad and Tobago', 'Trinidad and Tobago')])
    submit = SubmitField('Submit')
class perCountry(Form):
     country = SelectField('Select a country', choices=[('Guyana', 'Guyana'), 
                            ('Jamaica', 'Jamaica'), ('Trinidad and Tobago', 'Trinidad and Tobago')])                            
     age = SelectField('Select age (18,25,30)',   choices=[('18', 18), ('25', 25), ('30', 30)])

     submit = SubmitField('Submit')      
class countryRequest(Form):
     country = SelectField('Select a country', choices=[('Guyana', 'Guyana'), 
                            ('Jamaica', 'Jamaica'), ('Trinidad and Tobago', 'Trinidad and Tobago')])                            
     age = SelectField('Select age (18,25,30)',   choices=[('18', 18), ('25', 25), ('30', 30)])
     gender = SelectField('Select Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
     submit = SubmitField('Submit')                        

class compareCountries(Form):
    country1= SelectField('Select  1st Country', choices=[('Guyana', 'Guyana'), 
                            ('Jamaica', 'Jamaica'), ('Trinidad and Tobago', 'Trinidad and Tobago')])    

    country2=  SelectField('Select 2nd Country', choices=[('Guyana', 'Guyana'), 
                            ('Jamaica', 'Jamaica'), ('Trinidad and Tobago', 'Trinidad and Tobago')])   

    age= SelectField('Select age (18,25,30)',   choices=[('18', 18), ('25', 25), ('30', 30)])

    gender = SelectField('Select Gender', choices=[('Male', 'Male'), ('Female', 'Female')])   
    submit = SubmitField('Submit')     

class agregateCountries(Form):
    country1= SelectField('Select  1st Country', choices=[('Guyana', 'Guyana'), 
                            ('Jamaica', 'Jamaica'), ('Trinidad and Tobago', 'Trinidad and Tobago')])    

    country2=  SelectField('Select 2nd Country', choices=[('Guyana', 'Guyana'), 
                            ('Jamaica', 'Jamaica'), ('Trinidad and Tobago', 'Trinidad and Tobago')])   

    age = SelectField('Select age (18,25,30)',   choices=[('18', 18), ('25', 25), ('30', 30)])

    submit = SubmitField('Submit')                            
    
    
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')



@app.route('/table', methods=['GET', 'POST'])
def table():
    form = perCountry()
    session.pop('collection2', None)
    session.pop('collection3', None)
    session.pop('collection', None)
    #session.pop('country', None)
    if form.validate_on_submit():
          
 
        age = form.age.data
        country = form.country.data


        c= Country.query.filter_by(countryname= country).first()
        #c2= populationdata.query.filter_by(countryid=c.countryid,age=age,year=year).all()
        c2= populationdata.query.filter_by(countryid=c.countryid,age=age).all()
        collection= []
        for e in c2:
            data= [e.populationid, e.countryid, e.age, e.male, e.female, e.year]
            data2= {'year':e.year,'age':age,'country':country,'male':e.male,'female':e.female}
            #data2= {'year':year,'age':age,'country':country,'male':e.male,'female':e.female}
            collection.append(data2)
        session['country'] = country
        
        session['query']= collection
        #session['query'] = [(e.populationid,e.countryid,e.age,e.male,e.female,e.year)
        print(collection)
        print (country)
     
        return redirect(url_for('table'))
    # return render_template('query.html', form=form, pop_data=session.get('pop_io'))
   # result = Country.query.all()
    return render_template('tables.html', form=form, country=session.get('country'), query=session.get('query'))




@app.route('/single', methods=['GET', 'POST'])
def country(): 
    form1= countryRequest()

   

    if form1.validate_on_submit():
        session.pop('collection2', None)
        session.pop('collection3', None)
        country = form1.country.data
        age = form1.age.data
        gender = form1.gender.data
        #get country id
        
        r =Country.query.filter_by(countryname= country).first()

        #query all data for country in populationdata table
        r2 =populationdata.query.filter_by(countryid=r.countryid,age=age).all()
        collection = []
        print (r2)
        for e in r2:
         
            #data2= [{'year':year,'age':age,'country':country,'gender':gender,'male':e.male,'female':e.female}]
            if (gender=='Male'):
                tuple = {'year': e.year,'age':age,'country':country, 'gender':e.male, 'group': 1}
            elif (gender=='Female'):
                tuple = {'year': e.year,'age':age,'country':country, 'gender':e.female,'group': 1}
            #append result to collection
            collection.append(tuple)
        session.pop('country', None)
        session['country'] ={'country1':country,'age':age, 'gender':gender}
        #session['collection'] = collection
        #print(collection)

        session['single']=1
        session['collection']=collection

        print  (session['collection'])
        return redirect(url_for('country'))
    return render_template('single.html',form1=form1,query1=session.get('collection'),country=session.get('country'))

@app.route('/compare', methods=['GET', 'POST'])
def compareCountry():   
     #Comparison form     
    form2 = compareCountries()
    if form2.validate_on_submit():

        country1 = form2.country1.data
        country2 = form2.country2.data
        age = form2.age.data        
        gender = form2.gender.data
        r_country1 =Country.query.filter_by(countryname= country1).first()
        r_country2 =Country.query.filter_by(countryname= country2).first()

        r2_country1= populationdata.query.filter_by(countryid= r_country1.countryid,age=age).all()
        collection1 = []
        for e in r2_country1:
            if (gender=='Male'):
                    tuple = {'year': e.year,'age':age,'country':country1, 'gender':e.male, 'group': 1}
            elif (gender=='Female'):
                tuple = {'year': e.year,'age':age,'country':country1, 'gender':e.female, 'group': 1}
            #append result to collection
            collection1.append(tuple)

        r2_country2= populationdata.query.filter_by(countryid= r_country2.countryid,age=age).all()
        collection2 = []
        for e in r2_country2:
            if (gender=='Male'):
                    tuple = {'year': e.year,'age':age,'country':country2, 'gender':e.male, 'group': 2}
            elif (gender=='Female'):
                tuple = {'year': e.year,'age':age,'country':country2, 'gender':e.female, 'group': 2}
            
            collection2.append(tuple)
        session.pop('country', None)    
        session['country'] = {'country1':country1,'country2':country2 ,'age':age, 'gender':gender}
       
    
        #print (collection1,collection2)
        collection =collection1+collection2

        session['collection2'] = collection
        print  (session['collection2'])
        return redirect(url_for('compareCountry'))

    return render_template('compare.html',form2=form2,query2=session.get('collection2'),country=session.get('country'))


@app.route('/totals', methods=['GET', 'POST'])
def agregateCountry():  
    form3= agregateCountries() 
    if form3.validate_on_submit():  
        session.pop('collection', None)
        session.pop('collection2', None)
        country1 = form3.country1.data
        country2 = form3.country2.data
        age = form3.age.data      

        r_country1 =Country.query.filter_by(countryname= country1).first()
        r_country2 =Country.query.filter_by(countryname= country2).first()

        r2_country1= populationdata.query.filter_by(countryid= r_country1.countryid,age=age).all()
        collection1 = []
        for e in r2_country1:
                tuple = {'year': e.year,'age':age,'country':country2, 'gender':e.male+ e.female, 'group': 1}
                collection1.append(tuple)
        r2_country2= populationdata.query.filter_by(countryid= r_country2.countryid,age=age).all()
        collection2 = []
        for e in r2_country2:
                tuple = {'year': e.year,'age':age,'country':country2, 'gender':e.male+ e.female, 'group': 2}
                collection2.append(tuple)        
        collection =collection1+collection2

        session['collection3'] = collection
        session['country'] = {'country1':country1,'country2':country2 ,'age':age, 'gender':'Male & Female'}
        print  (session['collection3'])
        return redirect(url_for('agregateCountry'))

    return render_template('totals.html',form3=form3,query3=session.get('collection3'),country=session.get('country'))


if __name__ == '__main__':
    db.create_all     
    app.run(host='127.0.0.1', port=5000, debug=True)

