from iqoptionapi.api import IQOptionApi
import logging
import random
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
Iq=IQOptionApi("email","password")
Iq.connect()#connect to iqoption
ALL_Asset=Iq.get_all_open_time()