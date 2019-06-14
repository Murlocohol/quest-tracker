from bs4 import BeautifulSoup
import requests
import time
import sys
import re

# __What we care about__
# Name
# Link
# Rewards: 	Items
# Gains: 	XP, Reputation
# Faction
# Requires Level
# Level

class Quest:
	def __init__(self, Name, Link, Faction, Req_Level, Level, Reward_Str, Gains_Str):
		self.name = Name
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

	def decode_rewards(self):
		soup = BeautifulSoup(self.reward_str, 'html.parser')
		soup = BeautifulSoup(soup.prettify(), 'html.parser')

		local_list = soup.find_all('td')

		# Table
		for item in local_list:
			item_name = item.find('a').string.strip()
			item_link = 'https://classicdb.ch/' + item.prettify().split('href=\"')[1].split('\">')[0]
			item_tuple = (item_name, item_link)
			self.items.append(item_tuple)


		# print("Rewards decoded")
		return 0

	def decode_gains(self):
		soup = BeautifulSoup(self.gains_str, 'html.parser')
		soup = BeautifulSoup(soup.prettify(), 'html.parser')

		local_list = soup.find_all('li')

		for listicle in local_list:
			item = listicle.prettify().split('<div>')[1].split('</div>')[0]
			if 'experience' in str(item):
				self.experience = int(item.split(' experience')[0])
			if 'Reputation' in item:
				rep_gains = int(item.split(' Reputation')[0])
				rep_faction = BeautifulSoup(item, 'html.parser').find('a').string.strip()
				rep_tuple = (rep_gains, rep_faction)
				self.reputations.append(rep_tuple)

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

	# Properties: name, link, faction, level, required level, experience, items, reputations
	def to_json(self):
		json_name 				= '"name" : "%s",\n' % (self.name)
		json_link 				= '"link" : "%s",\n' % (self.link)
		json_faction 			= '"faction" : "%s",\n' % (self.faction)
		json_level 				= '"level" : %d,\n' % (self.level)
		json_required_level 	= '"required_level" : %d,\n' % (self.req_level)
		
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
			json_rep_array = json_rep_array[:-2] + ']\n'
		else:
			json_rep_array = json_rep_array[:-1] + ']\n'

		return "{" + json_name + json_link + json_faction + json_level + json_required_level + json_item_array + json_rep_array + "}"



def decode_quest(link):
	html = requests.get(link).text

	name 		= html.split('<h1>')[1].split(' -')[0]
	link 		= link
	faction 	= html.split('Side: ')[1].split('</div>')[0]
	# zone		= html.split('Eastern Kingdoms')[1].split('</div>')[0]
	# level 		= int(html.split('Level: ')[1].split('</font>')[0])
	# req_level 	= int(html.split('Requires level: ')[1].split('</div>')[0])

	level 		= int(re.search(r'([\d])\w+', html.split('Level: ')[1]).group(0))
	req_level 	= int(re.search(r'([\d])\w+', html.split('Requires level: ')[1]).group(0))

	reward_str = None
	gains_str = None
	try:
		reward_str 	= html.split('Reward')[1].split('<table class=\"icontab\">')[1].split('</table>')[0]
	except:
		pass
	try:
		gains_str 	= html.split('Gains')[1].split('<ul>')[1].split('</ul>')[0]
	except:
		pass

	q = Quest(name, link, faction, req_level, level, reward_str, gains_str)
	#q.print_details()
	#print(q.to_json())

	# print(q.reward_str)
	# print(q.gains_str)

	return q.to_json()

if __name__ == '__main__':
	HTML = 'https://classicdb.ch/?quest=448'
	decode_quest(HTML)
	
	print('Program ran')