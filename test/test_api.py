
import json
import os

import pytest
from scripts.gl_epic_data_export import GLExportEpics

config_folder = 'scripts/config'
config_file = 'config.json'

ob = GLExportEpics(config_folder=config_folder, config_file=config_file)
config = json.load(open("{}/{}".format(config_folder, config_file)))


def test_authentication():
    '''
        Test if the endpoint is working
    '''
    result = ob.__GetEpicData__(config["endpoint"])
    assert result.status_code == 200


def test_return_data_type():
    '''
        Test the data type of returned data
    '''
    result = ob.__GetEpicData__(config["endpoint"])
    assert isinstance(result.json()[0], dict)


def test_output_directory_access():
    '''
        Test output directory writeable
    '''
    assert os.access('./', os.W_OK)
