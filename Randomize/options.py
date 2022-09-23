import azure.functions as func
import sys

def parseOptions(req: func.HttpRequest, defaultItemList, fileList, itemListExpanded):
	body = req.get_json()
	prefs = {}
	spoilerLog = []
	prefs["customSeed"] = body.get('seed')
	prefs["itemRandomization"] = body.get('itemRandomization')
	if prefs["itemRandomization"] == 3:
		if body.get('customItems') == "":
			print("Error: Custom item pool not specified")
			sys.exit(1)
		else:
			itemList = body.get('customItems').split(",")
	if body.get('customItems') == None:
		itemList = defaultItemList
	prefs["itemLogic"] = body.get('itemLogic')
	prefs["npcRandomization"] = body.get('npcRandomization')
	if body.get('spoilerLog') == 1:
		prefs["spoilerLog"] = 1
		logSeed = "seed: " + prefs["customSeed"] + "\n \n"
		spoilerLog.append(logSeed)
	else:
		prefs["spoilerLog"] = 0
	if body.get('lspCaveRandomization') == 1:
		prefs["lspCaveRando"] = 1
		fileList.append("overworld_lsp_cave.pak")
	if body.get('nightmareCastleRandomization') == 1:
		fileList.append("castle_nightmare_master.pak")
		itemListExpanded.remove("PickupSweater\0\0\0\0\0\0")
	if body.get('castleBasementRandomization') == 1:
		fileList.append("castle_basement_master.pak")
	return prefs, spoilerLog, itemList, fileList