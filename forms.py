from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,HiddenField,SelectMultipleField,SelectField,TextAreaField,IntegerField
from wtforms.validators import DataRequired, URL, Email,ValidationError,Length,EqualTo
from wtforms.widgets import ListWidget,CheckboxInput
from flask_ckeditor import CKEditorField

def category_Selected(form,field):
    if not field.data or field.data == 0:
        raise ValidationError("Please select a category.")

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    category = SelectField("Category",coerce=int , validators=[category_Selected],validate_choice=False)
    tags=SelectMultipleField("Tags",coerce=int ,widget=ListWidget(prefix_label=False),option_widget=CheckboxInput())
    submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
    name=StringField("Name",validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password=PasswordField("Password",validators=[DataRequired(),Length(min=8)])
    submit=SubmitField("SIGN ME UP!")
    

class LoginForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    submit=SubmitField("LET ME IN!")


class CommentForm(FlaskForm):
    parent_id=HiddenField()
    comment=TextAreaField("Comments", validators=[DataRequired(),Length(max=300, message="Comment must be 300 characters or fewer.")])
    submit=SubmitField('Submit Comments')

class ProfileForm(FlaskForm):
    name=StringField("Name",validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    bio=TextAreaField("Bio",default="no-bio",validators=[Length(max=600, message="Bio  must be 600 characters or fewer.")])
    submit=SubmitField("Update Profile")

class ContactForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired()])
    email = StringField("Your Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone (Optional)")
    message = TextAreaField("Your Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")

class newsletterForm(FlaskForm):
    email = StringField ("Email",validators=[DataRequired(),Email()])

class reset_emailForm(FlaskForm):
    email = StringField ("Email",validators=[DataRequired(),Email()])
    submit = SubmitField ("Send OTP")

class OTP_Form(FlaskForm):
    otp = StringField("OTP",validators=[DataRequired()])
    submit=SubmitField("Send Otp")

class Password_Form(FlaskForm):
    new_pass = PasswordField("New Password",validators=[DataRequired(),Length(min=8)])
    confirm_pass = PasswordField("Confirm_Password",validators=[DataRequired(),EqualTo('new_pass', message='Passwords must match.')])
    submit=SubmitField("Change Password!")