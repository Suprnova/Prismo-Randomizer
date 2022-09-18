import random
import time

from fileHandler import readFiles, writeFiles, writeLog

# Builds local item pool while replacing items with placeholder text to be changed into randomized items; placeholder text named to have length of 19
def randomize(fs, prefs, fileList, spoilerLog, itemList, itemLocal, itemListExpanded, NPCList, NPCList2, NPCLocal):
	random.seed(prefs["customSeed"])
	files = readFiles(fs, fileList)
	for key in files:
		lines = files[key]
		areaClean = key.lstrip("\\").rstrip(".pak") + ": \n"
		c = 0
		if prefs["spoilerLog"] == 1:
			spoilerLog.append(areaClean)
		if prefs["itemRandomization"] != 0:
			placeholder = "placeholdertextomg0"
			for location in lines:
				beenHere = c
# This exception about castle_nightmare_master.pak is currently depricated due to args(nightmare-castle-randomization)
#				if area == "\\castle_nightmare_master.pak" and prefs["itemLogic"] != 0:
#					while "PickupSweater\0\0\0\0\0\0" in location:
#						itemLocal.append("PickupSweater\0\0\0\0\0\0")
#						replacement = lines[c].replace("PickupSweater\0\0\0\0\0\0", placeholder, 1)
#						lines[c] = replacement.lstrip('')
#						location = lines[c]
#						print("Added PickupSweater\0\0\0\0\0\0 to item pool")
#						if prefs["spoilerLog"] == 1:
#							spoilerLog.append("PickupSweater\0\0\0\0\0\0 -> ")
# Currently unused shop randomization, functions however other factors in the game prevent it from being usable
#				elif area == "\\global.pak":
#					for item in shopList:
#						while item in location:
#							itemLocal.append(item.ljust(19, "\0"))
#							replacement = lines[c].replace(item, "placeholdertextomg!", 1)
#							lines[c] = replacement.lstrip('')
#							location = lines[c]
#							print("Added ", item, " to item pool")
#							if spoiler is 1:
#								i = item.ljust(19, "\0") + " ->  "
#								spoilerLog.append(i)
#				else:
# Takes items from desired items to be randomized and replaces them with a placeholder while adding them to the item pool
				for item in itemList:
					while item in location:
						placeholder = "placeholdertextomg" + str(beenHere - c)
						itemLocal.append(item.ljust(19))
						replacement = lines[c].replace(item, placeholder, 1)
						lines[c] = replacement.lstrip('')
						location = lines[c]
						print("Added", item, "to item pool")
						if prefs["spoilerLog"] == 1:
							i = item + " ->  "
							spoilerLog.append(i)
						beenHere += 1
				c += 1
			itemLocal.sort()
# Takes NPCs and replaces them with a placeholder while adding them to the item pool
		if prefs["npcRandomization"] != 0:
			c = 0
			NPCListMaster = NPCList + NPCList2
			for location in lines:
				beenHere = c
				for nonplay in NPCListMaster:
					while nonplay in location:
						placeholder = "creatingafiftysevencharacterplaceholderisnotveryfunforme" + str(beenHere - c)
						NPCLocal.append(nonplay)
						replacement = lines[c].replace(nonplay, placeholder)
						lines[c] = replacement.lstrip('')
						location = lines[c]
						print("Added", nonplay[:19], "to NPC pool")
						if prefs["spoilerLog"] == 1:
							n = nonplay[:19] + " ->  "
							spoilerLog.append(n)
						beenHere += 1
				c += 1
			NPCLocal.sort()
# Writing to files
		if prefs["spoilerLog"] == 1:
			spoilerLog.append( "\n")

# Uses expanded item pool if selected
	if prefs["itemRandomization"] == 2:
				while len(itemListExpanded) != 0:
					fillerSpot = itemLocal.index("PickupChestItemKey\0")
					fillerReplace = itemListExpanded[random.randint(0, len(itemListExpanded)-1)]
					replacement = itemLocal[fillerSpot].replace("PickupChestItemKey\0", fillerReplace)
					itemLocal[fillerSpot] = replacement
					itemListExpanded.remove(fillerReplace)
