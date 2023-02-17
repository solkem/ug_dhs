import configparser
from pathlib import Path

def config(file_name="config.ini", section="postgresql"):
    """Read configuration parameters from config.ini file"""
    # get config file
    config_file = Path.cwd() / file_name
    if not config_file.exists():
        raise FileNotFoundError(f"Could not find config file: {config_file}")
    # read config file
    parser = configparser.ConfigParser()
    parser.read(config_file)
    # get section, default to postgresql
    db_params = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_params[param[0]] = param[1]
    else:
        raise ValueError(f"Section {section} not found in the {file_name} file")

    return db_params
