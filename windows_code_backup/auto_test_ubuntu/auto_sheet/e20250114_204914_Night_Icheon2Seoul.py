import os
import list_step_2
import cv2
from datetime import datetime
import pandas as pd

def step2(rfn, kfs):
    # result_folder_name = f'20250114_204914_Night_Icheon2Seoul'
    # key_frames = '125569'
    # key_frames = [i.strip() for i in key_frames.split('\t')]
    result_folder_name = rfn
    key_frames = [kfs]
    
    print(key_frames)
    origin_tw_root = f'Y:/MOBIS_MCAM1.0_18'                            
    home_root = f'Y:/MOBIS_MCAM1.0_18/step1_250115'

    result_folder_dir = f'{home_root}/{result_folder_name}'

    result_folder_vids = [f'{result_folder_dir}/{i}' for i in os.listdir(result_folder_dir) if len(i.split('_')) == 2]

    files_for_step_2 = []
    for folders in result_folder_vids:
        folder_temp_dirs = f'{folders}/Img_full'
        for img_files in os.listdir(folder_temp_dirs):
            img_num = img_files.split('.')[0]
            for key_num in key_frames:
                if int(img_num) == int(key_num):
                    # print(folders)
                    only_folder_name = folders.split('/')[-2]
                    original_vid_root = f'{origin_tw_root}/{only_folder_name}/Front/Video'
                    # print(original_vid_root)
                    files_for_step_2.append([folders, original_vid_root, original_vid_root, key_num])
                    
    error_list = []
    cnt = 0
    for i in files_for_step_2:
        print(i)
        cnt+=1
        e1 = cv2.getTickCount()
        try:
            list_step_2.auto_step_2(i[0], i[1], i[2], i[3])
            pass
        except:
            error_list.append(f'{i[0].split('step1_250115/')[1]} :: {i[3]}')
        e2 = cv2.getTickCount()

        total_time = (e2-e1)/cv2.getTickFrequency()
        print(f'Total time: {total_time}seconds.....{cnt}/{len(files_for_step_2)}')


    time_now = datetime.now()
    file_prefix = f'{time_now.strftime('%m%d%H%M')}'

    error_txt = f'{file_prefix}_error_step2.txt'
    with open(error_txt, 'w+') as f:
        f.write('\n'.join(error_list))

excel_file = '18_step2.xlsx'
cols_excel = ['l_g', 'm_g', 'kf']

def excel_to_list(excel_file):
    df = pd.read_excel(f'{excel_file}', engine='openpyxl', usecols='B:D', sheet_name=0, names=cols_excel, dtype={'l_g': str, 'm_g': str, 'kf': str})
    l_gs = df['l_g'].tolist()
    m_gs = df['m_g'].tolist()
    kfs = df['kf'].tolist()
    data_list = []
    for i in range(len(l_gs)):
        w = []
        w.append(l_gs[i])
        w.append(m_gs[i])
        w.append(kfs[i])
        data_list.append(w)
    return data_list[1:]


excel_list = excel_to_list(excel_file)
for i in excel_list:
    print(i)
    step2(i[0], i[2])