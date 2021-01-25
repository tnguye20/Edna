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
def get_masked_frame(df, pattern):
    return df[df['content'].str.contains(pattern, flags=re.IGNORECASE, regex=True)]

def get_general_statistics(df, parentDf=None):
    data = {}
    
    totalText = df.shape[0]
    participants = df['sender'].unique().tolist()
    years = df['year'].unique().tolist()
    months = np.sort(df['month'].unique()).tolist()
    
    data['totalText'] = totalText
    data['participants'] = participants
    
    #Mean
    data['means'] = {}
    data['means']['year'] = totalText / len(years) if len(years) > 0 else 0
    
    range_df = parentDf if parentDf is not None else df
    
    if(range_df.shape[0] > 0 and df.shape[0] > 0):
        delta = range_df['timestamp'].iloc[-1] - range_df['timestamp'].iloc[0] 
        delta_month = math.ceil(delta/np.timedelta64(1, 'M'))
        delta_day = math.ceil(delta/np.timedelta64(1, 'D'))
        data['totalMonth'] = delta_month
        data['totalDay'] = delta_day
        data['means']['month'] = (totalText / delta_month) if delta_month > 0 else totalText
        data['means']['day'] = (totalText / delta_day) if delta_day > 0 else totalText

        data['first_record_timestamp'] = df.iloc[0]['timestamp']
        data['last_record_timestamp'] = df.iloc[-1]['timestamp']
    else:
        data['totalMonth'] = 0
        data['totalDay'] = 0
        data['means']['month'] = totalText
        data['means']['day'] = totalText

        data['first_record_timestamp'] = None
        data['last_record_timestamp'] = None

    data['years'] = years
    data['months'] = months
    
    return data