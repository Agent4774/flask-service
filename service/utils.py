import os
from hashlib import sha256


def get_pay_sign(data):
		shop_secret_key = os.getenv('SHOP_SECRET_KEY', 'SecretKey01')
		items = [
			data['amount'], 
			data['currency'], 
			data['shop_id'], 
			data['shop_order_id']
		]
		value = ':'.join(items) + shop_secret_key
		return sha256(value.encode('utf-8')).hexdigest()

def get_bill_sign(data):
		shop_secret_key = os.getenv('SHOP_SECRET_KEY', 'SecretKey01')
		items = [
			data['payer_currency'], 
			data['shop_amount'], 
			data['shop_currency'], 
			data['shop_id'], 
			data['shop_order_id']
		]
		value = ':'.join(items) + shop_secret_key
		return sha256(value.encode('utf-8')).hexdigest()

def get_invoice_sign(data):
		shop_secret_key = os.getenv('SHOP_SECRET_KEY', 'SecretKey01')
		items = [
			data['amount'], 
			data['currency'], 
			data['payway'], 
			data['shop_id'], 
			data['shop_order_id']
		]
		value = ':'.join(items) + shop_secret_key
		return sha256(value.encode('utf-8')).hexdigest()