# If Guntsanity is enabled, replaces all NPCs within pool with Gunter
	if prefs["npcRandomization"] == 3:
		c = 0
		for npc in NPCLocal:
			NPCLocal[c] = "Gunter\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_gunter.pak\0\0\0\0\0\0\0\0\0\0\0"
			c += 1
# Replaces placeholders with actual items from local item pool
	for key in files:
		lines = files[key]
		areaClean = key.lstrip("\\").rstrip(".pak") + ": \n"
		flamboTreeList = ["placeholdertextomg0\0\0\0\0\0dry_tree.wf3d", "placeholdertextomg1\0\0\0\0\0dry_tree.wf3d", "placeholdertextomg2\0\0\0\0\0dry_tree.wf3d", "placeholdertextomg3\0\0\0\0\0dry_tree.wf3d", "placeholdertextomg4\0\0\0\0\0dry_tree.wf3d", "placeholdertextomg5\0\0\0\0\0dry_tree.wf3d", "placeholdertextomg6\0\0\0\0\0dry_tree.wf3d", "placeholdertextomg7\0\0\0\0\0dry_tree.wf3d", "placeholdertextomg8\0\0\0\0\0dry_tree.wf3d", "placeholdertextomg9\0\0\0\0\0dry_tree.wf3d"]
		heroRock = "global:forest_pickup_heavy_1.wf3d\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0" + bytes.fromhex("01").decode("latin-1") + "\0\0\0placeholdertextomg"
		c = 0
		s = 0
		for location in lines:
			if prefs["itemLogic"] != 0 and prefs["itemRandomization"] != 0:
# This exception about castle_nightmare_master.pak is to prevent key items from being within Nightmare Castle to allow seeds with logic that randomize this area to be beatable; expanded items are not prevented from being placed here as their inclusion in the pool does not decide a seed's completability; Slammy Hand is prevented from being placed here if LSP cave if randomized to allow for a seed to be completed
				if key == "\\castle_nightmare_master.pak":
					while "placeholdertextomg0" in location:
						length = len(itemLocal)
						randomNumber = random.randint(0, length-1)
						while itemLocal[randomNumber] == "PickupGrabbyHand\0\0\0" or itemLocal[randomNumber] == "PickupHeroGauntlet\0":
							randomNumber = random.randint(0, length-1)
							if prefs["lspCaveRando"] == 1:
								while itemLocal[randomNumber] == "PickupSlammyHand\0\0\0":
									randomNumber = random.randint(0, length-1)
						replacement = lines[c].replace("placeholdertextomg0", itemLocal[randomNumber], 1)
						lines[c] = replacement.lstrip(' ')
						location = lines[c]
#						print("Replaced placeholder with ", itemLocal[randomNumber])
						if prefs["spoilerLog"] == 1:
							for entry in spoilerLog:
								if entry == areaClean:
									s += 1
									logIndex = int(spoilerLog.index(entry) + s)
									logEntry = spoilerLog[logIndex] + itemLocal[randomNumber] + "\n"
									spoilerLog[logIndex] = logEntry
						itemLocal.remove(itemLocal[randomNumber])
# Currently unused shop randomization, functions however other factors in the game prevent it from being usable
#				elif area == "\\global.pak":
#					j = 0
#					while j < 10:
#						tempPlaceholder = "placeholdertextomg" + str(j)
#						while tempPlaceholder in location:
#							length = len(itemLocal)
#							randomNumber = random.randint(0, length-1)
#							replacementItem = itemLocal[randomNumber].rstrip("\0")
#							replacement = lines[c].replace("placeholdertextomg!",replacementItem, 1)	
#							lines[c] = replacement.lstrip(' ')
#							location = lines[c]
#							print("Replaced placeholder with ", itemLocal[randomNumber])
#							if spoiler is 1:
#								for entry in spoilerLog:
#									if entry == areaClean:
#										s += 1
#										logIndex = int(spoilerLog.index(entry) + s)
#										logEntry = spoilerLog[logIndex] + itemLoca[randomNumber] + "\n"	
#										spoilerLog[logIndex] = logEntry
#							itemLocal.remove(itemLocal[randomNumber])
#						j += 1

