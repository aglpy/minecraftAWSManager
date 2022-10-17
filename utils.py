from typing import Dict
import json
import socket
from vars import port
from boto3.dynamodb.conditions import Key
import datetime

def get_source(event: Dict):
    if event.get('source') == 'aws.events':
        return 'watchdog'
    if event.get('rawPath') == '/':
        return 'request'
    return None
    
def get_server_status(instance):
    code = instance.state['Code']
    print(code)
    if code in [32, 48]:
        return 'unavailable'
    if code == 0:
        return 'launching'
    if code == 16:
        return 'running'
    if code == 64:
        return 'stopping'
    if code == 80:
        return 'stopped'
        
def get_last_number_of_players(table):
    return table.query(KeyConditionExpression=Key('index').eq(0), Limit=1, ScanIndexForward=False).get('Items')[0].get('players')
    
def set_number_of_players(table, players):
    return table.put_item(Item={'index': 0, 'timestamp': int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')), 'players': players})
        
def get_ip(instance):
    return instance.public_ip_address
        
def z(s):
    a = 0
    b = s.recv(1)[0]
    while b & 128:
        a = (a << 7) + b & 127
        b = s.recv(1)[0]
    return b & 127 + (a << 7)
def V(d, b):
    return bytes([(64 * (i != b // 7)) + ((d >> (7 * i)) % 128) for i in range(1 + b // 7)])
def D(d):
    return V(len(d), len(d).bit_length()) + d
def get_players_online(ip):
    s = socket.socket(2, 1)
    try:
        s.connect((ip, port))
    except:
        return -1
    s.send(D(bytes(2) + D(bytes(ip, 'utf-8')) + bytes([port >> 8, port % 256, 1])) + bytes([1, 0]))
    z(s)
    z(s)
    l = z(s)
    d = bytes()
    while len(d) < l:
        d += s.recv(1024)
    s.close()
    return json.loads(str(d, 'utf-8')).get('players').get('online')
