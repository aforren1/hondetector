import requests
import os

class AlertEmail:

	disabled = False
	mailgun_key = None
	mailgun_domain = None
	address_from = None
	address_to = None

	def __init__(self):
		if 'MAILGUN_API_KEY' not in os.environ:
			self.disabled = True
			print("Cannot instantiate mail library; please set the environment variable MAILGUN_API_KEY and restart hondetector.")
			return
		else:
			self.mailgun_key = os.environ['MAILGUN_API_KEY']

		if 'MAILGUN_DOMAIN' not in os.environ:
			self.disabled = True
			print("Cannot instantiate mail library; please set the environment variable MAILGUN_DOMAIN and restart hondetector.")
			return
		else:
			self.mailgun_domain = os.environ['MAILGUN_DOMAIN']

		if 'HONDETECTOR_EMAIL_FROM' not in os.environ:
			self.disabled = True
			print("Cannot send mail messages; please set the environment variable HONDETECTOR_EMAIL_FROM and restart hondetector.")
			return
		else:
			self.address_from = os.environ['HONDETECTOR_EMAIL_FROM']

		if 'HONDETECTOR_EMAIL_TO' not in os.environ:
			self.disabled = True
			print("Cannot send mail messages; please set the environment variable HONDETECTOR_EMAIL_TO and restart hondetector.")
			return
		else:
			self.address_to = os.environ['HONDETECTOR_EMAIL_TO']

	def sendMessage(self, message):
		if self.disabled == True:
			return

		response = requests.post('https://api.mailgun.net/v3/' + self.mailgun_domain + '/messages',
			auth=("api", self.mailgun_key),
			data={
				"from": self.address_from,
				"to": [self.address_to],
				"subject": "[hondetector] Alert triggered",
				"text": message
			}
		)