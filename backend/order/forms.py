from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateOrderForm(FlaskForm):
    client_name = StringField('Имя клиента', validators=[DataRequired()])
    submit = SubmitField('Создать заказ')


class AddToStorageForm(FlaskForm):
    count = IntegerField('количество продукта', validators=[DataRequired()])
    submit = SubmitField('Добавить на склад')