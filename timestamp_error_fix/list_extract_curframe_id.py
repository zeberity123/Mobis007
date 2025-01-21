import os
import pandas as pd
from datetime import datetime
import cv2

#====================================#
excel = 'excel_list.xlsx'
col_to_use = 'D'
drives = {
    'vol1': fr'Z:',
    'vol2': fr'Y:'
}
#====================================#

def excel_to_folder_list(excel):
    cols = ['folder_name']
    df = pd.read_excel(excel, usecols=col_to_use, dtype={'folder_name': str}, names=cols, sheet_name=4, header=9)
    folder_names = df['folder_name'].to_list()
    return folder_names

def get_all_yuuv(drives):
    folders_to_search = []
    for i in os.listdir(fr'{drives["vol1"]}\TW'):
        if len(i.split('_')) >= 2 and 'mcam_v5' not in i:
            folders_to_search.append(fr'{drives["vol1"]}\TW\{i}')

    for i in os.listdir(fr'{drives["vol2"]}'):
        if 'MOBIS' in i:
            for j in os.listdir(fr'{drives["vol2"]}\{i}'):
                if ('step1' not in j) and len(j.split('_')) >= 2:
                    folders_to_search.append(fr'{drives["vol2"]}\{i}\{j}')

    all_yuuv = []
    cnt = 0       
    for i in folders_to_search:
        cnt += 1
        temp_root = fr'{i}\Front\Video'
        try:
            for j in os.listdir(temp_root):
                if j.split('_')[-1] == '30Hz.bin':
                    all_yuuv.append(fr'{temp_root}\{j}')
        except:
            pass
        print(f'scanning... {cnt}/{len(folders_to_search)} :: {i}')

    for i in all_yuuv:
        print(i)
    print(f'n_of_yuuvs: {len(all_yuuv)}\n')
    
    return all_yuuv

def extract_info_from_yplane(raw_data):
    fid_up_u32 = int.from_bytes(raw_data[13:14], byteorder='little') << 24
    fid_up_u32 |= int.from_bytes(raw_data[15:16], byteorder='little') << 16
    fid_up_u32 |= int.from_bytes(raw_data[17:18], byteorder='little') << 8
    fid_up_u32 |= int.from_bytes(raw_data[19:20], byteorder='little') << 0
    fid_low_u32 = int.from_bytes(raw_data[21:22], byteorder='little') << 24
    fid_low_u32 |= int.from_bytes(raw_data[23:24], byteorder='little') << 16
    fid_low_u32 |= int.from_bytes(raw_data[25:26], byteorder='little') << 8
    fid_low_u32 |= int.from_bytes(raw_data[27:28], byteorder='little') << 0

    frame_id = int(fid_up_u32) << 32
    frame_id |= fid_low_u32

    return int(frame_id)

def extract_single_curfram_id(yuuv_file):
    with open(yuuv_file, 'rb') as raw_video_f:
        raw_video_data = raw_video_f.read(4147264)#raw_video_f.read(4147200)
        cur_frameid = extract_info_from_yplane(raw_video_data[64:])
        
    return cur_frameid

folder_lists = excel_to_folder_list(excel)
all_yuuv = get_all_yuuv(drives)

curframe_dict = {}
unique_nums = {}

e1 = cv2.getTickCount()
cnt = 0
for i in folder_lists:
    cnt += 1
    i_split = i.split('_')
    unique_num = i_split[2] + '_' + i_split[3]
    if unique_num in unique_nums:
        curframe_dict[i] = unique_nums[unique_num]
    else:
        for j in all_yuuv:
            if unique_num in j:
                cur_frameid = extract_single_curfram_id(j)
                curframe_dict[i] = cur_frameid
                unique_nums[unique_num] = cur_frameid
                break
    
    print(f'extracting... {cnt}/{len(folder_lists)} :: {i}')

e2 = cv2.getTickCount()
total_time = (e2-e1)/cv2.getTickFrequency()
print(f'total_time: {total_time}')

df = pd.DataFrame(data=curframe_dict, index=[0])
df = (df.T)
time_now = datetime.now()
file_suffix = f'{time_now.strftime("%m%d%H%M")}'
df.to_excel(f'curframe_ids_{file_suffix}.xlsx')