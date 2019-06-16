from bs4 import BeautifulSoup
import requests
import time
import sys
import re

class Quest:
	def __init__(self, Name, Link, Faction, Req_Level, Level, Reward_Str, Gains_Str):
		self.name = Name.replace("&#039;", "'")
		self.link = Link
		self.faction = BeautifulSoup(Faction, 'html.parser').string
		self.req_level = Req_Level
		self.level = Level
		self.reward_str = Reward_Str
		self.gains_str = Gains_Str

		# Init rewards
		self.items = []

		# Init gains
		self.experience = 0
		self.reputations = []
		
		if self.reward_str is not None:
			self.decode_rewards()
		if self.gains_str is not None:
			self.decode_gains()

	# TODO: Make formating prettier and reduce BeautifulSoup usage
	def decode_rewards(self):
		soup = BeautifulSoup(self.reward_str, 'html.parser')
		soup = BeautifulSoup(soup.prettify(), 'html.parser')

		local_list = soup.find_all('td')

		# Table
		for item in local_list:
			try:
				item.find('a').string.strip()
				item_name = item.find('a').string.strip()
				item_link = 'https://classicdb.ch/' + item.prettify().split('href=\"')[1].split('\">')[0]
				item_tuple = (item_name, item_link)
				self.items.append(item_tuple)
			except:
				pass
			


		# print("Rewards decoded")
		return 0

	# TODO: Make formating prettier and reduce BeautifulSoup usage
	def decode_gains(self):
		soup = BeautifulSoup(self.gains_str, 'html.parser')
		soup = BeautifulSoup(soup.prettify(), 'html.parser')

		local_list = soup.find_all('li')

		for listicle in local_list:
			try:
				item = listicle.prettify().split('<div>')[1].split('</div>')[0]
				if 'experience' in str(item):
					self.experience = int(item.split(' experience')[0])
				if 'Reputation' in item:
					rep_gains = int(item.split(' Reputation')[0])
					rep_faction = BeautifulSoup(item, 'html.parser').find('a').string.strip()
					rep_tuple = (rep_gains, rep_faction)
					self.reputations.append(rep_tuple)
			except:
				pass

		# print("Gains decoded")
		return 0

	def print_details(self):
		print("\nName: %s | Link: %s" % (self.name, self.link))
		print("Level: %d | Required Level: %d" % (self.level, self.req_level))
		print("Faction: %s" % (self.faction))
		
		print("\n__Items__")
		for item in self.items:
			print("'%s'\t ~%s" % item)

		print("\n__Gains__")
		print("Experience: %s" % (self.experience))
		for rep in self.reputations:
			print("%d\t %s" % rep)

	def to_json(self):
		json_name 				= '"name" : "%s",\n' % (self.name)
		json_link 				= '"link" : "%s",\n' % (self.link)
		json_faction 			= '"faction" : "%s",\n' % (self.faction)
		json_level 				= '"level" : %d,\n' % (self.level)
		json_required_level 	= '"required_level" : %d,\n' % (self.req_level)
		json_experience			= '"experience" : %d,\n' % (self.experience)
		
		json_item_array = '"items" : [\n'
		for item in self.items:
			json_item_array = json_item_array + ('{"name" : "%s", "link" : "%s"},\n' % item)
		if len(self.items) > 0:
			json_item_array = json_item_array[:-2] + '],\n'
		else:
			json_item_array = json_item_array[:-1] + '],\n'

		json_rep_array = '"reputations" : [\n'
		for rep in self.reputations:
			json_rep_array = json_rep_array + ('{"amount" : "%s", "faction" : "%s"},\n' % rep)
		if len(self.reputations) > 0:
			json_rep_array = json_rep_array[:-2] + '\n]'
		else:
			json_rep_array = json_rep_array[:-1] + '\n]'

		return "{" + json_name + json_link + json_faction + json_level + json_required_level + json_experience + json_item_array + json_rep_array + "}"


def grab_until_no_num(str):
	number = ""

	for char in str:
		if char.isnumeric():
			number += char
		else:
			break

	return int(number)


def decode_quest(link):
	html = requests.get(link).text
	html = html.split('class="infobox"')[1]

	name 		= html.split('<h1>')[1].split(' -')[0]
	link 		= link
	faction 	= html.split('Side: ')[1].split('</div>')[0]
	level 		= -1
	req_level 	= -1
	reward_str = None
	gains_str = None
	
	try:
		level 	= grab_until_no_num( html.split('class="infobox"')[1].split('Level: ')[1] )
	except:
		pass

	try:
		req_level 	= grab_until_no_num( html.split('class="infobox"')[1].split('Requires level: ')[1] )
	except:
		pass

	choose_reward_str = None
	receive_reward_str = None

	try:									
		choose_reward_str 	= html.split('You can choose one of these rewards')[1].split('<table class="icontab">')[1].split('</table>')[0]
	except:
		pass

	try:									
		receive_reward_str 	= html.split('You will receive:')[1].split('<table class="icontab">')[1].split('</table>')[0]
	except:
		pass

	try:
		gains_str 	= html.split('<h3>Gains</h3>')[1].split('<ul>')[1].split('</ul>')[0]
	except:
		pass

	if choose_reward_str and receive_reward_str:
		reward_str = choose_reward_str + receive_reward_str
	elif choose_reward_str:
		reward_str = choose_reward_str
	elif receive_reward_str:
		reward_str = receive_reward_str

	return Quest(name, link, faction, req_level, level, reward_str, gains_str).to_json()

if __name__ == '__main__':
	quest_id = 0
	test_html = ''

	if(len(sys.argv) > 1):
		if(sys.argv[1] and isinstance(int(sys.argv[1]), int)):
			START = int(sys.argv[1])

	test_html = 'https://classicdb.ch/?quest=' + str(quest_id)
	

	if test_html is 'https://classicdb.ch/?quest=':
		results = 'Error'
	else:
		results = decode_quest(test_html)
	

	print(results)
	print('Program ran')