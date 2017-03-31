from flask import Flask, render_template, url_for, redirect, session
from flask_bootstrap import Bootstrap
import requests
from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Required
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'secretkey'


class populationRequest(Form):
    year = IntegerField('Enter Year (1950 and 2100)', validators=[Required()])
    age = IntegerField('Enter age (0-100)', validators=[Required()])
    #country = SelectField('Selct a country')
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = populationRequest()   
   

    if form.validate_on_submit():
        year = form.year.data
        age = form.age.data
        values= (year,age,)
        data= getRequest(year,age)
        session['data'] = data
        session['age'] = age
        
        #session['test']= [0,1,2]
        #form.year.data = ''
        #form.age.data = ''
        
        # return redirect(url_for('index'))
  
    return render_template('index.html', form=form, pop_data=session.get('data'))

def getRequest(year,age):
        r = requests.get('http://api.population.io:80/1.0/population/'+ str(year)+ '/aged/'+ str(age)+ '/')
        data = r.json()
        return data
       



if __name__ == '__main__':
    app.run(debug=True)
