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

def get_masked_data(masks, df):
    data = {}
    for mask in masks:
        data[mask['name']] = get_general_statistics(get_masked_frame(df, mask['pattern']), df)
    return data

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

    masks = get_user_masks(uid)

    #Init Data Collection
    data = get_general_statistics(chat)
    data['annual_statistics'] = OrderedDict()
    data['masks'] = get_masked_data(masks, chat)

    for year in data['years']:
        print(year)
        _chat = chat[chat['year'] == year]
        year = str(year)
        data['annual_statistics'][year] = get_general_statistics(_chat)
        data['annual_statistics'][year]['masks'] = get_masked_data(masks, _chat)

        data['annual_statistics'][year]['monthly_statistics'] = OrderedDict()
        for month in _chat['month'].unique():
            _month_chat = _chat[_chat['month'] == month]
            month = str(month)
            data['annual_statistics'][year]['monthly_statistics'][month] = get_general_statistics(_month_chat)
            data['annual_statistics'][year]['monthly_statistics'][month]['masks'] = get_masked_data(masks, _month_chat)

    return data

def get_user_statistics(uid):
    userDao = UserDao(uid)
    data = userDao.getUser()
    return data['statistics']

def get_user_masks(uid):
    userDao = UserDao(uid)
    data = userDao.getUser()
    return data['masks']

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