# Exception for Grabby Hand and Flambo under dead bushes
				for fireTrees in flamboTreeList:
					while fireTrees in location:
						j = 0
						while j < 10:
							tempPlaceholder = "placeholdertextomg" + str(j)
							while tempPlaceholder in location:
								length = len(itemLocal)
								randomNumber = random.randint(0, length-1)
								while itemLocal[randomNumber] == "PickupGrabbyHand\0\0\0" or itemLocal[randomNumber] == "PickupFlambo\0\0\0\0\0\0\0":
									randomNumber = random.randint(0, length-1)
								replacement = lines[c].replace(tempPlaceholder, itemLocal[randomNumber], 1)
								lines[c] = replacement.lstrip(' ')
								location = lines[c]
								print("Replaced placeholder with", itemLocal[randomNumber])
								print("Dry tree worky")
								if prefs["spoilerLog"] == 1:
									for entry in spoilerLog:
										if entry == areaClean:
											s += 1
											logIndex = int(spoilerLog.index(entry) + s)
											logEntry = spoilerLog[logIndex] + itemLocal[randomNumber] + "\n"
											spoilerLog[logIndex] = logEntry
							j += 1
# Exception for Billy's Gauntlets under huge rocks
				while heroRock in location:
					j = 0
					while j < 10:
						tempPlaceholder = "placeholdertextomg" + str(j)
						while tempPlaceholder in location:
							length = len(itemLocal)
							randomNumber = random.randint(0, length-1)
							while itemLocal[randomNumber] == "PickupHeroGauntlet\0":
								randomNumber = random.randint(0, length-1)
							replacement = lines[c].replace(tempPlaceholder, itemLocal[randomNumber], 1)
							lines[c] = replacement.lstrip(' ')
							location = lines[c]
							print("Replaced placeholder with", itemLocal[randomNumber])
							print("Heavy rock worky")
							if prefs["spoilerLog"] == 1:
								for entry in spoilerLog:
									if entry == areaClean:
										s += 1
										logIndex = int(spoilerLog.index(entry) + s)
										logEntry = spoilerLog[logIndex] + itemLocal[randomNumber] + "\n"
										spoilerLog[logIndex] = logEntry
						j += 1
# Item replacement with no exceptions
			if prefs["itemRandomization"] != 0:
				j = 0
				while j < 10:
					tempPlaceholder = "placeholdertextomg" + str(j)
					while tempPlaceholder in location:
						length = len(itemLocal)
						randomNumber = random.randint(0, length-1)
						replacement = lines[c].replace(tempPlaceholder, itemLocal[randomNumber], 1)
						lines[c] = replacement.lstrip(' ')
						location = lines[c]
						print("Replaced placeholder with", itemLocal[randomNumber])
						if prefs["spoilerLog"] == 1:
							for entry in spoilerLog:
								if entry == areaClean:
									s += 1
									logIndex = int(spoilerLog.index(entry) + s)
									logEntry = spoilerLog[logIndex] + itemLocal[randomNumber] + "\n"
									spoilerLog[logIndex] = logEntry
						itemLocal.remove(itemLocal[randomNumber])
					j += 1
			c += 1
# NPC randomization, uses similar code to the item replacement without exceptions but with a different placeholder
		if prefs["npcRandomization"] != 0:
			c = 0
			for location in lines:
				j = 0
				while j < 10:
					tempPlaceholder = "creatingafiftysevencharacterplaceholderisnotveryfunforme" + str(j)
					while tempPlaceholder in location:
						length = len(NPCLocal)
						randomNumber = random.randint(0, length-1)
						replacement = lines[c].replace(tempPlaceholder, NPCLocal[randomNumber], 1)
						lines[c] = replacement.lstrip(' ')
						location = lines[c]
						print("Replaced placeholder with", NPCLocal[randomNumber][:19])
						if prefs["spoilerLog"] == 1:
							for entry in spoilerLog:
								if entry == areaClean:
									s += 1
									logIndex = int(spoilerLog.index(entry) + s)
									logEntry = spoilerLog[logIndex] + NPCLocal[randomNumber][:19] + "\n"
									spoilerLog[logIndex] = logEntry
						NPCLocal.remove(NPCLocal[randomNumber])
					j += 1
				c += 1
	identifier = str(round(time.time() * 1000))
	writeFiles(fs, files, identifier)
	print("Your seed is: ", prefs["customSeed"])
	if prefs["spoilerLog"] == 1:
		writeLog(fs, spoilerLog, identifier)
	return