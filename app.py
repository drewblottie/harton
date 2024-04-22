#!/usr/bin/python
#
# https://flask.palletsprojects.com/en/3.0.x/installation/
#

from flask import Flask, jsonify, request, render_template
import hashlib
import hmac
import email
import time
import json
import requests
import datetime
from requests.auth import HTTPBasicAuth
import threading
import traceback
import sys

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)



app = Flask(__name__,
            static_url_path='',
            static_folder='public',)



class TreeNode:
    def __init__(self, name, id, url, is_dead):
        self.type= 'TreeNode'
        self.name = name
        self.id = id
        self.url = url
        self.is_dead =  is_dead
        self.children = []
    def add_child(self, child):
        self.children.append(child)

class Location:
    def __init__(self, name, id, parent_id, url, is_dead):
        self.type = 'Location'
        self.name = name
        self.id = id
        self.url = url
        self.is_dead =  is_dead
        self.parent_id = parent_id
        self.children = []
        self.characters = []
        self.orgs = []
        self.items = []
        
class Character:
    def __init__(self, name, id, parent_id, url, is_dead):
        self.type = 'Character'
        self.name = name
        self.id = id
        self.url = url
        self.is_dead =  is_dead
        self.parent_id = parent_id
        self.children = []
        self.items = []

def build_tree(locations, characters):
    # Create a dictionary to store locations by name for efficient lookup
    location_dict = {location['id']: Location(location['name'],location['id'],location['location_id'],location['urls']['view'],None) for location in locations}
    char_dict = {character['id']: Character(character['name'],character['id'],character['location_id'],character['urls']['view'],character['is_dead']) for character in characters}
    
    
    # Define a function to recursively build the tree
    def add_child_to_parent(location):
        specific_location = location_dict.get(location['id'])
        if specific_location.parent_id is None:
            return location_dict[location['id']]
        else: 
            parent_location = location_dict.get(specific_location.parent_id)
            parent_location.children.append(specific_location)
            return specific_location
        
    def add_characters(character):
        def add_child_to_parent(character):
            specific_char = char_dict.get(character['id'])
            if specific_char.parent_id is None:
                return char_dict[character['id']]
            else: 
                parent_location = location_dict.get(specific_char.parent_id)
                parent_location.characters.append(specific_char)
                return specific_char

        for character in characters:
            add_child_to_parent(character)
        

    # Build the tree by adding each location to its parent's children
    for location in locations:
        add_child_to_parent(location)
        #add_child_to_parent(location)
    for location in locations:
        specific_location = location_dict.get(location['id'])
    # Find and return the root node(s) (locations without a parent)
    root_nodes = [node for node in location_dict.values() if not node.parent_id]
    add_characters(characters)
    return root_nodes

def get_sublocations(location):
    sublocations = []

    def traverse(node):
        if node==location:
            pass    
        else:
            sublocations.append(node)
        for child in node.children:
            traverse(child)

    traverse(location)
    return sublocations
    
def get_subchars(location):
    subchars = []

    def traverse(node):
        if node==location:#base case for recursion - if it is this node, we skip
            pass    
        else:  #if it is another node
            for char in node.characters: #we get all characters in that node
                location.characters.append(char) #and append them to the parent location
        for child in node.children: # we recursively do this for all children
            traverse(child)

    traverse(location)
    for chars in subchars:print(chars.name)
    return subchars


#All Location Children







def transformationHeader(properties):
    list = []
    for k, v in properties.items():
        list.append("{0}:{1}".format(k, v))

    return ";".join(list)



