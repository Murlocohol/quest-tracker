from bs4 import BeautifulSoup
import requests

rep_list = []
gnome_faction = 'https://classicdb.ch/?faction=54#quests'

# Skip if Donation
def get_all_links(original_link):
	valid_hrefs = []

	r = requests.get(original_link)

	# split all hrefs
	href = []

	for href in hrefs:
		# if valid href push to list
		href = []
	
	return valid_hrefs

def push_to_rep_list(list):
	# quest name, min_level, zone, rewards
	# name = h1
	# min = 'requires level:' div in li
	# zone = href
	# rewards = 'gains' 'upon completion of this quest you will gain:' h3 ul

	return 0

def write_rep(list):
	my_doc = ''

	for line in list:
		my_doc.write_to

	close_doc

	return 0

if __name__ == "__main__":
	f = open("rep_file.txt", 'w')

	r = requests.get(gnome_faction)

	pull = BeautifulSoup(r.text, 'html.parser')
	f.write(pull.prettify())
	f.close()

	stringify = pull.prettify()

	part_i_care_about = stringify.split('id="listview-generic"')
	print(part_i_care_about[1])

	listicle = part_i_care_about[1].split('<a')

	#len(listicle - (len(listicle) / 2))
	# print(listicle)

	# raw_list = raw_html.prettify().split('href')

	# for list in raw_list:
	# 	print(list)

	# print(raw_list[2])


