import tempfile
from os import path, makedirs
from shutil import rmtree
import zipfile
import re
import csv

import numpy as np 
import pandas as pd
import math
from collections import OrderedDict

from libs import firebase
linePattern = re.compile(r'\[([\d\/]+), ([\d:]+)\]([\w\s]+):(.*)$')

def verifyPOST(request):
    headers = request.headers;
    if 'AUTH-TOKEN' in headers:
        decoded_token = firebase.auth.verify_id_token(headers['AUTH-TOKEN'])
        return decoded_token["uid"]
    raise Exception('Invalid Credentials')

def getTmpDir():
    return tempfile.gettempdir()

def downloadFile(uid, filename, customFileName=None):
    tempdir = tempfile.gettempdir()
    bucket = firebase.storage.bucket()

    fullPath = f'{uid}/WhatsApp/{filename}'
    downloadPath = path.join(tempdir, uid, 'WhatsApp')
    downloadFilePath = path.join(downloadPath, customFileName if customFileName != None else filename)
    if(path.isdir(downloadPath)):
        rmtree(downloadPath)
    makedirs(downloadPath, exist_ok=True)

    blob = bucket.blob(fullPath)
    blob.download_to_filename(downloadFilePath)

    return [downloadPath, downloadFilePath]

def uploadFile(localFilePath, destinationFilePath):
    bucket = firebase.storage.bucket()
    blob = bucket.blob(destinationFilePath)
    blob.upload_from_filename(localFilePath)

def saveToBucket(uid, localFilePath):
    filename = localFilePath.split('/')[-1]
    bucketPath = f'{uid}/WhatsApp/{filename}'
    uploadFile(localFilePath, bucketPath)

def extractZip(dirPath, filePath):
    with zipfile.ZipFile(filePath, 'r') as zip_ref:
        zip_ref.extractall(dirPath)

def parseChatData(chatFilePath):
    data = []
    with open(chatFilePath, 'r') as fp:
        for cnt, line in enumerate(fp):
            match = linePattern.search(line)
            if(match):
                date = match.group(1)
                time = match.group(2)
                sender = match.group(3)
                content = match.group(4)

                month, day, year = date.split('/')
                day = '0' + day if len(day) == 1 else day
                month = '0' + month if len(month) == 1 else month
                formattedDate = f'20{year}-{month}-{day}';
                timestamp = f'{formattedDate} {time}'

                data.append({
                    'date': formattedDate,
                    'time': time,
                    'timestamp': timestamp,
                    'sender': sender.strip(),
                    'content': content.strip(),
                    'type': 'text'
                })
            else:
                data[-1]['content'] = data[-1]['content'] + '\n' + line
    fp.close()
    return data

def chatToCSV(chatFilePath, data):
    with open(chatFilePath.replace('txt', 'csv'), 'w') as f:
        header = [
            'date',
            'time',
            'timestamp',
            'sender',
            'content',
            'type'
        ]
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        w.writerows(data)






## Data Funcs
def getLoveMask(df):
    return df['content'].str.contains('((I |me )(still |just )?(l|w)ove (you|u))|(^(l|w)ove (you|u))', flags=re.IGNORECASE, regex=True)

def getMissMask(df):
    return df['content'].str.contains('((I |me )(still |just )?miss (you|u))|(^miss (you|u))', flags=re.IGNORECASE, regex=True)

def getMask(df, pattern):
    return df['content'].str.contains(pattern, flags=re.IGNORECASE, regex=True)

def getGeneralStatistic(df):
    data = OrderedDict()
    
    totalText = df.shape[0]
    participants = df['sender'].unique().tolist()
    years = df['year'].unique().tolist()
    months = np.sort(df['month'].unique()).tolist()
    
    data['totalText'] = totalText
    data['participants'] = participants
    
    #Mean
    data['means'] = OrderedDict()
    data['means']['year'] = totalText / len(years) if len(years) > 0 else 0

    data['years'] = years
    data['months'] = months

    if(df.shape[0] > 0):
        delta = df['timestamp'].iloc[-1] - df['timestamp'].iloc[0] 
        delta_month = math.ceil(delta/np.timedelta64(1, 'M'))
        delta_day = math.ceil(delta/np.timedelta64(1, 'D'))
        data['totalMonth'] = delta_month
        data['totalDay'] = delta_day
        data['means']['month'] = (totalText / delta_month) if delta_month > 0 else totalText
        data['means']['day'] = (totalText / delta_day) if delta_day > 0 else totalText

        data['first_record_timestamp'] = df.iloc[0]['timestamp']
        data['last_record_timestamp'] = df.iloc[-1]['timestamp']
        # data['first_record_timestamp'] = df.iloc[0]['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        # data['last_record_timestamp'] = df.iloc[-1]['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    else:
        data['totalMonth'] = 0
        data['totalDay'] = 0
        data['means']['month'] = totalText
        data['means']['day'] = totalText

        data['first_record_timestamp'] = None
        data['last_record_timestamp'] = None
    
    return data