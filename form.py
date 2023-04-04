from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import EmailInput


class ContactForm(FlaskForm):
    name = StringField(
        name='name',
        label='Name *',
        render_kw={"placeholder": "name"},
        validators=[DataRequired(message="This field is required.")]
    )
    email = StringField(
        name='email',
        label="Email *",
        render_kw={"placeholder": "email"},
        widget=EmailInput(),
        validators=[DataRequired(message="This field is required."), Email()]
    )
    phone = StringField(
        name='phone',
        label="Phone",
        render_kw={"placeholder": "phone"}
    )
    message = TextAreaField(
        name='message',
        label="Your message *",
        render_kw={"placeholder": "your message"},
        validators=[DataRequired(message="This field is required.")]
    )
