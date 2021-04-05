import os
import requests
import json
import logging

download_uri = "https://api.magicthegathering.io/v1/cards"
save_to = "raw.json"


logging.warn("HttpDownloadOperator execution started.")

logging.warn("Downloading '" + download_uri + "' to '" + save_to + "'.")
page_num = 1

while True:
    # Try downloading a page of cards
    try:
        r = requests.get(download_uri + "?page=" + str(page_num)).json()
    except requests.exceptions.RequestException as e:
        logging.warn("Failure, could not execute request. Exception: " + str(e))

    # Check if the cards array in the response is empty. If so, exit the loop
    if 'cards' not in r or len(r['cards']) == 0:
        logging.warn("HttpDownloadOperator done.")
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


