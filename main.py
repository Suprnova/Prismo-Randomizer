import argparse
import os

from azure.storage.file import FileService
from dotenv import load_dotenv
from options import parseOptions
from randomizer import randomize

load_dotenv()

fs = FileService(account_name=os.getenv('AZURE_FILESHARE_NAME'), account_key=os.getenv('AZURE_FILESHARE_KEY'))
prefs = {}

# List of files to be randomized within data folder
fileList = ["overworld_forest_cave.pak", "overworld_forest_cave_2.pak", "overworld_forest_master.pak", "overworld_iceking_cave.pak",
			"overworld_kingdom_master.pak", "overworld_mountain_cave_1.pak", "overworld_mountain_cave_3.pak", "overworld_mountain_cave_4.pak", "overworld_mountain_master.pak", "overworld_swamp_master.pak",
			"overworld_wasteland_cave_1.pak", "temple_dream_master.pak", "temple_fear_master.pak", "temple_song_master.pak"]

# Files that could be in fileList but are currently excluded
#fileListExtras = ["\\castle_nightmare_master.pak", "\\global.pak", "\\overworld_lsp_cave.pak", "\\castle_basement_master.pak"]

# Used for debugging, lists most files within data folder to scout for files that can be added to pooling and randomizing but aren't due to lack of items or NPCs
#fileListComplete = ["\\arena_hairapes.pak", "\\autoload.pak", "\\15boss_crabdemon.pak", "\\boss_hairapes.pak", "\\boss_nightmare.pak", "\\boss_shadowfinn.pak", "\\castle_basement_master.pak",
#			"\\castle_nightmare_master.pak", "\\caves.pak", "\\dreamtemple.pak", "\\fearcastle.pak", "\\feartemple.pak", "\\gym_crabdemon.pak", "\\gym_nprincess.pak",
#			"\\gym_quests.pak", "\\gym_shadowfinn.pak", "\\npc_choose_goose.pak", "\\npc_coalman.pak", "\\npc_iceking.pak", "\\npc_magicman.pak", "\\npc_marceline.pak", "\\npc_mr_pig.pak",
#			"\\npc_partypat.pak", "\\npc_potteryshopguy.pak", "\\npc_rattleballs.pak", "\\npc_shelby.pak", "\\npc_starchy.pak", "\\npc_treetrunks.pak", "\\overworld.pak", "\\overworld_forest.pak",
#			"\\overworld_forest_cave.pak", "\\overworld_forest_cave_2.pak", "\\overworld_forest_master.pak", "\\overworld_iceking_cave.pak", "\\overworld_kingdom.pak", "\\overworld_kingdom_cave_01.pak",
#			"\\overworld_kingdom_master.pak", "\\overworld_lsp_cave.pak", "\\overworld_mountain.pak", "\\overworld_mountain_cave_1.pak", "\\overworld_mountain_cave_2.pak", "\\overworld_mountain_cave_3.pak",
#			"\\overworld_mountain_cave_4.pak", "\\overworld_mountain_master.pak", "\\overworld_swamp.pak", "\\overworld_swamp_master.pak", "\\overworld_wasteland_cave_1.pak", "\\songtemple.pak",
#			"\\temple_dream_master.pak", "\\temple_fear_master.pak", "\\temple_song_master.pak", "\\temples.pak"]

# List of items to check randomization; Null char added to each entry to maintain a consistent length of 19
defaultItemList = ["PickupChestItemKey\0", "PickupTreasureHuge\0", "PickupTrailMix\0\0\0\0\0", "PickupSpareThumps\0\0", "PickupTrailMix3\0\0\0\0", "PickupMeat\0\0\0\0\0\0\0\0\0", "PickupHeartPiece\0\0\0", 
			"PickupPencil\0\0\0\0\0\0\0", "PickupSweater\0\0\0\0\0\0", "PickupMapPaper\0\0\0\0\0", "PickupChestItemRBK\0", "PickupTreasureSmall", "PickupTreasureBig\0\0",
			"PickupGumGlobe\0\0\0\0\0", "PickupWoodPlank\0\0\0\0", "PickupPlasticBag\0\0\0", "PickupFruitStack\0\0\0", "PickupHeroGauntlet\0", "PickupTrailMix1\0\0\0\0", "PickupTrailMix2\0\0\0\0", "PickupTrailMix4\0\0\0\0", "PickupGrabbyHand\0\0\0"]
	
# List of items that work when put into the game, however are not found to be pooled as well as are not worth putting into itemsListExpanded
itemListUnused = ["PickupNutStack\0\0\0\0\0", "PickupJake\0\0\0\0\0\0\0\0\0"]

# Items that are found on in bushes and pots. Although their placements that would be replaced are consistent, they are separated into a different item list so that the user may toggle them off
itemListExtras = ["PickupHealthOne\0\0\0\0", "PickupFruits\0\0\0\0\0\0\0", "PickupDemonHeart\0\0\0", "PickupNuts\0\0\0\0\0\0\0\0\0", "PickupPieFairy\0\0\0\0\0"]

