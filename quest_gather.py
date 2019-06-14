import requests
import time
import sys

# Return True if link contains data
def link_contains_data(full_http_link):
	r = requests.get(full_http_link)

	if('This quest doesn\'t exist in our database' in r.text):
		return False

	return True

def run(time_s=time.time(), start=0, stop=10):
	http = 'https://classicdb.ch/?quest='
	valid_link_list = []
	file_name = 'valid_quest_list ' + str(start) + '-' + str(stop) + '.txt'
	f = open(file_name, 'w', encoding='utf-8')

	index = start
	while index < stop:
		link = http + str(index)
		if(link_contains_data(link)):
			valid_link_list.append(link)
			f.write(link + '\n')
			print("Found One: %s\t at %s" % (link, str(time.time() - time_s)[0:5]))
		index += 1
	
	f.close()
	return
	

if __name__ == "__main__":
	START = 0
	STOP = 10

	if(len(sys.argv) > 1):
		if(sys.argv[1] and isinstance(int(sys.argv[1]), int)):
			START = int(sys.argv[1])

		if(sys.argv[2] and isinstance(int(sys.argv[2]), int)):
			STOP = int(sys.argv[2])

	TIME_START = time.time()
	run(start=START, stop=STOP)
	TIME_END = time.time()
	print("Time elapsed: " + str(TIME_END - TIME_START)[0:5])