@app.route('/')
def root():
    print("test")
    indicators = []
    
    v4_URL = 'https://api.kanka.io/1.0/campaigns/246695'
    v4_public_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiN2NjZjg2MjQ3ZDU3NWNkZDk0MDE2MmUzN2I0ODY3ZDRlMWQxOTEyNDkyZjJjMWY5NDFhODE2ZTY2YTQyMTIyYjcyMTc3MWZiOTBlZWU3OWEiLCJpYXQiOjE3MTM3MzU2MzguODE2NjQxLCJuYmYiOjE3MTM3MzU2MzguODE2NjQ1LCJleHAiOjE3NDUyNzE2MzguODA2NTM2LCJzdWIiOiIyNDk1NjciLCJzY29wZXMiOltdfQ.spM5nOpEA3P_OT-hZeFHm_OmLnT_103w_V4vjHdSV-Gpj9pZSIUyiNPQ9fuIgehxD5i2H3MR3JjANg3ADJjKLT7tYNOX79uPOnZPngskuNqJMvgctbtb5X_yK842hRojMPxMQ0vQgU2f3IjdjtzurxfOT88w1tQp2AQ52TLogNF2JqFfmEzvUlwNgHrqzMylwtaILITv6v695LDEdgouFgP4X6IC7Y3_-uc7X7u0IdSfHG2H7f0-HhWX_pyAyKOl4sWAOe9PJggwQwCQRhVyDbxUlSDE32rtPq0YGovv_KDE5j4fbP6r5peMl6QE2coOpcnWrNxX8ugLEmaUde8Clhu6WoePgFmMszIkW-02F5ZWRPU9rRjfikjxB-iFAXRanc_rtp_xfQVsKI4S8pZ4nHjVlcCurpC3Ys_ZprT2BenmIkRzcU441BlwdY14nvnTNggd0D70-tW13ZySX2-d494A9Yx6FthIO5HHPcbtmTn1XxWfWE4ALFOL-VnzIcjZR0muiKAEel3OuObcuI5MNWWPNjOATlovgBHutOgCfg1cvqdXpp6Zhfa0MkW_h8s916VOUB6qncc0VE6dxbloOxXr3vrjHaP86I9p_SpLPprNWBsh96WaIaIahC9zhIe66_PGCnmaodBcbtnfY0Wm-4op3hghJhUzfgJ_pNi2xow'
    #v4_public_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMjQ1MzAwZjFlZGJkYWE0ZDk3YzAyOTA2YTZhNTAxZDc2MGI2YWEyZTY4MDQ0MDM3YTk0NzU5YjZkMGQ4MGYxYWI2YWZmYWUwNjUwNGZjNTYiLCJpYXQiOjE3MTMxOTAxMjcuODQwNDE2LCJuYmYiOjE3MTMxOTAxMjcuODQwNDIxLCJleHAiOjE3NDQ3MjYxMjcuODM0NTg1LCJzdWIiOiIyNDk1NTQiLCJzY29wZXMiOltdfQ.WVwoAct2TRY-i6pxAY2iZs5UJKTEFbNAlt7uwRPq6CLMIWig4AZGgtZplFxw2gO5ZeorNdPM3YL-uaPveINJBKABuPfB5ASnri7Qqo5JE_dIUl-D0L9b7WYxFX53NKPWHzQ-Bt6LXL5uQsHUzwTgyz48HC-EKGauX2e3tBOxvqaN-TR8v7T1-SsCVaNgkLOsl6jGYIp1DJ2NVtMqnXgGIG6y4hlAyIes_MdHbnxz8qKIDHzFVaj0r74-45dYOMJFxK94wdlPzOL9RnTuzZz0E7nP_AZ4sPzC7MLVgr_S72RNoeL8mKM52qUId3eqhrRhSvqV93ZleUe5X2KbVXTRagE-ZFriJQgh-wj6srAonZsxp_kpd_p1RpKm79FfBRgBeOyWVzvCsr5Vsv59g2NXKHtekLzmtUXvlIH8WchmznjmZusZZgXi51a8CvbHdQtKyld2KiF3OISaitTrFOgQBRHlYRgfrVFMUFIZG4UiXXmYhaPK0Z_eyGU59lBV7ngY5l-Bu2O1DM5zAkzamRBl8X6W5vPd8b2_hW0SHmbjpRRSZimd9n4Ur-lNoawMMVngy8t8iVjeLkw0M-qmnmL3VoBYpHteiMtg6uzBLN_Z1S31lQayVXwCky7BEubgHg91W3TZPzXiTF4ve3YlXohtkRinxs8KsrOHkCiH1IXZB8Y'
    #v4_private_key = ''
    nowish = str(time.time())
    accept_header = 'application/json'
    x_app_name = 'APIv4_Vulnerabilities'
    payload={}
    #fname='C:\\Users\\bzsf\\Kanka_' + nowish + '.csv'
    ENDPOINT = 'https://api.kanka.io/1.0/campaigns/246695'
    headers = {
        "Authorization": "Bearer "+ v4_public_key,
        "Content-Type" : accept_header 
    }


    EPCHARS = ENDPOINT + '/characters'
    responsechars = requests.request("GET", EPCHARS, headers=headers, verify=False)
    characters = responsechars.json()['data']
    with open ('.venv\public\characters.json', 'w') as f:
        json.dump(responsechars.json(), f)
    

    EPLOCS = ENDPOINT + '/locations'

    responselocs=requests.request("GET", EPLOCS, headers=headers, verify=False)
    locations = responselocs.json()['data']
    with open ('.venv\public\locations.json', 'w') as f:
        json.dump(responselocs.json(), f)

    EPORGS = ENDPOINT + '/organisations'

    responseorgs=requests.request("GET", EPORGS, headers=headers, verify=False)
    orgs = responseorgs.json()['data']
    with open ('.venv\public\orgs.json', 'w') as f:
        json.dump(responseorgs.json(), f)

    EPQUESTS = ENDPOINT + '/quests'

    responsequests =requests.request("GET", EPQUESTS, headers=headers, verify=False)
    quests = responsequests.json()['data']
    with open ('.venv\public\quests.json', 'w') as f:
        json.dump(responsequests.json(), f)

    EPITEMS = ENDPOINT + '/items'

    responseitems =requests.request("GET", EPITEMS, headers=headers, verify=False)
    items = responseitems.json()['data']
    with open ('.venv\public\items.json', 'w') as f:
        json.dump(responseitems.json(), f)
    #print("test2")
    

    rootnodes = build_tree(locations, characters)
    for root in rootnodes: 
        ini_string = json.dumps({'type': root.type,  'parentid': str(root.parent_id),  'id': str(root.id),  'name': str(root.name),  'parentname': str(root.name),  'url': root.url,  'is_dead': root.is_dead    })
        mid_string = ini_string
    root2 = root
    root2.children = get_sublocations(root2)

    for node in root2.children: 
        #print(root2.name,",", node.name)
        ini_string = {'type': node.type,  'parentid': str(root2.id),  'id': str(node.id),  'name': str(node.name),  'parentname': str(root2.name),  'url': node.url,  'is_dead': node.is_dead  }
        add_string = json.dumps(ini_string)
        add_string = "," + add_string
        mid_string += add_string
        for char in node.characters:
            #print(root2.name, ",", char.name)
            ini_string = {'type': char.type,  'parentid': str(node.id),  'id': str(char.id),  'name': str(char.name),  'parentname': str(node.name),  'url': char.url,  'is_dead': char.is_dead  }
            add_string = json.dumps(ini_string)
            add_string = "," + add_string
            mid_string += add_string
            ini_string = {'type': char.type,  'parentid': str(root2.id),  'id': str(char.id),  'name': str(char.name),  'parentname': str(root2.name),  'url': char.url,  'is_dead': char.is_dead  }
            add_string = json.dumps(ini_string)
            add_string = "," + add_string
            mid_string += add_string
        node.children = get_sublocations(node)
        for subnode in node.children: 
            #print("Subchild: ", node.name,",", subnode.name)
            ini_string = {'type': subnode.type,  'parentid': str(node.id),  'id': str(subnode.id),  'name': str(subnode.name),  'parentname': str(node.name),  'url': subnode.url,  'is_dead': subnode.is_dead  }
            add_string = json.dumps(ini_string)
            add_string = "," + add_string
            mid_string += add_string
            #for char in subnode.characters:
                #print(subnode.name, ",", char.name)
                #ini_string = {'type': char.type,  'parentid': str(subnode.id),  'id': str(char.id),  'name': str(char.name),  'parentname': str(subnode.name)  }
                #add_string = json.dumps(ini_string)
                #add_string = "," + add_string
                #mid_string += add_string
            for char in subnode.characters:
                #print(subnode.name, ",", char.name)
                ini_string = {'type': char.type,  'parentid': str(node.id),  'id': str(char.id),  'name': str(char.name),  'parentname': str(node.name),  'url': char.url,  'is_dead': char.is_dead  }
                add_string = json.dumps(ini_string)
                add_string = "," + add_string
                mid_string += add_string

    string1 = "{ \"data\": ["
    string2 = "]}"
    mid_string = string1 + mid_string + string2
    print (mid_string)
    json_object = json.loads(mid_string)
    with open ('.venv\public\\treemap.json', 'w') as f:
        json.dump(json_object, f)

 
    
    return app.send_static_file('adminpage.html') 

if __name__ == '__main__':
    app.run(debug=True)
    