# List of items to be removed in favor of items from itemListExpanded while using expanded item pool; Currently depricated in favor of replacing PickupChestItemKey as they are entirely useless outside of dungeons
itemListReplaced = ["PickupTreasureSmall", "PickupTreasureBig\0\0", "PickupDemonHeart\0\0\0", "PickupNuts\0\0\0\0\0\0\0\0\0", "PickupFruits\0\0\0\0\0\0\0"]

# Items that could be added to the item pool, but are not found within the game via current methods or are only found in the shop, which can't currently be randomized. Used for expanded item pool
itemListExpanded = ["PickupFlambo\0\0\0\0\0\0\0", "PickupBananarang\0\0\0", "PickupLadyRing\0\0\0\0\0", "PickupSlammyHand\0\0\0", "PickupSweater\0\0\0\0\0\0", "PickupLoveNote\0\0\0\0\0", "PickupHeatSignature", "PickupMindGames\0\0\0\0", "PickupFanfiction\0\0\0", "PickupEnergyDrink\0\0", "PickupBugMilk\0\0\0\0\0\0", "PickupEnchiridion\0\0"]

# List of all items that can be toggled on and off when using custom item pool
itemListCustom = ["PickupTreasureSmall", "PickupTreasureBig\0\0", "PickupTreasureHuge\0", "PickupPencil\0\0\0\0\0\0\0", "PickupMapPaper\0\0\0\0\0", "PickupChestItemKey\0", "PickupChestItemRBK\0",
				  "PickupPlasticBag\0\0\0", "PickupTrailMix\0\0\0\0\0", "PickupTrailMix1\0\0\0\0", "PickupTrailMix2\0\0\0\0", "PickupTrailMix3\0\0\0\0", "PickupTrailMix4\0\0\0\0",  "PickupSpareThumps\0\0", 
				  "PickupHeartPiece\0\0\0", "PickupGumGlobe\0\0\0\0\0", "PickupWoodPlank\0\0\0\0", "PickupFruits\0\0\0\0\0\0\0", "PickupFruitStack\0\0\0", "PickupNuts\0\0\0\0\0\0\0\0\0", "PickupDemonHeart\0\0\0", "PickupHealthOne\0\0\0\0",
				  "PickupBananarang\0\0\0", "PickupGrabbyHand\0\0\0", "PickupFlambo\0\0\0\0\0\0\0", "PickupHeroGauntlet\0", "PickupLadyRing\0\0\0\0\0", "PickupSlammyHand\0\0\0", "PickupSweater\0\0\0\0\0\0",  
				  "PickupLoveNote\0\0\0\0\0", "PickupHeatSignature", "PickupMindGames\0\0\0\0", "PickupFanfiction\0\0\0", "PickupEnergyDrink\0\0", "PickupBugMilk\0\0\0\0\0\0", "PickupEnchiridion\0\0"]

# List of NPCs to check randomization; Null char added to each entry to maintain consistent length of 57
NPCList = ["Gunter\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_gunter.pak\0\0\0\0\0\0\0\0\0\0\0", "PartyPat\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_partypat.pak\0\0\0\0\0\0\0\0\0", "Demon\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_nightospheredemon.pak"
		   "TinyManticore\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_manticore.pak\0\0\0\0\0\0\0\0", "Rattleballs\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_rattleballs.pak\0\0\0\0\0\0", "IceKing\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_iceking.pak\0\0\0\0\0\0\0\0\0\0",
		   "Shelby\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_shelby.pak\0\0\0\0\0\0\0\0\0\0\0", "MrPig\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_mr_pig.pak\0\0\0\0\0\0\0\0\0\0\0", "TreeTrunks\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_treetrunks.pak\0\0\0\0\0\0\0"
		   "MagicMan\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_magicman.pak\0\0\0\0\0\0\0\0\0", "Stanley\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_stanely.pak\0\0\0\0\0\0\0\0\0\0", "Witch\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_witch.pak\0\0\0\0\0\0\0\0\0\0\0\0"
		   "CoalMan\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_coalman.pak\0\0\0\0\0\0\0\0\0\0", "WizardTheif\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_wizardthief.pak\0\0\0\0\0\0"]

