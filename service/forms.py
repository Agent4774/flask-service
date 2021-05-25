from flask_wtf import FlaskForm
from wtforms import (
	DecimalField, 
	HiddenField, 
	SelectField, 
	SubmitField, 
	TextAreaField
)
from wtforms.validators import DataRequired


class PaymentForm(FlaskForm):
		amount = DecimalField(
			'Amount:', 
			validators=[DataRequired()], 
			default=10.00
		)
		currency = SelectField(
			'Currency:', 
			choices=[
				('978', 'EUR'), 
				('840', 'USD'), 
				('643', 'RUR')
			]
		)
		description = TextAreaField(
			'Description:', 
			validators=[DataRequired()], 
			default='Test invoice'
		)
		shop_id = HiddenField(default='5')
		shop_order_id = HiddenField(default='101')
		submit = SubmitField('Pay')