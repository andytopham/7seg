#!/usr/bin/python
# myubidots.py
# To get ubidots working....
#$ sudo apt-get install python-setuptools
#$ sudo easy_install pip
#$ sudo pip install ubidots

from ubidots import ApiClient
import logging
import keys

LOGFILE = '/home/pi/master/7seg/log/myubidots.log'

class Ubidots():
	def __init__(self):
		self.logger = logging.getLogger(__name__)
		# Ubidots Create an "API" object and variable object
		api = ApiClient(keys.ubidots_api_key)
		self.test_variable = api.get_variable(keys.ubidots_bench_variable_key)
		self.logger.info('Ubidots initialised.')
			
	def write(self, val):
		if True:
			try:
				self.test_variable.save_value({'value':val})
			except:
				self.logger.warning("Error saving to ubidots. Value="+str(val))				

if __name__ == "__main__":
	logging.basicConfig(filename=LOGFILE,filemode='w',level=logging.INFO)
	logging.warning('Running ubidots as a standalone app.')
	myUbidots = Ubidots()
	myUbidots.write(0)		# Test value
	