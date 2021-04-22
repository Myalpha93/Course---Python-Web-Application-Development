from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Este usuario ya existe, prueba uno diferente')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Este correo ya existe, prueba uno diferente')

    username = StringField(label='Username',validators=
    [Length(min=6,max=30),DataRequired()])
    email_address = StringField(label='Email Address',validators=[Email(),DataRequired()])
    password1 = PasswordField(label='Password',validators=[Length(min=6,max=60),DataRequired()])
    password2 = PasswordField(label='Repeat password',validators=[Length(min=6,max=60),EqualTo('password1'),DataRequired()])
    submit = SubmitField(label='Crear usuario')

class LoginForm(FlaskForm):
    username = StringField(label='Username',validators=
    [DataRequired()])
    password = PasswordField(label='Password',validators=[DataRequired()])
    submit = SubmitField(label='Iniciar Sesión')

class ComprarProducto(FlaskForm):
    submit = SubmitField(label='Comprar Producto')

class VenderProducto(FlaskForm):
    submit = SubmitField(label='Vender Producto')