from .forms import PaymentForm
from service import app, db
from service.models import Payment
from flask import (
	render_template, 
	request, 
	redirect
)
from urllib.parse import urlencode
from service.utils import (
	get_pay_sign, 
	get_bill_sign, 
	get_invoice_sign
)
import requests


@app.route('/', methods=['GET', 'POST'])
def payment():
		form = PaymentForm()
		if form.validate_on_submit():
				data = {}
				for key, value in request.form.items():
						data[key] = value
				if data['currency'] == '978':
						# If currency is EUR
						# Generating sign
						data['sign'] = get_pay_sign(data)
						# Adding payment info to database
						payment = Payment(
							amount=data['amount'],
							currency='EUR',
							description=data['description']
						)
						db.session.add(payment)
						db.session.commit()
						# Redirecting to service
						url = 'https://pay.piastrix.com/en/pay'
						return redirect(f'{url}/?{urlencode(data)}')
				if data['currency'] == '840':
						# If currency is USD
						# Setting necessary key-value
						data['shop_amount'] = data.pop('amount')
						data['shop_currency'] = data.pop('currency')
						data['payer_currency'] = data['shop_currency']
						del data['submit']
						# Generating sign
						data['sign'] = get_bill_sign(data)
						# Adding payment info to database
						payment = Payment(
							amount=data['shop_amount'],
							currency='USD',
							description=data['description']
						)
						db.session.add(payment)
						db.session.commit()
						# Getting service response
						url = 'https://core.piastrix.com/bill/create'
						res = requests.post(url, json=data)
						parsed_response = res.json()
						if parsed_response['error_code'] != 0:
								# In case error received
								app.logger.error(parsed_response['message'])
								return render_template(
									'payment.html',
									form=form,
									data='Error! Please, check request data!'
								)
						return redirect(parsed_response['data']['url'])
				if data['currency'] == '643':
						# If currency is RUR
						# Setting pay way
						data['payway'] = 'advcash_rub'
						# Generating sign 
						data['sign'] = get_invoice_sign(data)
						# Adding payment info to database
						payment = Payment(
							amount=data['amount'],
							currency='RUR',
							description=data['description']
						)
						db.session.add(payment)
						db.session.commit()
						# Getting service response
						url = 'https://core.piastrix.com/invoice/create'
						res = requests.post(url, json=data)
						parsed_response = res.json()
						if parsed_response['error_code'] != 0:
								# In case error received
								app.logger.error(parsed_response['message'])
								return render_template(
									'payment.html',
									form=form,
									data='Error! Please, check request data!'
								)
						# Another template rendered for confirmation
						return render_template(
							'confirm_invoice.html', 
							data=parsed_response['data']['data'], 
							method=parsed_response['data']['method'],
							url=parsed_response['data']['url']
						)
		return render_template('payment.html', form=form)