import azure.functions as func
import sys

def parseOptions(req: func.HttpRequest, defaultItemList, fileList, itemListExpanded):
	body = req.get_json()
	prefs = {}
	spoilerLog = []
	addedMaps = "Extra Maps: "
	itemRando, itemLogic, npcRando = "", "", ""
	prefs["customSeed"] = body.get('seed')
	prefs["itemRandomization"] = body.get('itemRandomization')
	if prefs["itemRandomization"] == 0:
		itemRando = "None"
	elif prefs["itemRandomization"] == 1:
		itemRando = "Standard"
	elif prefs["itemRandomization"] == 2:
		itemRando = "Expanded"
	if prefs["itemRandomization"] == 3:
		itemRando = "Custom"
		if body.get('customItems') == "":
			print("Error: Custom item pool not specified")
			sys.exit(1)
		else:
			itemList = body.get('customItems').split(",")
	if body.get('customItems') == None:
		itemList = defaultItemList
	prefs["itemLogic"] = body.get('itemLogic')
	if prefs["itemLogic"] == 0:
		itemLogic = "None"
	elif prefs["itemLogic"] == 1:
		itemLogic = "Standard"
	prefs["npcRandomization"] = body.get('npcRandomization')
	if prefs["npcRandomization"] == 0:
		npcRando = "None"
	elif prefs["npcRandomization"] == 1:
		npcRando = "Standard"
	elif prefs["npcRandomization"] == 3:
		npcRando = "Guntsanity"
	if body.get('lspCaveRandomization') == 1:
		prefs["lspCaveRando"] = 1
		fileList.append("overworld_lsp_cave.pak")
		addedMaps += "LSP Cave, "
	if body.get('nightmareCastleRandomization') == 1:
		fileList.append("castle_nightmare_master.pak")
		itemListExpanded.remove("PickupSweater\0\0\0\0\0\0")
		addedMaps += "Nightmare Castle, "
	if body.get('castleBasementRandomization') == 1:
		fileList.append("castle_basement_master.pak")
		addedMaps += "Castle Basement"
	if body.get('spoilerLog') == 1:
		prefs["spoilerLog"] = 1
		logSeed = "seed: " + prefs["customSeed"] + "\n"
		spoilerLog.append(logSeed)
		if (addedMaps.endswith(", ")):
			addedMaps = addedMaps[:-2]
		spoilerLog.append(addedMaps + "\n")
		if prefs["itemRandomization"] != 0:
			spoilerLog.append("Item Randomization: " + itemRando + "\n")
			spoilerLog.append("Item Logic: " + itemLogic + "\n")
		if prefs["npcRandomization"] != 0:
			spoilerLog.append("NPC Randomization: " + npcRando + "\n")
		spoilerLog.append("\n")
	else:
		prefs["spoilerLog"] = 0
	return prefs, spoilerLog, itemList, fileList