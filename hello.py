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


manager = Manager(app)
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
    #country = SelectField('Selct a country')
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')


@app.route('/data')
def data():
    print (session.get('data'))
    print (session.get('pop_io'))
    return render_template('index2.html',  pop_data=session.get('pop_io'))


@app.route('/query', methods=['GET', 'POST'])
def query():
    # session['data'] = ['foobar']
    form = populationRequest()
    if form.validate_on_submit():
        year = form.year.data
        age = form.age.data
        getRequest(year, age)
        session['data'] = [year, age]
        return redirect(url_for('index'))
    # return render_template('query.html', form=form, pop_data=session.get('pop_io'))
    result=Country.query.all()
    return render_template('query.html', form=form,query=result)
    
def getRequest(year, age):
        print (year,age)
        #r = requests.get('http://api.population.io:80/1.0/population/'+ str(year)+ '/aged/'+ str(age)+ '/')
        #r = requests.get('http://swapi.co/api/people/1/')
       # data = r.json()
        data ={'name': 'Luke Skywalker', 'height': '172', 'mass': '77', 'hair_color': 'blond', 'skin_color': 'fair', 'eye_color': 'blue',
         'birth_year': '19BBY', 'gender': 'male', 'homeworld': 'http://swapi.co/api/planets/1/', 'films': ['http://swapi.co/api/films/6/', 
         'http://swapi.co/api/films/3/', 'http://swapi.co/api/films/2/', 'http://swapi.co/api/films/1/', 'http://swapi.co/api/films/7/'], 
         'species': ['http://swapi.co/api/species/1/'], 'vehicles': ['http://swapi.co/api/vehicles/14/', 'http://swapi.co/api/vehicles/30/'],
          'starships': ['http://swapi.co/api/starships/12/', 'http://swapi.co/api/starships/22/'], 'created': '2014-12-09T13:50:51.644000Z', 
          'edited': '2014-12-20T21:17:56.891000Z', 'url': 'http://swapi.co/api/people/1/'}
        #data= ['derp', 'lerp']
        print (data)
        session['pop_io']= data

if __name__ == '__main__':
    db.create_all()
    manager.run()

