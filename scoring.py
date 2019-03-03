import tbapy
import math

tba = tbapy.TBA('FsRCtOkFxHEy0mshFOrOXEfru18CkuRl4iKY4XFUsCM12w1BLawDoDVNrTWLHq6N')

week = 1
year = 2019
team_list = [610, 5687, 1577, 1648, 1511, 3646]


def getScoreFromRank(rank):
	score = 0
	if (rank == 1):
		score = 20
	elif (rank >= 2 and rank <= 3):
		score = 12
	elif (rank >= 4 and rank <= 8):
		score = 6
	elif (rank >= 9 and rank <= 12):
		score = 3
	elif (rank >= 13 and rank <= 16):
		score = 2
	return score


def getScoreFromElimResults(team_status):
	score = 0
	if (team_status.playoff != None):
		level = team_status.playoff["level"]
		status = team_status.playoff["status"]
	else:
		level = 'not picked'

	if (level == 'not picked'):
		score = 0
	elif (level == 'f' and status == 'won'):
		score = 30
	elif (level == 'f' and status == 'eliminated'):
		score = 20
	elif (level == 'sf'):
		score = 10
	elif (level == 'qf'):
		score = 4
	return score


def getScoreFromAward(award_type):
	score = 0;
	if (award_type == 0):
		score = 42  # chairmans
		print("Award: Chairmans | Points: " + str(42))
	elif (award_type == 3):
		score = 8  # woodie flowers
		print("Award: Woodie Flowers | Points: " + str(8))
	elif (award_type == 9):
		score = 36  # engineering inspiration
		print("Award: Engineering Inspiration | Points: " + str(36))
	elif (award_type == 10):
		score = 20  # rookie all-star
		print("Award: Rookie All-Star | Points: " + str(20))
	elif (award_type == 15):
		score = 15  # rookie inspiration
		print("Award: Rookie Inspiration | Points: ") + str(15)
	elif (award_type == 14):
		score = 5  # highest rookie seed
		print("Award: Highest Rookie Seed | Points: " + str(5))
	elif (award_type == 13):
		score = 5  # 
		print("Award: Judges | Points: " + str(5))
	elif (award_type == 16 or award_type == 17 or award_type == 20 or award_type == 21 or award_type == 29 or award_type == 71):
		score = 15  # robot-based awards
		print("Award: Robot-based awards | Points: " + str(15))
	elif (award_type == 4):
		score = 4  # deans list
		print("Award: Deans List | Points: " + str(4))
	return score

total_ff_score = 0

print()
print("WEEK " + str(week) + " | " + str(year))
print(team_list)
print()

for team in team_list:
	team_key = 'frc' + str(team)
	events = tba.team_events(team, year)
	for event in events:
		if event.week == (week - 1):
			print(event.name)
			print("TEAM " + str(team))

			team_ff_score = 0
			if (tba.team_status(team, event.key) == None):
				print("NEED MANUAL SCORING")
			elif (tba.team_status(team, event.key).qual == None):
				print("HAS NOT PLAYED YET")
			else: 
				team_status = tba.team_status(team, event.key)
				rank = team_status.qual["ranking"]["rank"]
				total_rp = math.floor(team_status.qual["ranking"]["sort_orders"][0] * team_status.qual["ranking"]["matches_played"])

				print("Points from rank: " + str(getScoreFromRank(rank)))
				team_ff_score += getScoreFromRank(rank)
				print("Points from RP: " + str(total_rp))
				team_ff_score += total_rp
				print("Points from elimination results: " + str(getScoreFromElimResults(team_status)))
				team_ff_score += getScoreFromElimResults(team_status)

				event_awards = tba.event_awards(event.key)
				for award in event_awards:
					for recipient in award["recipient_list"]:
						if (recipient["team_key"] == team_key):
							award_type = award["award_type"]
							# print("Points from awards: " + str(getScoreFromAward(award_type)))
							team_ff_score += getScoreFromAward(award_type)

			print("FF SCORE: " + str(team_ff_score))
			print()
			total_ff_score += team_ff_score

print("TOTAL WEEK " + str(week) + " SCORE: " + str(total_ff_score))
print()
