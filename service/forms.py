from flask_wtf import FlaskForm
from wtforms import (
	DecimalField, 
	HiddenField, 
	SelectField, 
	SubmitField, 
	TextAreaField
)
from wtforms.validators import (
	DataRequired, 
	ValidationError
)


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

		def validate_amount(self, amount):
				value = str(amount.data)
				if '.' not in value:
						raise ValidationError('Error! Correct format: 100.00')
				items = value.rsplit('.')
				if len(items[1]) > 2 or len(items[1]) < 2:
						raise ValidationError('Error! Correct format: 100.00')