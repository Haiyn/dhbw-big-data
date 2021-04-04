from airflow.plugins_manager import AirflowPlugin
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException

import os
import requests
import json

class HttpDownloadOperator(BaseOperator):

    template_fields = ('download_uri', 'save_to')
    ui_color = '#26730a'

    @apply_defaults
    def __init__(
            self,
            download_uri,
            save_to,
            *args, **kwargs):
        """
        :param download_uri: http uri of file to download
        :type download_uri: string
        :param save_to: where to save file
        :type save_to: string
        """

        super(HttpDownloadOperator, self).__init__(*args, **kwargs)
        self.download_uri = download_uri
        self.save_to = save_to

    def execute(self, context):

        self.log.info("HttpDownloadOperator execution started.")

        self.log.info("Downloading '" + self.download_uri + "' to '" + self.save_to + "'.")
        page_num = 1

        while True:
            # Try downloading a page of cards
            try:
                r = requests.get(self.download_uri + "?page=" + str(page_num)).json()
            except requests.exceptions.RequestException as e:
                raise AirflowException("Failure, could not execute request. Exception: " + str(e))

            # Check if the cards array in the response is empty. If so, exit the loop
            if 'cards' not in r or len(r['cards']) == 0:
                self.log.info("HttpDownloadOperator done.")
                break

            # Append the data
            with open(save_to, "w+") as file:
                try:
                    existing = json.load(file)
                except Exception as e:
                    existing = { }
                existing.update(r)
                file.seek(0)
                json.dump(existing, file)

            # Increment page and continue
            page_num = page_num + 1
            self.log.info("Appended contents. Continuing on page " + page_num)

        self.log.info("HttpDownloadOperator done.")

