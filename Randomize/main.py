import json
import logging
import os

import azure.functions as func
from azure.storage.file import FileService 
from dotenv import load_dotenv
from . import options
from . import randomizer

def main(req: func.HttpRequest) -> func.HttpResponse:
    prefs = {}
    logging.info('Python HTTP trigger function processed a request.')

    load_dotenv()

    fs = FileService(account_name=os.getenv('AZURE_FILESHARE_NAME'), account_key=os.getenv('AZURE_FILESHARE_KEY'))

    # List of files to be randomized within data folder
    fileList = ["overworld_forest_cave.pak", "overworld_forest_cave_2.pak", "overworld_forest_master.pak", "overworld_iceking_cave.pak", "overworld_kingdom_master.pak", "overworld_mountain_cave_1.pak", "overworld_mountain_cave_3.pak", "overworld_mountain_cave_4.pak", "overworld_mountain_master.pak", "overworld_swamp_master.pak", "overworld_wasteland_cave_1.pak", "temple_dream_master.pak", "temple_fear_master.pak", "temple_song_master.pak"]

    # Files that could be in fileList but are currently excluded
    #fileListExtras = ["\\castle_nightmare_master.pak", "\\global.pak", "\\overworld_lsp_cave.pak", "\\castle_basement_master.pak"]

    # Used for debugging, lists most files within data folder to scout for files that can be added to pooling and randomizing but aren't due to lack of items or NPCs
    #fileListComplete = ["\\arena_hairapes.pak", "\\autoload.pak", "\\15boss_crabdemon.pak", "\\boss_hairapes.pak", "\\boss_nightmare.pak", "\\boss_shadowfinn.pak", "\\castle_basement_master.pak",
    #			"\\castle_nightmare_master.pak", "\\caves.pak", "\\dreamtemple.pak", "\\fearcastle.pak", "\\feartemple.pak", "\\gym_crabdemon.pak", "\\gym_nprincess.pak",
    #			"\\gym_quests.pak", "\\gym_shadowfinn.pak", "\\npc_choose_goose.pak", "\\npc_coalman.pak", "\\npc_iceking.pak", "\\npc_magicman.pak", "\\npc_marceline. pak", "\\npc_mr_pig.pak",
    #			"\\npc_partypat.pak", "\\npc_potteryshopguy.pak", "\\npc_rattleballs.pak", "\\npc_shelby.pak", "\\npc_starchy.pak", "\\npc_treetrunks.pak", "\\overworld.pak", "\\overworld_forest.pak",
    #			"\\overworld_forest_cave.pak", "\\overworld_forest_cave_2.pak", "\\overworld_forest_master.pak", "\\overworld_iceking_cave.pak", "\\overworld_kingdom.pak", "\\overworld_kingdom_cave_01.pak",
    #			"\\overworld_kingdom_master.pak", "\\overworld_lsp_cave.pak", "\\overworld_mountain.pak", "\\overworld_mountain_cave_1.pak", "\\overworld_mountain_cave_2.pak", "\\overworld_mountain_cave_3.pak",
    #			"\\overworld_mountain_cave_4.pak", "\\overworld_mountain_master.pak", "\\overworld_swamp.pak", "\\overworld_swamp_master.pak", "\\overworld_wasteland_cave_1.pak", "\\songtemple.pak",
    #			"\\temple_dream_master.pak", "\\temple_fear_master.pak", "\\temple_song_master.pak", "\\temples.pak"]

    # List of items to check randomization; Null char added to each entry to maintain a consistent length of 19
    defaultItemList = ["PickupChestItemKey\0", "PickupTreasureHuge\0", "PickupTrailMix\0\0\0\0\0", "PickupSpareThumps\0\0", "PickupTrailMix3\0\0\0\0", "PickupMeat\0\0\0\0\0\0\0\0\0", "PickupHeartPiece\0\0\0", "PickupPencil\0\0\0\0\0\0\0", "PickupSweater\0\0\0\0\0\0", "PickupMapPaper\0\0\0\0\0", "PickupChestItemRBK\0", "PickupTreasureSmall", "PickupTreasureBig\0\0", "PickupGumGlobe\0\0\0\0\0", "PickupWoodPlank\0\0\0\0", "PickupPlasticBag\0\0\0", "PickupFruitStack\0\0\0", "PickupHeroGauntlet\0", "PickupTrailMix1\0\0\0\0", "PickupTrailMix2\0\0\0\0","PickupTrailMix4\0\0\0\0", "PickupGrabbyHand\0\0\0"]
    
    # List of items that work when put into the game, however are not found to be pooled as well as are not worth putting into itemsListExpanded
    itemListUnused = ["PickupNutStack\0\0\0\0\0", "PickupJake\0\0\0\0\0\0\0\0\0"]

    # Items that are found on in bushes and pots. Although their placements that would be replaced are consistent, they are separated into a different item list so that the user may toggle them off
    itemListExtras = ["PickupHealthOne\0\0\0\0", "PickupFruits\0\0\0\0\0\0\0", "PickupDemonHeart\0\0\0", "PickupNuts\0\0\0\0\0\0\0\0\0", "PickupPieFairy\0\0\0\0\0"]

    # List of items to be removed in favor of items from itemListExpanded while using expanded item pool; Currently depricated in favor of replacing PickupChestItemKey as they are entirely useless outside of dungeons
    itemListReplaced = ["PickupTreasureSmall", "PickupTreasureBig\0\0", "PickupDemonHeart\0\0\0", "PickupNuts\0\0\0\0\0\0\0\0\0", "PickupFruits\0\0\0\0\0\0\0"]

    # Items that could be added to the item pool, but are not found within the game via current methods or are only found in the shop, which can't currently be randomized. Used for expanded item pool
    itemListExpanded = ["PickupFlambo\0\0\0\0\0\0\0", "PickupBananarang\0\0\0", "PickupLadyRing\0\0\0\0\0", "PickupSlammyHand\0\0\0", "PickupSweater\0\0\0\0\0\0", "PickupLoveNote\0\0\0\0\0", "PickupHeatSignature", "PickupMindGames\0\0\0\0", "PickupFanfiction\0\0\0", "PickupEnergyDrink\0\0", "PickupBugMilk\0\0\0\0\0\0", "PickupEnchiridion\0\0"]

    # List of all items that can be toggled on and off when using custom item pool
    itemListCustom = ["PickupTreasureSmall", "PickupTreasureBig\0\0", "PickupTreasureHuge\0", "PickupPencil\0\0\0\0\0\0\0", "PickupMapPaper\0\0\0\0\0", "PickupChestItemKey\0", "PickupChestItemRBK\0", "PickupPlasticBag\0\0\0", "PickupTrailMix\0\0\0\0\0", "PickupTrailMix1\0\0\0\0", "PickupTrailMix2\0\0\0\0", "PickupTrailMix3\0\0\0\0", "PickupTrailMix4\0\0\0\0", "PickupSpareThumps\0\0", "PickupHeartPiece\0\0\0", "PickupGumGlobe\0\0\0\0\0", "PickupWoodPlank\0\0\0\0", "PickupFruits\0\0\0\0\0\0\0", "PickupFruitStack\0\0\0", "PickupNuts\0\0\0\0\0\0\0\0\0", "PickupDemonHeart\0\0\0", "PickupHealthOne\0\0\0\0", "PickupBananarang\0\0\0", "PickupGrabbyHand\0\0\0", "PickupFlambo\0\0\0\0\0\0\0", "PickupHeroGauntlet\0", "PickupLadyRing\0\0\0\0\0", "PickupSlammyHand\0\0\0", "PickupSweater\0\0\0\0\0\0", "PickupLoveNote\0\0\0\0\0", "PickupHeatSignature", "PickupMindGames\0\0\0\0", "PickupFanfiction\0\0\0", "PickupEnergyDrink\0\0", "PickupBugMilk\0\0\0\0\0\0", "PickupEnchiridion\0\0"]

    # List of NPCs to check randomization; Null char added to each entry to maintain consistent length of 57
    NPCList = ["Gunter\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_gunter.pak\0\0\0\0\0\0\0\0\0\0\0", "PartyPat\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_partypat. pak\0\0\0\0\0\0\0\0\0", "Demon\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_nightospheredemon.pak" "TinyManticore\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_manticore.pak\0\0\0\0\0\0\0\0", "Rattleballs\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_rattleballs.pak\0\0\0\0\0\0", "IceKing\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_iceking.pak\0\0\0\0\0\0\0\0\0\0", "Shelby\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_shelby.pak\0\0\0\0\0\0\0\0\0\0\0", "MrPig\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_mr_pig.pak\0\0\0\0\0\0\0\0\0\0\0", "TreeTrunks\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_treetrunks.pak\0\0\0\0\0\0\0", "MagicMan\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_magicman.pak\0\0\0\0\0\0\0\0\0", "Stanley\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_stanely. pak\0\0\0\0\0\0\0\0\0\0", "Witch\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_witch. pak\0\0\0\0\0\0\0\0\0\0\0\0", "CoalMan\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_coalman.pak\0\0\0\0\0\0\0\0\0\0", "WizardTheif\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_wizardthief.pak\0\0\0\0\0\0"]

    # List of certain NPCs in their hex values, due to a bug that has them not be found with the method used in NPCList
    NPCList2 = [bytes.fromhex("44656D6F6E0000000000000000000000000000000000000000000000000000006E70635F6E696768 746F73706865726564656D6F6E2E70616B").decode("latin-1"), # Nightosphere Demon entry in NPCList
    			bytes.fromhex("54696E794D616E7469636F7265000000000000000000000000000000000000006E70 635F6D616E7469636F72652E70616B0000000000000000").decode("latin-1"), # Tiny Manticore entry in NPCList
    			bytes.fromhex("4D616769634D616E0000000000000000000000000000000000000000000000006E70 635F6D616769636D616E2E70616B000000000000000000").decode("latin-1"), # Magic Man entry in NPCList
    			bytes.fromhex("547265655472756E6B73000000000000000000000000000000000000000000006E70 635F747265657472756E6B732E70616B00000000000000").decode("latin-1"), # Tree Trunks entry in NPCList
    			bytes.fromhex("57697A61726454686965660000000000000000000000000000000000000000006E70 635F77697A61726474686965662E70616B000000000000").decode("latin-1"), # Wizard Thief entry in NPCList
    			bytes.fromhex("436F616C4D616E000000000000000000000000000000000000000000000000006E70 635F636F616C6D616E2E70616B00000000000000000000").decode("latin-1")] # Coal Man entry in NPCList

    # Files that could be in NPCList but are currently excluded
    #NPCListExtras = ["PartyBear1\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_partybear1.pak\0\0\0\0\0\0\0", "PartyBear2\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_partybear2.pak\0\0\0\0\0\0\0", "PartyBear3\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_partybear3.pak\0\0\0\0\0\0\0", "CinnamonBun\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_cinnamonbun.pak\0\0\0\0\0\0", "Keyper\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_keyper.  pak\0\0\0\0\0\0\0\0\0\0\0","Snail\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_snail.pak\0\0\0\0\0\0\0\0\0\0\0\0", "ChooseGoose\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_choose_goose. pak\0\0\0\0\0", "PotShopGuy\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_potteryshopguypak", "PootCloud\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0npc_pootcloud.pak\0\0\0\0\0\0\0\0"]

    # List of items within global_shop.txt in global.pak; currently unsupported due to the forced file size change and Choose Goose not selling you items that he doesn't sell in vanilla
    shopList = ["PickupTrailMix1", "PickupTrailMix2", "PickupTrailMix3", "PickupBananarang", "PickupPlasticBag", "PickupHeartPiece", "PickupMeat",  "PickupCyclopsTears", "PickupGumGlobe", "PickupDynaMIGHT"]


    # List of local item pool
    itemLocal = []

    # List of local NPC pool
    NPCLocal = []


    itemList = []

    prefs, spoilerLog, itemList, fileList = options.parseOptions(req, defaultItemList, fileList, itemListExpanded)

    body = randomizer.randomize(fs, prefs, fileList, spoilerLog, itemList, itemLocal, itemListReplaced, NPCList, NPCList2, NPCLocal)

    return func.HttpResponse(json.dumps(body), mimetype="application/json", status_code=200)

