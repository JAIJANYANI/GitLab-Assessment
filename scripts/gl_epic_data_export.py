import logging
from datetime import datetime

import pandas as pd
import requests
import json


class GLExportEpics:
    """
    Contains the functions which helps in exporting Epics data from GitLab into a tabular format
    """

    def __init__(self, config_folder, config_file, *args, **kwargs):
        """
        This is a constructor method.

        :param config_file: config file name to get requred details such as access_token, group_id etc
        :param config_folder: config path

        """

        super(GLExportEpics, self).__init__(*args, **kwargs)
        self.config_file = config_file
        self.config_folder = config_folder
        self.config = json.load(
            open("{}/{}".format(self.config_folder, self.config_file)))

        # As this is a standalone script, getting the access_token from local
        self.access_token = self.config['access_token']
        # Group ID to fetch relevant data according to requirements
        self.group_id = self.config['group_id']
        # Endpoint to get epic data
        self.endpoint = self.config['endpoint']
        # Output file name to store final data
        self.output_filename = self.config['output_filename']

    def __GetEpicData__(self, endpoint):
        """
        This method is used to get the epic data using the configured api endpoint

        :param endpoint: endpoint url to get epic data
        :return: raw json structure direct from API

        """

        endpoint = endpoint.format(self.group_id)

        payload = {}
        headers = {
            'PRIVATE-TOKEN': self.access_token
        }

        response = requests.request(
            "GET", endpoint, headers=headers, data=payload)
        if response.status_code == 200:
            return response
        else:
            raise ValueError("API Returned error : ", response.text)

    def __SerializeData__(self, data):
        """
        This method is used to serialize the json data into pandas dataframe data

        :param data: data in dataframe format
        :return: data in tabular format

        """
        df = pd.DataFrame(data.json())
        return df

    def __TransformData__(self, data):
        """
        This method is used to transform the json data into required format

        :param data: data in dataframe format
        :return: data in required format

        """
        ## Selecting specific columns only
        data = data[['id', 'group_id', 'title', 'author', 'created_at']]
        ## Extracting author name from nested structure 
        data['author'] = data['author'].apply(lambda x: x['username'])
        return data

    def __ExportData__(self, data):
        """
        This method is used to export the data into tabular/csv format, with headers as first row

        :param data: data in dataframe format
        :return: None

        """
        data.to_csv(self.output_filename, index=False)

    def __execute__(self):
        """
        This method is used to execute function in order
        :return: True

        """
        json_data = self.__GetEpicData__(self.endpoint)
        df_data = self.__SerializeData__(json_data)
        df_data = self.__TransformData__(df_data)
        self.__ExportData__(df_data)
        logging.info("Data exported successfully, please take a look at ", self.output_filename)
        return True


if __name__ == "__main__":
    config_folder = 'config'
    config_file = 'config.json'
    GLExportEpics(config_folder, config_file).__execute__()
