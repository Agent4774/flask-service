from .forms import PaymentForm
from service import app
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
def confirm_payment():
		form = PaymentForm()
		if request.method == 'POST':
				data = {}
				for key, value in request.form.items():
						data[key] = value
				if data['currency'] == '978':
						# If currency is EUR
						# Generating sign
						data['sign'] = get_pay_sign(data)
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
						url = 'https://core.piastrix.com/bill/create'
						# Getting service response
						res = requests.post(url, json=data)
						parsed_response = res.json()
						if parsed_response['error_code'] != 0:
								# In case error received
								return render_template(
									'payment.html',
									form=form,
									data=parsed_response['message']
								)
						return redirect(parsed_response['data']['url'])
				if data['currency'] == '643':
						# If currency is RUR
						# Setting pay way
						data['payway'] = 'advcash_rub'
						# Generating sign 
						data['sign'] = get_invoice_sign(data)
						url = 'https://core.piastrix.com/invoice/create'
						res = requests.post(url, json=data)
						parsed_response = res.json()
						if parsed_response['error_code'] != 0:
								# In case error received
								return render_template(
									'payment.html',
									form=form,
									data=parsed_response['message']
								)
						# Another templated rendered for confirmation
						return render_template(
							'confirm_invoice.html', 
							data=parsed_response['data']['data'], 
							method=parsed_response['data']['method'],
							url=parsed_response['data']['url']
						)
		return render_template('payment.html', form=form)