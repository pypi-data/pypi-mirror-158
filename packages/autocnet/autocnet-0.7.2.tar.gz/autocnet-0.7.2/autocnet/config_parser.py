import os
import yaml

def parse_config(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'Config file {filepath} does not exist.')

    # Not wrapping in a try/except so that we get the 
    # yaml library to raise any issues on parsing
    with open(filepath, 'r') as f:
        config = yaml.safe_load(f)
    
    spatial = config.get('spatial', None)
    if spatial == None:
        raise KeyError('Config is missing the root "spatial" key.')
    for k in ['latitudinal_srid', 'dem']:
        if k not in spatial.keys():
            raise KeyError(f'Missing key: {k} in the spatial section of the config.')
            
    database = config.get('database', None)
    if database == None:
        raise KeyError('Config is missing the root "database" key.')
    
    redis = config.get('redis', None)
    if redis == None:
        raise KeyError('Config is missing the root "redis" key.')

    for k in ['type', 'username', 'password', 'host', 'pgbouncer_port', 'name']:
        if k not in database.keys():
            raise KeyError(f'Missing key: "{k}" in the database section of the config.')

    return config
