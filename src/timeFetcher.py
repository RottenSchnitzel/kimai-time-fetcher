import requests
import sched, time
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

s = sched.scheduler(time.time, time.sleep)

load_dotenv()
beginning = ""

def fetchTime(sc):
	global beginning
	
	Header = {"X-AUTH-USER": os.getenv('USER_NAME'), "X-AUTH-TOKEN": os.getenv('USER_TOKEN')}
	response = requests.get(os.getenv('KIMAI_API_LINK'), headers=Header)
	if response.status_code == 200:
		beginning = response.json()
		if beginning:
			beginning = beginning[0]['begin'].replace("T","-")
	else:
		beginning = response.status_code

	sc.enter(5, 1, fetchTime, (sc,))

def getTime(sc):
	global beginning
	
	if beginning == 403:
		print("403: Forbidden")
		return
	elif not isinstance(beginning, str) and not isinstance(beginning, list):
		print(beginning)
		return

	if not beginning:
		output = "NaN"
	else:
		_beginning = datetime.strptime(beginning, "%Y-%m-%d-%H:%M:%S%z").replace(microsecond=0)
		_current = datetime.now(timezone.utc).replace(microsecond=0)

		output = str(_current - _beginning)

	f = open(os.getenv('OUTPUT_PATH'), "w")
	f.write(output)
	f.close()
	
	sc.enter(1, 1, getTime, (sc,))

if __name__ == '__main__':
	s.enter(1, 1, fetchTime, (s,))
	s.enter(1, 1, getTime, (s,))
	s.run()
