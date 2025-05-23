from wtforms import Form, StringField, PasswordField, validators, DateField, SubmitField
from datetime import date

def validate_future_date(form, field):
    if field.data < date.today():
        raise validators.ValidationError("Date must be in the future")

class RegistrationForm(Form):
    full_name = StringField('Full Name', [validators.DataRequired(), validators.Length(min=2, max=50)])
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=6)])
    submit = SubmitField('Register')

class LoginForm(Form):
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=6)])
    submit = SubmitField('Login')

class SearchForm(Form):
    departure = StringField('Departure City', [validators.DataRequired(), validators.Length(min=3)])
    destination = StringField('Destination City', [validators.DataRequired(), validators.Length(min=3)])
    date = DateField('Date', [validators.DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Search')