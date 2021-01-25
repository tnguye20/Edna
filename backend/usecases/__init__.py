from os import path
from utils import *
from daos import UserDao
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
    data['annual_statistics'] = OrderedDict()
    data['love_statistic'] = getGeneralStatistic(love_chat)
    data['miss_statistic'] = getGeneralStatistic(miss_chat)

    for year in data['years']:
        _chat = chat[chat['year'] == year]
        year = str(year)
        _love_chat = _chat[getLoveMask(_chat)]
        _miss_chat = _chat[getMissMask(_chat)]
        data['annual_statistics'][year] = getGeneralStatistic(_chat)
        data['annual_statistics'][year]['love_statistic'] = getGeneralStatistic(_love_chat)
        data['annual_statistics'][year]['miss_statistic'] = getGeneralStatistic(_miss_chat)

        data['annual_statistics'][year]['monthly_statistics'] = OrderedDict()
        for month in _chat['month'].unique():
            _month_chat = _chat[_chat['month'] == month]
            _month_love_chat = _month_chat[getLoveMask(_month_chat)]
            _month_miss_chat = _month_chat[getMissMask(_month_chat)]
            month = str(month)
            data['annual_statistics'][year]['monthly_statistics'][month] = getGeneralStatistic(_month_chat)
            data['annual_statistics'][year]['monthly_statistics'][month]['love_statistic'] = getGeneralStatistic(_month_love_chat)
            data['annual_statistics'][year]['monthly_statistics'][month]['miss_statistic'] = getGeneralStatistic(_month_miss_chat)

    return data

def get_user_statistics(uid):
    userDao = UserDao(uid)
    data = userDao.getUser()
    return data['statistics']

def get_formatted_data(uid):
    statistics = get_user_statistics(uid)
    annual_data = []
    monthly_data = []

    for year in statistics['years']:
        year = str(year)
        annual_statistic = statistics['annual_statistics'][year]
        annual_data.append({
            "label": year,
            "data": annual_statistic["totalText"],
        })
        
        months = annual_statistic["months"]
        for month in months:
            month = str(month)
            monthly_statistic = annual_statistic['monthly_statistics'][month]
            monthly_data.append({
                "label": f'{year}-{month}',
                "data": monthly_statistic["totalText"],
            })

    payload = {
        "annual_data": annual_data,
        "monthly_data": monthly_data
    }
    return payload