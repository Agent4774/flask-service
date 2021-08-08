from service import db
from datetime import datetime


class Payment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	amount = db.Column(db.String(255), nullable=False)
	currency = db.Column(db.String(3), nullable=False)
	description = db.Column(db.Text, nullable=False)
	timestamp = db.Column(db.DateTime, default=datetime.now)

	def __repr__(self):
		return f'Payment({self.amount}, {self.currency}, {self.timestamp})'