import os
import pandas as pd

excel = 'excel_list.xlsx'

cols = ['folder_name']

def excel_to_folder_list(excel):
    df = pd.read_excel(excel, usecols='D', dtype={'folder_name': str}, names=cols, sheet_name=4, header=9)
    foldernames = df['folder_name'].to_list()
    return foldernames

folder_lists = excel_to_folder_list(excel)

nas_folders = [
    r'Y:',
    r'Z:\TW'
]
yuuv_list = []
for i in folder_lists[:10]:
    i_split = i.split('_')
    unique_num = i_split[2] + '_' + i_split[3]
    print(unique_num)