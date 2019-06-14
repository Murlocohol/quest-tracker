from bs4 import BeautifulSoup
import requests
import time
import sys

from quest_parser import decode_quest


def main(txt_name='valid_quest_list 0-10.txt'):
	TIME_START = time.time()
	valid_links = []
	json = "{"

	with open(txt_name) as f:
		for line in f:
			valid_links.append(line)

	print(valid_links)

	for link in valid_links:
		quest_id = link.split('https://classicdb.ch/?quest=')[1][:-1]
		print("Working on Quest %s\t | Time Elapsed: %s" % (quest_id, str(time.time() - TIME_START)[:5]))
		json_link = '"%s" : %s,\n' % (quest_id, decode_quest(link[:-1]))
		json = json + json_link
		

	json = json[:-2] + '}'

	json_name = txt_name[:-4] + ".json"
	f = open(json_name, 'w', encoding='utf-8')
	f.write(json)
	f.close()

	return


if __name__ == '__main__':
	txt_name = 'valid_quest_list 0-10000.txt'

	if(len(sys.argv) > 1):
		if(sys.argv[1] and isinstance(str(sys.argv[1]), int)):
			txt_name = str(sys.argv[1])

	main(txt_name)
