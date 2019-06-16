from bs4 import BeautifulSoup
import requests
import time
import sys
import re

class Quest:
	def __init__(self, Name, Link, Faction, Req_Level, Level, Reward_Str, Gains_Str, Start_NPC_Str, End_NPC_Str):
		self.name = Name.replace("&#039;", "'")
		self.link = Link
		self.faction = BeautifulSoup(Faction, 'html.parser').string
		self.req_level = Req_Level
		self.level = Level


		# Init rewards
		self.items = []	# (name, link)

		# Init gains
		self.experience = 0
		self.reputations = []	# (name, amount)

		# Init quest NPCs
		self.start_npc = ()	# (name, link)
		self.end_npc = ()	# (name, link)
		
		# TODO: Eliminate useless aditional data
		self.reward_str = Reward_Str
		self.gains_str = Gains_Str
		self.start_npc_str = Start_NPC_Str
		self.end_npc_str = End_NPC_Str

		if self.reward_str is not None:
			self.decode_rewards()
		if self.gains_str is not None:
			self.decode_gains()

		if self.start_npc_str is not None:
			self.decode_quest_giver()
		if self.end_npc_str is not None:
			self.decode_quest_turn_in()

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

# 	Start NPC:
#                                 <a href="?npc=10926"
#                                                                                         >Pamela Redpath
# End NPC: <a href="?npc=10926">Pamela Redpath

	def decode_quest_giver(self):
		npc_name = self.start_npc_str.split('>')[1]
		npc_link = 'https://classicdb.ch/' + self.start_npc_str.split('href="')[1].split('"')[0]

		self.start_npc = (npc_name, npc_link)

		return 0



	def decode_quest_turn_in(self):
		npc_name = self.end_npc_str.split('>')[1]
		npc_link = 'https://classicdb.ch/' + self.end_npc_str.split('href="')[1].split('">')[0]

		self.end_npc = (npc_name, npc_link)

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
		
		json_start_npc			=	'"start_npc" : [],\n'
		json_end_npc			=	'"end_npc" : [],\n'

		if self.start_npc is not None:
			json_start_npc			=	'"start_npc" : {"name" : "%s", "link" : "%s"},\n' % self.start_npc
		if self.end_npc is not None:
			json_end_npc			=	'"end_npc" : {"name" : "%s", "link" : "%s"},\n' % self.end_npc

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

		return "{" + json_name + json_link + json_faction + json_level + json_required_level + json_experience + json_start_npc + json_end_npc + json_item_array + json_rep_array + "}"


def grab_until_no_num(str):
	number = ""

	for char in str:
		if char.isnumeric():
			number += char
		else:
			break

	return int(number)

def examine_html(raw_html):
	f = open('the_html.html', 'w', encoding='utf-8')
	f.write(raw_html)
	f.close()

	return 0

def decode_quest(link):
	# print(link)
	html = requests.get(link).text
	# examine_html(html)
	html = html.split('<table class="infobox">')[1]

	name 		= html.split('<h1>')[1].split('</h1>')[0]
	link 		= link
	faction 	= html.split('Side: ')[1].split('</div>')[0]
	level 		= -1
	req_level 	= -1
	reward_str = None
	gains_str = None
	start_npc_str = None
	end_npc_str = None
	
	try:
		level 	= grab_until_no_num( html.split('Level: ')[1] )
	except:
		pass

	try:
		req_level 	= grab_until_no_num( html.split('Requires level: ')[1] )
	except:
		pass

	try:
		start_npc_str 	= html.split('Start: ')[1].split('</a>')[0]
	except:
		pass

	try:
		end_npc_str 	= html.split('End: ')[1].split('</a>')[0]
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

	quest = Quest(name, link, faction, req_level, level, reward_str, gains_str, start_npc_str, end_npc_str)

	return quest.to_json()

if __name__ == '__main__':
	quest_id = 0
	test_html = ''

	if(len(sys.argv) > 1):
		if(sys.argv[1] and isinstance(int(sys.argv[1]), int)):
			quest_id = int(sys.argv[1])

	test_html = 'https://classicdb.ch/?quest=' + str(quest_id)
	

	if test_html is 'https://classicdb.ch/?quest=':
		results = 'Error'
	else:
		results = decode_quest(test_html)
	

	print(results)
	print('Program ran')