import parameters
import os
import re
import requests
import jwt
import time
import sqlite3
import json
import concurrent.futures
import queue
import threading


def save_to_file(data, file_path):
    with open(file_path, 'w') as file:
        # file.write(data)
        json.dump(data, file)


def load_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def generate_jwt_token(client_id, client_secret):
    # Replace with the appropriate token endpoint URL for your OAuth server
    token_endpoint = "https://web.arbeitsagentur.de/weiterbildungssuche/suche"

    now = int(time.time())
    payload = {
        "iss": client_id,
        "sub": client_id,
        "aud": token_endpoint,
        "iat": now,
        "exp": now + 3600,  # Token expires in 1 hour
    }

    # Sign the payload with your client secret to generate the JWT
    jwt_token = jwt.encode(payload, client_secret, algorithm='HS256')

    return jwt_token


def get_access_token(client_id, client_secret):
    # Generate the JWT token
    jwt_token = generate_jwt_token(client_id, client_secret)

    # Request the access token using the JWT token
    token_endpoint = "https://rest.arbeitsagentur.de/oauth/gettoken_cc"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(token_endpoint, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(
            f"Failed to get access token. Status code: {response.status_code}")


def get_api_data(api_url, access_token, params=None):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    print(params)
    response = requests.get(api_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def stripHtmlTagsFromString(text):
    CLEANR = re.compile(
        '<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6})|(--)+|;+|=+|ewa-rteLine+|\[|\]|●+')
    cleanText = re.sub(CLEANR, '', str(text))
    return cleanText


def create_table(db_connection):
    cursor = db_connection.cursor()
    # Create a table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS weiterbildung_data
                        (
                            angebot_id INT,
                            angebot_titel TEXT NULL,
                            angebot_inhalt TEXT NULL,
                            angebot_abschlussbezeichnung TEXT NULL,
                            angebot_foerderung TEXT NULL,
                            angebot_zielgruppe TEXT NULL,
                            bildungsart_bezeichnung TEXT NULL
                        )
                   ''')
    db_connection.commit()


def insert_data_into_db(data, db_connection):
    cursor = db_connection.cursor()
    for entry in data:
        angebot = entry['angebot']
        cursor.execute('''INSERT INTO weiterbildung_data (
                    angebot_id,
                    angebot_titel,
                    angebot_inhalt,
                    angebot_abschlussbezeichnung,
                    angebot_foerderung,
                    angebot_zielgruppe,
                    bildungsart_bezeichnung
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            angebot["id"],
            stripHtmlTagsFromString(angebot["titel"]),
            stripHtmlTagsFromString(angebot["inhalt"]),
            stripHtmlTagsFromString(angebot["abschlussbezeichnung"]),
            stripHtmlTagsFromString(angebot["foerderung"]),
            stripHtmlTagsFromString(angebot["zielgruppe"]),
            angebot["bildungsart"]["bezeichnung"]
        ))
    db_connection.commit()
    print("insert data")


# load data with all filters
param = parameters.init()
print(parameters.regions)


# Pagination: Fetch all data from the API using multiple requests
def pagination(api_url, access_token, db_connection, params, data_queue, page):
    last_page = 20
    params = params.copy()
    params["page"] = page
    api_data = get_api_data(api_url, access_token, params)
    if last_page != 0:
        data_queue.put(api_data["_embedded"]["termine"])
        # insert_data_into_db(api_data["_embedded"]["termine"], db_connection)
        # writer_thread(db_connection, data_queue)
        if page < last_page - 1:
            pagination(api_url, access_token, db_connection,
                       params, data_queue, page + 1)


def writer_thread(db_connection, data_queue):
    while True:
        data = data_queue.get()
        if data is None:
            # Signal to exit
            break
        print("insertion", len(data))
        insert_data_into_db(data)
        data_queue.task_done()


def fetch_data(db_connection, data_queue, params=None):
    # Replace with the API endpoint URL
    api_url = "https://rest.arbeitsagentur.de/infosysbub/wbsuche/pc/v2/bildungsangebot"
    data_file = "data_json.txt"
    # Replace with your OAuth client ID
    client_id = "38053956-6618-4953-b670-b4ae7a2360b1"
    # Replace with your OAuth client secret
    client_secret = "c385073c-3b97-42a9-b916-08fd8a5d1795"

    # Get the access token using client credentials flow with JWTs
    access_token = get_access_token(client_id, client_secret)
    regions = parameters.regions
    dauer = parameters.dauer
    beginntermin = parameters.beginntermin
    unterrichtsform = parameters.unterrichtsform

    # Adjust max_workers as needed
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for region_item in regions:
            print(region_item)
            for dauer_item in dauer:
                for begintermin in beginntermin:
                    for urf in unterrichtsform:
                        for uz in parameters.unterrichtszeit:
                            for sys in parameters.systematik:
                                params = {
                                    "re": region_item,
                                    "uk": "Bundesweit",
                                    "uf": urf,
                                    "bt": begintermin,
                                    "dauer": dauer_item,
                                    "uz": uz,
                                    "sys": sys,
                                    "size": 20  # Limit per page as per API's limitation
                                }
                                futures.append(executor.submit(
                                    pagination, api_url, access_token, db_connection, params, data_queue, 0))

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)


def main():
    # Open a connection
    db_connection = sqlite3.connect('weiterbildung_new_data.db')
    create_table(db_connection)

    data_queue = queue.Queue()

    fetch_data(db_connection, data_queue)

    # Process the fetched data from the queue and insert into the database
    while not data_queue.empty():
        data = data_queue.get()
        print(len(data))
        insert_data_into_db(data, db_connection)
        data_queue.task_done()

    # Close the database connection
    db_connection.close()


if __name__ == "__main__":
    main()
