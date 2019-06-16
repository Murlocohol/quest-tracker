from bs4 import BeautifulSoup
import requests
import time

# Return True if link contains data
def link_contains_data(full_http_link):
	r = requests.get(full_http_link)
	soup = BeautifulSoup(r.text, 'html.parser')

	if('This quest doesn\'t exist in our database' in soup.prettify()):
		return False

	return True

if __name__ == "__main__":
	START = 0
	STOP = 1000
	HTTP = 'https://classicdb.ch/?quest='
	valid_link_list = []
	file_name = 'valid_quest_list ' + str(START) + '-' + str(STOP) + '.txt'
	F = open(file_name, 'w', encoding='utf-8')

	index = START

	TIME_START = time.time()
	while index < STOP:
		link = HTTP + str(index)

		if(link_contains_data(link)):
			#print(link)
			valid_link_list.append(link)
			F.write(link + '\n')

		index += 1
	TIME_END = time.time()
	print("Time elapsed: " + str(TIME_END - TIME_START)[0:5])







