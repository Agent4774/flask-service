import requests
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


@app.route('/', methods=['GET', 'POST'])
def confirm_payment():
		if request.method == 'POST':
				data = {}
				for key, value in request.form.items():
						data[key] = value
				if data['currency'] == '978':
						data['sign'] = get_pay_sign(data)
						url = 'https://pay.piastrix.com/en/pay'	
						return redirect(f'{url}/?{urlencode(data)}')
				if data['currency'] == '840':
						data['shop_amount'] = data.pop('amount')
						data['shop_currency'] = data.pop('currency')
						data['payer_currency'] = data['shop_currency']
						data['sign'] = get_bill_sign(data)
						url = 'https://core.piastrix.com/bill/create'
						res = requests.post(url, json=data).json()
						if res['error_code'] != 0:
								return render_template(
									'payment.html',
									data='Error! Please, check if request data is correct!'
								)
						return redirect(res['data']['url'])
				if data['currency'] == '643':
						data['payway'] = 'advcash_rub'
						data['sign'] = get_invoice_sign(data)
						url = 'https://core.piastrix.com/invoice/create'
						res = requests.post(url, json=data).json()
						if res['error_code'] != 0:
								return render_template('payment.html', data='Error! Please, check if request data is correct!')
						return render_template(
							'confirm_invoice.html', 
							data=res['data']['data'], 
							method=res['data']['method'],
							url=res['data']['url']
						)
		return render_template('payment.html')