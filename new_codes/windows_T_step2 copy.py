import os
import list_step_2
import cv2
from datetime import datetime

# 경로와 관련된 변수
result_folder_name = '20241116_201936_Hangyeryung2Inje'
key_frames = '74327	113453	114713	116213'

key_frames = [i.strip() for i in key_frames.split('\t')]

# 경로 설정 (Windows 환경에 맞게 수정)
origin_tw_root = r'\\192.168.3.2\FC3_NAS_007_vol2\MOBIS_vol_2'  # 네트워크 경로
home_root = r'\\192.168.3.2\FC3_NAS_007_vol2\MOBIS_vol_2\step1_241217'  # 네트워크 경로

# 결과 폴더 경로 설정
result_folder_dir = os.path.join(home_root, result_folder_name)

# 비디오 폴더 리스트
result_folder_vids = [
    os.path.join(result_folder_dir, i) for i in os.listdir(result_folder_dir) if len(i.split('_')) == 2
]

# step2 처리할 파일 목록 생성
files_for_step_2 = []
for folders in result_folder_vids:
    folder_temp_dirs = os.path.join(folders, 'Img_full')
    for img_files in os.listdir(folder_temp_dirs):
        img_num = img_files.split('.')[0]
        for key_num in key_frames:
            if int(img_num) == int(key_num):
                only_folder_name = folders.split('\\')[-2]
                original_vid_root = os.path.join(origin_tw_root, only_folder_name, 'Front', 'Video')
                files_for_step_2.append([folders, original_vid_root, original_vid_root, key_num])

# 오류 리스트와 처리 카운트
error_list = []
cnt = 0
for i in files_for_step_2:
    cnt += 1
    e1 = cv2.getTickCount()
    try:
        list_step_2.auto_step_2(i[0], i[1], i[2], i[3])
    except Exception as e:
        error_list.append(f'{i[0].split("step_1_241203\\")[1]} :: {i[3]}')
    e2 = cv2.getTickCount()

    total_time = (e2 - e1) / cv2.getTickFrequency()
    print(f'Total time: {total_time} seconds.....{cnt}/{len(files_for_step_2)}')

# 오류 파일 저장
time_now = datetime.now()
file_prefix = f'{time_now.strftime("%m%d%H%M")}'

error_txt = f'{result_folder_name}_error_step2_{file_prefix}.txt'
with open(error_txt, 'w+') as f:
    f.write('\n'.join(error_list))
