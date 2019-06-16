from bs4 import BeautifulSoup
import requests
import time
import sys
from datetime import datetime

from quest_parser import decode_quest

#	Functionality
# - Range of points arg option
#

def main(txt_name='valid_quest_list 0-10.txt'):
	TIME_START = time.time()
	valid_links = []
	time_stamp = '%d-%d' % (datetime.now().day, datetime.now().month)
	json_name = txt_name[:-4] + ' ' + time_stamp + ".json"
	json = '{ "data" : [\n'

	print(json_name)

	with open(txt_name) as f:
		for line in f:
			valid_links.append(line)

	# print(valid_links)



	for link in valid_links:
		quest_id = int(link.split('https://classicdb.ch/?quest=')[1][:-1])
		
		print(str(time.time() - TIME_START))

		time_elap = str(time.time() - TIME_START).split('.')
		time_elap = time_elap[0] + '.' + time_elap[1][:3]

		print("Working on Quest %s\t | Time Elapsed: %s" % (quest_id, time_elap))
		quest_id = '"id" : %d,\n' % (quest_id)
		quest_data = '"data" : %s\n' % (decode_quest(link[:-1]))
		json_link = '{' + quest_id + quest_data + '},'
		json = json + json_link
		

	json = json[:-1] + '\n]}'

	f = open(json_name, 'w', encoding='utf-8')
	f.write(json)
	f.close()

	return


if __name__ == '__main__':
	txt_name = 'valid_quest_list 0-10.txt'

	if(len(sys.argv) > 1):
		if(sys.argv[1] and isinstance(str(sys.argv[1]), str)):
			txt_name = str(sys.argv[1])

	main(txt_name)
