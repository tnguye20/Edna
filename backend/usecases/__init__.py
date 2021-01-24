from os import path
from utils import *
# from daos import UserDao
import numpy as np
import pandas as pd
import re

def load_data(uid, filename):
    downloadPath, downloadFilePath = downloadFile(uid, filename, 'chat.zip')
    saveToBucket(uid, downloadFilePath)

    extractZip(downloadPath, downloadFilePath)

    # Download Data
    chatFilePath = path.join(downloadPath, '_chat.txt')
    saveToBucket(uid, chatFilePath)

    # Parse Data
    data = parseChatData(chatFilePath)
    chatToCSV(chatFilePath, data)
    saveToBucket(uid, chatFilePath.replace('txt', 'csv'))

    # Save Data to DB
    # userDao = UserDao(uid)
    # userDao.updateChatHistory(data);
    # userDao.updateChatHistory(list(map(lambda x: x['content'], data)));

def generate_all_data(uid, filePath):
    # Ensure CSV file is there before proceeding
    if(not path.isfile(filePath)):
        downloadFile(uid, filePath.split('/').pop())

    currentPath = '/'.join(filePath.split('/')[0:-1])

    #Load chat data into DataFrame
    chat = pd.read_csv(filePath)
    chat['timestamp'] = pd.to_datetime(chat['timestamp'])
    chat['date'] = pd.to_datetime(chat['date'])
    chat['month'] = pd.DatetimeIndex(chat['timestamp']).month
    chat['year'] = pd.DatetimeIndex(chat['timestamp']).year
    chat['month-year'] = pd.to_datetime(chat['timestamp']).dt.to_period('M')

    #Setup Masks
    LOVE_MASK = getLoveMask(chat)
    MISS_MASK = getMissMask(chat)
    love_chat = chat[LOVE_MASK]
    miss_chat = chat[MISS_MASK]

    #Init Data Collection
    data = getGeneralStatistic(chat)
    data['annual_statistic'] = OrderedDict()
    data['love_statistic'] = getGeneralStatistic(love_chat)
    data['miss_statistic'] = getGeneralStatistic(miss_chat)

    for year in data['years']:
        _chat = chat[chat['year'] == year]
        year = str(year)
        _love_chat = _chat[getLoveMask(_chat)]
        _miss_chat = _chat[getMissMask(_chat)]
        data['annual_statistic'][year] = getGeneralStatistic(_chat) 
        data['annual_statistic'][year]['love_statistic'] = getGeneralStatistic(_love_chat)
        data['annual_statistic'][year]['miss_statistic'] = getGeneralStatistic(_miss_chat)
        
        data['annual_statistic'][year]['monthly_statistic'] = OrderedDict()
        for month in _chat['month'].unique():
            _month_chat = _chat[_chat['month'] == month]
            month = str(month)
            data['annual_statistic'][year]['monthly_statistic'][month] = getGeneralStatistic(_month_chat)

    return data