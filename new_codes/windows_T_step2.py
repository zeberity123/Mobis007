import os
import list_step_2
import cv2
from datetime import datetime

result_folder_name = f'20241116_213759_Injae2Anyang'
key_frames = '150625	158347	167065	178033	192977	197837	201623	210851	214571	221063	223223	233963	235523	240023	248229	252189	253517	259277	268747	270127	277153	288981	310757	316517	318491	338171'

key_frames = [i.strip() for i in key_frames.split('\t')]

print(key_frames)
# origin_tw_root = f'T:/'                                      
# home_root = f'T:/step1_241217'

origin_tw_root = r'\\192.168.3.2\FC3_NAS_007_vol2'
home_root = r'\\192.168.3.2\FC3_NAS_007_vol2\step1_241217'

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
    cnt+=1
    e1 = cv2.getTickCount()
    try:
        list_step_2.auto_step_2(i[0], i[1], i[2], i[3])
    except:
        error_list.append(f'{i[0].split('step_1_241203/')[1]} :: {i[3]}')
    e2 = cv2.getTickCount()

    total_time = (e2-e1)/cv2.getTickFrequency()
    print(f'Total time: {total_time}seconds.....{cnt}/{len(files_for_step_2)}')


time_now = datetime.now()
file_prefix = f'{time_now.strftime('%m%d%H%M')}'

error_txt = f'{result_folder_name}_error_step2_{file_prefix}.txt'
with open(error_txt, 'w+') as f:
    f.write('\n'.join(error_list))