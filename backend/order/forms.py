from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateOrderForm(FlaskForm):
    client_name = StringField('Имя клиента', validators=[DataRequired()])
    submit = SubmitField('Создать заказ')