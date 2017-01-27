import nexmo
import os

class AlertSMS:

	disabled = False
	number_from = None
	number_to = None
	
	def __init__(self): 

		if 'NEXMO_API_KEY' not in os.environ:
			self.disabled = True
			print("Cannot instantiate SMS library; please set the environment variable NEXMO_API_KEY and restart hondetector.")
			return
			
		if 'NEXMO_API_SECRET' not in os.environ:
			self.disabled = True
			print("Cannot instantiate SMS library; please set the environment variable NEXMO_API_SECRET and restart hondetector.")
			return

		if 'HONDETECTOR_FROM' not in os.environ:
			self.disabled = True
			print("Cannot send SMS messages; please set the environment variable HONDETECTOR_FROM and restart hondetector.")
			return
		else:
			self.number_from = os.environ['HONDETECTOR_FROM']

		if 'HONDETECTOR_TO' not in os.environ:
			self.disabled = True
			print("Cannot send SMS messages; please set the environment variable HONDETECTOR_TO and restart hondetector.")
			return
		else:
			self.number_to = os.environ['HONDETECTOR_TO']


		self.client = nexmo.Client()

	def sendMessage(self, message):
		if sms.disabled == True:
			return

		response = self.sms.send_message({
			'from': self.number_from,
			'to': self.number_to,
			'text': message
		})

		response = response['messages'][0]

		if response['status'] != '0':
			print("Could not send SMS alert: ", response['error-text'])