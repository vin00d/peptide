# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_basics.ipynb (unless otherwise specified).

__all__ = ['settings_template', 'read_settings', 'settings', 'DATA_STORE', 'LOG_STORE', 'MODEL_STORE',
           'EXPERIMENT_STORE']

# Cell

from .imports import *

# Cell

def settings_template():
    '''Create initial settings for library.'''
    template = {
        'STORES' :
        {
            'DATA_STORE'       : f'{Path.home()}/.peptide/datasets',
            'LOG_STORE'        : f'{Path.home()}/.peptide/logs',
            'MODEL_STORE'      : f'{Path.home()}/.peptide/models',
            'EXPERIMENT_STORE' : f'{Path.home()}/.peptide/experiments'
        }
    }

    return template

# Cell

def read_settings():
    '''Read settings file at "~/.peptide/settings.yaml", if doesnt exist, create it from template.'''
    settings_dir = f'{Path.home()}/.peptide'
    settings_file = Path(f'{settings_dir}/settings.yaml')

    if not settings_file.exists():
        print('No settings file found, so creating from template ..')
        settings = Dict(settings_template())
        Path.mkdir(Path(settings_dir), exist_ok=True)
        with open(settings_file, 'w') as s:
            yaml.dump(settings.to_dict(), s, sort_keys=False, allow_unicode=True)
    else:
        with open(settings_file, 'r') as s:
            settings = Dict(yaml.full_load(s))

    # create directories if needed
    Path.mkdir(Path(settings.STORES.DATA_STORE), exist_ok=True)
    Path.mkdir(Path(settings.STORES.LOG_STORE), exist_ok=True)
    Path.mkdir(Path(settings.STORES.MODEL_STORE), exist_ok=True)
    Path.mkdir(Path(settings.STORES.EXPERIMENT_STORE), exist_ok=True)

    return settings

# Cell

settings = read_settings()

DATA_STORE         = settings.STORES.DATA_STORE
LOG_STORE          = settings.STORES.LOG_STORE
MODEL_STORE        = settings.STORES.MODEL_STORE
EXPERIMENT_STORE   = settings.STORES.EXPERIMENT_STORE