# List of certain NPCs in their hex values, due to a bug that has them not be found with the method used in NPCList
NPCList2 = [bytes.fromhex("44656D6F6E0000000000000000000000000000000000000000000000000000006E70635F6E696768746F73706865726564656D6F6E2E70616B").decode("latin-1"), # Nightosphere Demon entry in NPCList
			bytes.fromhex("54696E794D616E7469636F7265000000000000000000000000000000000000006E70635F6D616E7469636F72652E70616B0000000000000000").decode("latin-1"), # Tiny Manticore entry in NPCList
			bytes.fromhex("4D616769634D616E0000000000000000000000000000000000000000000000006E70635F6D616769636D616E2E70616B000000000000000000").decode("latin-1"), # Magic Man entry in NPCList
			bytes.fromhex("547265655472756E6B73000000000000000000000000000000000000000000006E70635F747265657472756E6B732E70616B00000000000000").decode("latin-1"), # Tree Trunks entry in NPCList
			bytes.fromhex("57697A61726454686965660000000000000000000000000000000000000000006E70635F77697A61726474686965662E70616B000000000000").decode("latin-1"), # Wizard Thief entry in NPCList
			bytes.fromhex("436F616C4D616E000000000000000000000000000000000000000000000000006E70635F636F616C6D616E2E70616B00000000000000000000").decode("latin-1")] # Coal Man entry in NPCList

# Files that could be in NPCList but are currently excluded
#NPCListExtras = ["PartyBear1\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_partybear1.pak\0\0\0\0\0\0\0", "PartyBear2\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_partybear2.pak\0\0\0\0\0\0\0", "PartyBear3\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_partybear3.pak\0\0\0\0\0\0\0",
#			"CinnamonBun\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_cinnamonbun.pak\0\0\0\0\0\0", "Keyper\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_keyper.pak\0\0\0\0\0\0\0\0\0\0\0", "Snail\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_snail.pak\0\0\0\0\0\0\0\0\0\0\0\0",
#			"ChooseGoose\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_choose_goose.pak\0\0\0\0\0", "PotShopGuy\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_potteryshopguypak", "PootCloud\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_pootcloud.pak\0\0\0\0\0\0\0\0",]	

# List of items within global_shop.txt in global.pak; currently unsupported due to the forced file size change and Choose Goose not selling you items that he doesn't sell in vanilla
shopList = ["PickupTrailMix1", "PickupTrailMix2", "PickupTrailMix3", "PickupBananarang", "PickupPlasticBag", "PickupHeartPiece", "PickupMeat", "PickupCyclopsTears", "PickupGumGlobe", "PickupDynaMIGHT"]


# List of local item pool
itemLocal = []

# List of local NPC pool
NPCLocal = []


itemList = []

# Choose data folder to randomize, initializes seed and spoiler log
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--folder", help="The AT3 data folder to randomize", type=str, required=True)
parser.add_argument("-s", "--seed", help="The custom seed to randomize with", type=str, required=False)
item_group = parser.add_argument_group("Item randomization")
ir = item_group.add_mutually_exclusive_group(required=True)
ir.add_argument("-nir", "--no-items-randomization", help="Do not randomize items", action="store_true")
ir.add_argument("-sir", "--standard-items-randomization", help="Use standard method of randomizing items", action="store_true")
ir.add_argument("-eir", "--expanded-items-randomization", help="Use expanded method of randomizing items", action="store_true")
ir.add_argument("-cir", "--custom-items-randomization", help="Use custom item pool to randomize items", action="store_true")
item_group.add_argument("-ci", "--custom-items", help="The custom item pool to use (comma terminated)", type=str, required=False)
il = item_group.add_mutually_exclusive_group(required=True)
il.add_argument("-nl", "--no-logic", help="Do not randomize item logic", action="store_true")
il.add_argument("-sl", "--standard-logic", help="Use standard method of randomizing item logic", action="store_true")
npc_group = parser.add_argument_group("NPC randomization")
nr = npc_group.add_mutually_exclusive_group(required=True)
nr.add_argument("-nnr", "--no-npcs-randomization", help="Do not randomize NPCs", action="store_true")
nr.add_argument("-snr", "--standard-npcs-randomization", help="Use standard method of randomizing NPCs", action="store_true")
nr.add_argument("-cnr", "--custom-npcs-randomization", help="Use custom NPC pool to randomize NPCs", action="store_true")
nr.add_argument("-gunt", "--gunter-insanity", help="Turns the NPCs to be randomized into Gunter", action="store_true", required=False)
npc_group.add_argument("-cn", "--custom-npcs", help="The custom NPC pool to use (comma terminated)", type=str, required=False)
parser.add_argument("-spl", "--spoiler-log", help="Output a spoiler log", action="store_true", default=False)
parser.add_argument("-lsp", "--lsp-cave-randomization", help="Randomize the LSP Cave area", action="store_true", default=False)
parser.add_argument("-ntmr", "--nightmare-castle-randomization", help="Randomize the Nightmare Castle area", action="store_true", default=False)
parser.add_argument("-bsmt", "--castle-basement-randomization", help="Randomize the Castle Basement area", action="store_true", default=False)

prefs, log, spoilerLog, itemList = parseOptions(parser.parse_args(), defaultItemList, fileList, itemListExpanded)

randomize(fs, prefs, fileList, spoilerLog, itemList, itemLocal, itemListReplaced, NPCList, NPCList2, NPCLocal)
