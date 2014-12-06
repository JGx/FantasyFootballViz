#!python
import nflgame
import json
import csv

class PlayerStats:

	def __init__(self):
		self.stats = {}


	def addSeasons(self, plyr, stat, first_season, last_season):
		if first_season < last_season:
			for x in range(first_season, last_season + 1):
				self.addStats(plyr, stat, x)

	def addStats(self, plyr, stat, season):
		if self.stats == {} or plyr not in self.stats:
			self.stats[plyr]={}
		self.stats[plyr][season] = self.getSeasonStats(plyr, stat, season)

	def write(self, filename):
		jsonf = open(filename,'w') 
		jsonf.write(json.dumps(self.stats))
		jsonf.close()

	def getSeasonStats(self, plyr, stat, season):   
		data = []
		for x in range(1, 18):
			game = nflgame.games(season,week=x)
			players = nflgame.combine_game_stats(game)
			player = players.name(plyr)
			if player is None:
				data.append({'week':str(x),'active':'false'})
			else:
				playerStats = player.stats
				week_obj = {'week':str(x)}
				if(stat == 'all'):
					for x in playerStats:
						week_obj[x] = playerStats[x]
					week_obj['active'] = 'true'
					data.append(week_obj)
				else:
					data.append({'week':str(x),stat:str(playerStats[stat]), 'active':'true'})
		return data


plyrstats = PlayerStats()
plyrstats.addSeasons('P.Manning','all', 2009, 2013)
plyrstats.write("ManningPassing.json")

