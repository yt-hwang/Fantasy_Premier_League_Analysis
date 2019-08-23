import json
import urllib
import re
import io
from bs4 import BeautifulSoup
import os

#####################################################################
#	Extract all of the player based information from the website	#
#####################################################################

i = 1
#Open the player file and make it writable
myfile = open("player_history.txt", "w")
myfile.close()

#Create a file to contain all the numbers for which there was errors.
errfile = open("errfile.txt", "w")
errfile.close()

#Website from which to scrape
while i < 700:
	htmltext = urllib.urlopen("http://fantasy.premierleague.com/web/api/elements/" + str(i) + "/")

	#Use a try-except block to ignore htmls that do not relate to players
	try:
		#Use the json command to read in the json file
		data = json.load(htmltext)
		#Extract the score history from the json file
		scoredata = data["fixture_history"]["all"]
		#Extract the player names
		playerdata = data["first_name"] + " " + data["second_name"]
		#Extract player team
		teamname = data["team_name"]
		#Extract player position
		position = data["type_name"]
		#Extract the players price
		price = data["event_cost"]
		#Percentage selected
		selected = data["selected_by"]
		#Open the file using the io.open with encoding='utf8' to counteract irregualr characters
		myfile = io.open("player_history.txt", "a", encoding='utf8')
		
		#Append the data to the file
		for datapoint in scoredata:
			mystring = str(datapoint)
			#Clean the data strings
			mystring1 = mystring.replace("[", "")
			mystring2 = mystring1.replace("u'", "")
			mystring3 = mystring2.replace("]", "")
			mystring4 = mystring3.replace("'", "")
			#Write the data to the file
			myfile.write(mystring4 + "," + playerdata + "," + teamname + "," + position + "," + selected + "," + str(price) + ',' + str(i)  + "\n")
	except:
		#Write all of the numbers for which there was errors to a file
		errfile = open("errfile.txt", "a")
		errfile.write(str(i) + "\n")
		pass
		
	print i
	i += 1

print "Player data scraped"	
#########################################################################
# Extract all of the fixture and result information from the website	#
#########################################################################

#os.remove("fixtures.txt")
base = "http://fantasy.premierleague.com/fixtures/"

#Create a loop to run through the 38 gameweeks
week = 1
fix_file = open('fixtures.txt', 'w')
while week < 39:
	myurl = base + str(week)
	html = urllib.urlopen(myurl).read()
	soup = BeautifulSoup(html)
	fixture_table = soup.find("table", {"class":"ismFixtureTable"})
	#scrape the website for the games played and points
	hometeam = soup.findAll("td", {"class":"ismHomeTeam"})
	awayteam = soup.findAll("td", {"class":"ismAwayTeam"})
	score = soup.findAll("td", {"class":"ismScore"})
	# for point in score:
	# print point.text
	i = 0
	#Keep looping until the code fails
	while True:
		try:
			fix_file.write(str(week) + ',' + hometeam[i].text + ',' + score[i].text + ',' + awayteam[i].text.strip() + ',' + '\n')
			i += 1
		except:
			break
	print week
	week += 1

fix_file.close()

print "Fixture data scraped"

#################################################
#	Extract the league table from the website	#
#################################################

base = "http://fantasy.premierleague.com/transfers/"

html = urllib.urlopen(base).read()
soup = BeautifulSoup(html)
#scrape the website for the games played and points
games_played = soup.findAll("td", {"class":"col-pld"})
points = soup.findAll("td", {"class":"col-pts"})
#create an empty list for team names
team = []

#Find all of the team names and append them to the list
for text in soup.find_all('table', {"class":'leagueTable'}):
	for links in text.find_all('a'):
		team.append(links.text.strip())

league_table = open("league_table.txt", "w")
league_table.close()

league_table = open("league_table.txt", "a")

#print out the league table
i=0
while i < 20:
	league_table.write(str(i+1) + "," + team[i] + "," + games_played[i].text + "," + points[i].text + "\n")
	i +=1

league_table.close()

print "League table scraped"
print "All data scraped"


