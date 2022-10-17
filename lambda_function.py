from utils import get_source, get_server_status, get_players_online, get_ip, set_number_of_players, get_last_number_of_players
import boto3
from vars import instance_id

instance = boto3.resource('ec2', region_name='eu-west-3').Instance(instance_id)
table = boto3.resource('dynamodb').Table('minecraft_server_players')

def lambda_handler(event, context):
    
    source = get_source(event)
    instance_status = get_server_status(instance)
    
    if source == 'watchdog':
        print(instance_status)
        if instance_status in ['running', 'launching']:
            current_players = get_players_online(get_ip(instance))
            if current_players > 0:
                set_number_of_players(table, current_players)
            else:
                last_players = get_last_number_of_players(table)
                if last_players > 0:
                    set_number_of_players(table, 0)
                else:
                    instance.stop()
        return None
    
    if source == 'request':
        print(instance_status)
        if instance_status == 'unavailable':
            return 'El servidor ha sido eliminado'
        if instance_status == 'launching':
            return f'Ya se está iniciando el servidor, espera un momento\n{instance.state.get("Name")}'
        if instance_status == 'running':
            ip = get_ip(instance)
            players = get_players_online(ip)
            return f'El servidor está abierto\nJugadores en linea: {players}\nDirección: {ip}:25565'
        if instance_status == 'stopping':
            return 'El servidor se está apagando, inténtalo más tarde'
        if instance_status == 'stopped':
            instance.start()
            set_number_of_players(table, 1000)
            return 'El servidor estaba apagado, iniciando...'
    return None
