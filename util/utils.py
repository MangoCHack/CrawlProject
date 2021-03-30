import os
import argparse
import sqlite3
from typing import Dict, Optional
from urllib.parse import urlparse
import socket

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'E:\\Project\\CrawlProject\\crawler\\googlekey\\ardent-strength-309105-f9e6b458ea6a.json'

def get_ip(url : str):
    baseUrl = urlparse(url)
    hostname = baseUrl.hostname
    port = baseUrl.port or (443 if baseUrl.scheme == 'https' else 80)
    ip = socket.getaddrinfo(hostname,port)[0][4][0]

    return ip

def connect_database(dbName : str):
    with sqlite3.connect(dbName) as dbConnection:
        return dbConnection

def initialize_database(dbName : str):
    dbConnection = connect_database(dbName)
    cursor = dbConnection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS illegal_sites(
            main_url TEXT PRIMARY KEY,
            scheme TEXT,
            main_html_path TEXT,
            captured_url TEXT,
            captured_file_path TEXT,
            google_analytics_code TEXT,
            telegram_url TEXT,
            twitter_url TEXT,
            similarity_group TEXT,
            engine TEXT,
            next_url TEXT,
            expected_category TEXT,
            visited BOOLEAN,
            site_available BOOLEAN,
            ip_address TEXT,
            created_at TEXT,
            last_visited_at TEXT
        )
    """
    )
    dbConnection.commit()
    return dbConnection

def initialize_database2(dbName : str):
    dbConnection = connect_database(dbName)
    cursor = dbConnection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sites_connection(
            main_url TEXT,
            main_ip TEXT,
            connect_url TEXT,
            connect_ip TEXT
        )
    """
    )
    dbConnection.commit()
    return dbConnection

def insert_row(dbConnection, row: Dict[str, Optional[str]]):
    connection = dbConnection
    with connection:
        cursor = connection.cursor()
        sql = f"""
            INSERT OR REPLACE INTO illegal_sites VALUES (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
        """
        cursor.execute(
            sql,
            (
                row["main_url"],
                row["scheme"],
                row["main_html_path"],
                row["captured_url"],
                row["captured_file_path"],
                row["google_analytics_code"],
                row["telegram_url"],
                row["twitter_url"],
                row["similarity_group"],
                row["engine"],
                row["next_url"],
                row["expected_category"],
                row["visited"],
                row["site_available"],
                row["ip_address"],
                row["created_at"],
                row["last_visited_at"],
            ),
        )
        connection.commit()
    return connection


def update_row(dbConnection, row: Dict[str, Optional[str]]):
    connection = dbConnection
    with connection:
        cursor = connection.cursor()
        # None으로 업데이트하지 않을 것이라고 가정
        will_be_updated = [
            (key, value)
            for key, value in row.items()
            if value is not None and key != "main_url"
        ]

        for key, value in will_be_updated:
            # {trim_url(row['main_url'])}
            sql = f"""
                UPDATE illegal_sites 
                SET {key} = ? 
                WHERE main_url = ?
                """

            cursor.execute(sql, (value, row["main_url"]))
        connection.commit()
    return connection


def select_urls_by_category(db_conection, category):
    connection = db_conection
    with connection:
        cursor = connection.cursor()

        sql = f"""
            SELECT main_url
            FROM illegal_sites
            WHERE expected_category = ?
        """

        result = cursor.execute(sql, (category,))

        connection.commit()
        return [url for (url,) in result.fetchall()]


def select_unstored_urls(dbConnection):
    connection = dbConnection
    with connection:
        cursor = connection.cursor()

        sql = f"""
            SELECT main_url
            FROM illegal_sites
            WHERE visited = ?
        """

        result = cursor.execute(sql, (False,))

        connection.commit()
        return [url for (url,) in result.fetchall()]


def select_all_urls(db_conection):
    connection = db_conection
    with connection:
        cursor = connection.cursor()

        sql = f"""
            SELECT main_url
            FROM illegal_sites
        """

        result = cursor.execute(sql)

        connection.commit()
        return [url for (url,) in result.fetchall()]

def select_all_fullurls(db_conection):
    connection = db_conection
    with connection:
        cursor = connection.cursor()

        sql = f"""
            SELECT main_url, scheme 
            FROM illegal_sites
        """

        result = cursor.execute(sql)

        connection.commit()
        return [scheme+url for (url,scheme) in result.fetchall()]


def select_available_urls(db_conection):
    connection = db_conection
    with connection:
        cursor = connection.cursor()

        sql = f"""
            SELECT main_url
            FROM illegal_sites
            WHERE site_available = ?
        """

        result = cursor.execute(sql, (True,))

        connection.commit()
        return [url for (url,) in result.fetchall()]


def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    result = ''
    for text in texts:
        result += '{}'.format(text.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return result

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_text_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    try:
        response = client.text_detection(image=image)
    except Exception as e:
        print('Error :' + str(e))
        return "Error : " + str(e)
    texts = response.text_annotations
    result = ''
    #print('Texts:')
    
    for text in texts:
        result += '{}'.format(text.description)
        #print('\n"{}"'.format(text.description))
        #print(result)
    '''
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
    '''
    if response.error.message:
        return "Error :" + str(Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message)))
    
    return result