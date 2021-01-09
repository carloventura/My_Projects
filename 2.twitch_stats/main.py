# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import os
import json
from datetime import datetime, timedelta

# Definizione variabili
c_id = '22kzmmnxclbjcr5c95sk9vnpkqudci'
c_sec = 'msysvmzq9qh8po37nzx08pkdspcspq'
excluded_games = ['Just Chatting', 'Special Events', 'Music']
game_list_id = []
game_list_name = []
out_list = []
today = datetime.now()
delta = today - timedelta(days=30)


def auth(client_id, client_secret):
    # Use a breakpoint in the code line below to debug your script.
    url_req = 'https://id.twitch.tv/oauth2/token?client_id=' + client_id + '&client_secret=' + client_secret + '&grant_type=client_credentials'
    req = requests.post(url_req)
    out = json.loads(req.content)
    authorization = out['token_type'].capitalize() + ' ' + out['access_token']
    print(authorization)
    return authorization


def get_top_games(client_id, authorization):
    url_req = f'https://api.twitch.tv/helix/games/top?first=30'
    req = requests.get(url_req, headers={'Client-Id': client_id, 'Authorization': authorization})
    out = json.loads(req.content)
    for i in out['data']:
        if i['name'] not in excluded_games:
            game_list_id.append(i['id'])
            game_list_name.append(i['name'])
    return out


def get_streams(client_id, authorization, id):
    url_req_start = f'https://api.twitch.tv/helix/streams?first=50'
    for j in id:
        url_req = url_req_start + '&game_id=' + j
        req = requests.get(url_req, headers={'Client-Id': client_id, 'Authorization': authorization})
        temp = json.loads(req.content)
        if j == id[0]:
            out = temp
            for k in range(len(out['data'])):
                out_data = out['data'][k]
                out_data['trnsctn_id'] = today.strftime("%Y%m%d%H%M")
        else:
            for k in range(len(temp['data'])):
                temp_data=temp['data'][k]
                temp_data['trnsctn_id'] = today.strftime("%Y%m%d%H%M")
                out['data'].append(temp_data)
    return out


def write_json(new, filename='twitch_stats.json'):
    if os.path.isfile('./'+filename):
        with open(filename) as json_file:
            data = json.load(json_file)
            temp = data['data']
            for ind in range(len(new['data'])):
                temp.append(new['data'][ind])
        with open(filename, 'w') as f:
            json.dump(data, f)
    else:
        with open(filename, 'w') as f:
            json.dump(new, f)


def delete_old_json(filename='twitch_stats.json'):
    if os.path.isfile('./' + filename):
        with open(filename) as json_file:
            data = json.load(json_file)
            temp = data['data']
            temp[:] = [d for d in temp if d.get('trnsctn_id') > delta.strftime("%Y%m%d%H%M")]
            temp[:] = [d for d in temp if d.get('trnsctn_id') > delta.strftime("%Y%m%d%H%M")]
            #rimettere il maggiore e cambiare il delta con 7 giorni
        with open(filename, 'w') as f:
            json.dump(data, f)
        print('deleted')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    delete_old_json(filename='twitch_stats.json')
    authoriz = auth(client_id=c_id, client_secret=c_sec)
    top_games = get_top_games(client_id=c_id, authorization=authoriz)
    streams = get_streams(client_id=c_id, authorization=authoriz, id=game_list_id)
    write_json(new=streams)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
