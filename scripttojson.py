import json
from openpyxl import Workbook
from openpyxl import load_workbook
import os
from pandas import *
import numpy

def getJsonFromLine(csv_data, csv_line_index):

    if numpy.isnan(csv_line_index):
        return float('nan')
    formatting_offset = 2
    line = int(csv_line_index - formatting_offset)
    data = {
        #"voiceover_id" : csv_data['VOICEOVER ID'].tolist()[line],
        "display_text" : csv_data['DISPLAY TEXT'].tolist()[line],
        "speaker" : csv_data['SPEAKER'].tolist()[line],
        "text" : csv_data['TEXT'].tolist()[line],
        "flag_id" : csv_data['FLAG ID'].tolist()[line],
        "flag_value" : csv_data['FLAG VALUE'].tolist()[line],
        "respondable" : csv_data['RESPONDABLE?'].tolist()[line],
        "response_1" : getJsonFromLine(csv_data, csv_data['RESPONSE 1'].tolist()[line]),
        "response_2" : getJsonFromLine(csv_data, csv_data['RESPONSE 2'].tolist()[line]),
        "response_3" : getJsonFromLine(csv_data, csv_data['RESPONSE 3'].tolist()[line]),
        "response_4" : getJsonFromLine(csv_data, csv_data['RESPONSE 4'].tolist()[line]),
        "response_5" : getJsonFromLine(csv_data, csv_data['RESPONSE 5'].tolist()[line]), 
    }

    if data['flag_id'] == "-":
        data['flag_id'] = ""

    if data['display_text'] == "-":
        data['display_text'] = ""

    convertedToJson = json.dumps(data, indent=4)
    return convertedToJson

def getCharacterSpriteData(csv_dialogue):
    characters = set()
    characterSprites = []
    for each in csv_dialogue['SPEAKER'].tolist():
        characters.add(each)
    for each in characters:
        characterSprites.append({"name" : each, "spriteID" : ""})
    return characterSprites

def getDialogueID(): # ---------------------------------------------------------------------------------- Make this, dummy
    return "********** MANUALLY CHANGE ID VALUE **********"

directory = 'input_script_xlsx'
completedDirectory = 'completed_scripts'
for filename in os.listdir(directory):
    file = os.path.join(directory, filename)

    #Pull out the data
    csv_data = read_csv(file)

    #Build the JSON
    firstLineIndex = 2
    dialogueData = getJsonFromLine(csv_data, firstLineIndex)
    jsonData = {
        "chatSpriteIDs" : getCharacterSpriteData(csv_data),
        "dialogueID" : getDialogueID(),
        "dialogue" : dialogueData 
    }
    outputJson = json.dumps(jsonData, indent=4)

    #Output the JSON
    completedPath = os.path.join(completedDirectory, 'TESTOUT.txt')
    out = open(completedPath, 'w', encoding='utf-8')
    out.write(outputJson)

    completedPath = os.path.join(completedDirectory, filename)
    os.rename(file, completedPath)
