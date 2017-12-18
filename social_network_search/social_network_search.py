from flask import Flask, session, url_for, render_template, flash, request, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import json 
import os

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

def get_social_network_contacts():
    path = os.path.dirname(__file__)
    with open(os.path.join(path, 'socialcontacts.json')) as contactsfile:
        contacts = json.load(contactsfile)
    return contacts

 
class ReusableForm(Form):
    job_history = TextField('Job History:')
    company = TextField('Company:')
    email = TextField('Email:')
    city = TextField('City:')
    name = TextField('Name:')
    country = TextField('Country:')


def validate_contact(search_fields, contact):
    valid = True

    if search_fields['name'] != "" and contact['name'] != search_fields['name']:
        valid = False
    if search_fields['company'] != ""  and contact['company'] != search_fields['company'] :
        valid = False
    if search_fields['email'] != "" and contact['email'] != search_fields['email']:
        valid = False
    if search_fields['city'] != "" and contact['city'] != search_fields['city']:
        valid = False
    if search_fields['country'] != "" and contact['country'] != search_fields['country'] :
        valid = False
    for job in contact['job_history']:
        if search_fields['job_history'] != "" and job != search_fields['job_history'] :
            valid = False

    return valid


def results_generator(search_fields, contacts):
    results = []
    for contact in contacts:
        if validate_contact(search_fields, contact):
             results.append(contact)
    return results 


@app.route("/results")
def results():
    search_fields = session.get('search_results', None)
    results = results_generator(search_fields, SOCIAL_NETWORK_CONTACTS)
    return render_template('results.html', contacts=results)


@app.route("/SocialNetworkSearch", methods=['GET', 'POST'])
def social_network_search():
    form = ReusableForm(request.form)
 
    if request.method == 'POST':
        name=request.form['name']
        job_history=request.form['job_history']
        company=request.form['company']
        email=request.form['email']
        city=request.form['city']
        country=request.form['country']

        session['search_results'] = {'name':name, 'company':company, 'email':email, 'job_history':job_history, 'city':city, 'country':country}
        print session['search_results']
        if form.validate():
            return redirect(url_for('results'))           
        else:
            flash('All the form fields are required. ')
 
    return render_template('register.html', form=form)
 

SOCIAL_NETWORK_CONTACTS = get_social_network_contacts()


if __name__ == "__main__":    
    app.run()
