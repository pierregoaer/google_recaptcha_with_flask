import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_mail import Message, Mail
from form import ContactForm
from datetime import datetime
import requests

# Create Flask app
app = Flask(__name__, static_folder='static', static_url_path='')

# Initialize app
# This is a demo app, variables should be saved as environment variables and accessed with os.environ['VARIABLE_NAME']
app.config['SECRET_KEY'] = 'my_secret_key'

# Set up email notification for new form submissions
EMAIL_SENDER = 'XXXXXXXXX'
app.config['MAIL_SERVER'] = 'email_server'
app.config['MAIL_PORT'] = 'email_port'
app.config['MAIL_USERNAME'] = EMAIL_SENDER
app.config['MAIL_PASSWORD'] = 'email_password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Add as many recipients as needed here
EMAIL_RECIPIENT_1 = 'XXXXXXXXX'
EMAIL_RECIPIENT_2 = 'XXXXXXXXX'

mail = Mail(app)

# Configure Google reCaptcha, visit https://www.google.com/recaptcha/about/ to create site key and secret key
GOOGLE_RECAPTCHA_SITE_KEY = 'site_key_here'
GOOGLE_RECAPTCHA_SECRET_KEY = 'secret_key_here'
# Google URL for verification
GOOGLE_RECAPTCHA_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'


@app.route('/', methods=["POST", "GET"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        secret_response = request.form['g-recaptcha-response']
        verify_response = requests.post(
            url=f'{GOOGLE_RECAPTCHA_VERIFY_URL}?secret={GOOGLE_RECAPTCHA_SECRET_KEY}&response={secret_response}').json()

        # Check Google response. If success == False or score < 0.5, most likely a robot -> abort
        if not verify_response['success'] or verify_response['score'] < 0.5:
            abort(401)

        # if success and score ok -> send email notification for new form submission
        today = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        message = form.message.data

        # Send email notification
        html = f"New form submission received!<br>" \
               f"<br>" \
               f"Date : {today}<br>" \
               f"Name : {name}<br>" \
               f"Email : {email}<br>" \
               f"Phone : {phone}<br>" \
               f"Message : {message}<br><br>"
        msg = Message(
            subject='New Contact Form Received',
            html=html,
            sender=('Your display name here', app.config['MAIL_USERNAME']),
            # pass recipients as a list (best to use env variables to not disclose email addresses here)
            recipients=[EMAIL_RECIPIENT_1, EMAIL_RECIPIENT_2]
        )
        mail.send(msg)
        flash(f"Your message was sent successfully", category='info')
    return render_template('contact.html', form=form, site_key=GOOGLE_RECAPTCHA_SITE_KEY)


if __name__ == "__main__":
    app.run(debug=True)
