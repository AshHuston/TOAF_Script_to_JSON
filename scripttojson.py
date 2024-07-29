import json
import os
import pandas
from pandas import *
import numpy

def getJsonFromLine(csv_data, csv_line_index):

    if numpy.isnan(csv_line_index):
        return float('nan')
    formatting_offset = 2
    line = int(csv_line_index - formatting_offset)
    data = {
        "voiceover_id" : csv_data['VOICEOVER ID'].tolist()[line],
        "display_text" : csv_data['DISPLAY TEXT'].tolist()[line],
        "speaker" : csv_data['SPEAKER'].tolist()[line],
        "speaker_side" :  csv_data['SPEAKER SIDE'].tolist()[line],
        "text" : csv_data['TEXT'].tolist()[line],
        "flag_id" : csv_data['FLAG ID'].tolist()[line],
        "flag_value" : csv_data['FLAG VALUE'].tolist()[line],
        "respondable" : csv_data['RESPONDABLE?'].tolist()[line],
        "response_options":{
            "response_1" : getJsonFromLine(csv_data, csv_data['RESPONSE 1'].tolist()[line]),
            "response_2" : getJsonFromLine(csv_data, csv_data['RESPONSE 2'].tolist()[line]),
            "response_3" : getJsonFromLine(csv_data, csv_data['RESPONSE 3'].tolist()[line]),
            "response_4" : getJsonFromLine(csv_data, csv_data['RESPONSE 4'].tolist()[line]),
            "response_5" : getJsonFromLine(csv_data, csv_data['RESPONSE 5'].tolist()[line])},
    }

    if data['flag_id'] == "-":
        data['flag_id'] = ""

    if data['display_text'] == "-":
        data['display_text'] = ""

    return data

def getCharacterSpriteData(csv_dialogue):
    characters = set()
    characterSprites = []
    for each in csv_dialogue['SPEAKER'].tolist():
        if not pandas.isna(each):
            characters.add(each)
    for each in characters:
        characterSprites.append({"name" : each, "spriteID" : "", "yapping_speed" : 0.5})    
    return characterSprites

def getDialogueID(csv_data):
    dialogueID = int(csv_data['\/ Dialogue ID \/'].tolist()[0])
    return dialogueID

directory = 'input_script_csvs'
completedDirectory = 'completed_scripts'
for filename in os.listdir(directory):
    file = os.path.join(directory, filename)

    #Pull out the data
    csv_data = read_csv(file)

    #Build the JSON
    firstLineIndex = 2
    dialogueData = getJsonFromLine(csv_data, firstLineIndex)
    jsonData = {
        "dialogueID" : getDialogueID(csv_data),
        "chatSpriteIDs" : getCharacterSpriteData(csv_data),
        "dialogue" : dialogueData 
    }

    
    #Output the JSON
    outputFileName  = filename.split(".")[0]
    completedPath = os.path.join(completedDirectory, f'{outputFileName}.txt')
    out = open(completedPath, 'w', encoding='utf-8')
    
    outputJson = json.dumps(jsonData, indent=4)

    out.write(outputJson)

    completedPath = os.path.join(completedDirectory, filename)
    os.rename(file, completedPath)
