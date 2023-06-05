import requests
from pyvi import ViTokenizer, ViPosTagger

def translator(token_list):
    url = 'https://bahnar.dscilab.site:20007/translate/vi_ba'

    header = {
        'Contend-Type': 'application/json'
    }

    response_data = []

    i = 0
    error = ""
    while i < len(token_list):
        token = token_list[i]

        data = {'text': token}
        response = requests.post(url, headers= header, json= data)
        
        if response.status_code != 200:
            print(f"POST Request failed: \"{token}\"")

            if error == "": error = token
            elif error != token: print(f"Have not fix \"{error}\" and jump another error: \"{token}\"")
        else:
            if error == token: 
                print(f"Fix \"{error}\"")
                error = ""

            response_data.append(response.json()['tgt'].replace(' .', '').lower())
            i += 1

    return response_data

def read_file(filename):
    sentences = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            sentences.append(line.rstrip())

    return sentences

def tokenize_tag(str):
    token, tag = ViPosTagger.postagging(ViTokenizer.tokenize(str))

    for i in range(len(token)):
        token[i] = token[i].replace('_', ' ')
    
    return (token, tag)