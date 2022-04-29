from cortex import Cortex
import time


class Record():
	def __init__(self, user):
		self.c = Cortex(user, debug_mode=True)
		self.c.do_prepare_steps()

	def create_record_then_export(self,
								record_name,
								record_description,
								record_length_s,
								record_export_folder,
								record_export_data_types,
								record_export_format,
								record_export_version):
		
		self.c.create_record(record_name,
							record_description)

		self.wait(record_length_s)

		self.c.stop_record()

		self.c.disconnect_headset()

		self.c.export_record(record_export_folder,
							record_export_data_types,
							record_export_format,
							record_export_version,
							[self.c.record_id])


	def wait(self, record_length_s):
		print('start recording -------------------------')
		length = 0
		while length < record_length_s:
			print('recording at {0} s'.format(length))
			time.sleep(1)
			length+=1
		print('end recording -------------------------')

# -----------------------------------------------------------
# 
# SETTING
# 	- replace your license, client_id, client_secret to user dic
# 	- specify infor for record and export
# 	- connect your headset with dongle or bluetooth, you should saw headset on EmotivApp
#
# RESULT
# 	- export result should be csv or edf file at location you specified
# 	- in that file will has data you specified like : eeg, motion, performance metric and band power
# 
# -----------------------------------------------------------


def get_record(record_name, record_description, record_export_folder, record_length_s):
	user = {
		"license" : "69b505f1-f0ab-4e6a-bf12-da3634e094a9",
		"client_id" : "GvbzHa8GxlzPeg82Hj4oblYh2OGsTwuR2ydcD4Kn",
		"client_secret" : "A2GB2IFTtNdXYIWJMuuJuJaiRSfi0DlFVPTpf"
						  "JhylQIRaSj0GwtbaazGJFQQTaPHBXgLDq1rkfdi4DfNXNTEQHhUhNrmDVZMJw6MdFKXMUx8pShJPnhu1Iod9f406l2N",
		"debit" : 100
	}

	r = Record(user)

	# export parameters
	# https://emotiv.gitbook.io/cortex-api/records/exportrecord
	record_export_data_types = ['EEG', 'PM', 'BP']	# ['EEG', 'MOTION', 'PM', 'BP']
	record_export_format = 'CSV'
	record_export_version = 'V2'

	# start record --> stop record --> disconnect headset --> export record
	r.create_record_then_export(record_name,
								record_description,
								record_length_s,
								record_export_folder,
								record_export_data_types,
								record_export_format,
								record_export_version )
	# -----------------------------------------------------------
