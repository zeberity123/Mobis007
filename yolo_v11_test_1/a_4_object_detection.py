import pandas as pd
from ultralytics import YOLO
import numpy as np
import cv2
import os

excel_filename = '현대모비스 NX4 Curation 상세 현황.xlsx'
cols_excel = ['nas_folder', 'p_folder', 
              's_folder', 'n_png', 'n_json', 'n_pcd', 'n_raw', 'n_yuv', 'bo', 'keyframe_condition', 'day_night', 'objects_a4']
excel_data = pd.read_excel(excel_filename, sheet_name=2, usecols='B:M', names=cols_excel)

excel_data = excel_data[15:]

nas_folder = excel_data['nas_folder'].tolist()
p_folder = excel_data['p_folder'].tolist()
s_folder = excel_data['s_folder'].tolist()
keyframe_condition = excel_data['keyframe_condition'].tolist()
objects_a4 = excel_data['objects_a4'].tolist()

keyframes_a4 = []
nas_root = f'/run/user/1000/gvfs/smb-share:server=192.168.2.1,share=fc3_nas_007/step_1_241203'
for i in range(len(keyframe_condition)):
# for i in range(95):
    conditions = keyframe_condition[i].split(',')
    if 'A-4' in conditions or ' A-4' in conditions:
        print(i, nas_folder[i], p_folder[i], s_folder[i], keyframe_condition[i], objects_a4[i])
        digit_6 = s_folder[i].split('_')[-1].zfill(6)
        img_address = f'{nas_root}/{p_folder[i]}/{s_folder[i]}/img/{digit_6}.png'
        # print(img_address)
        keyframes_a4.append([i+17, nas_folder[i], p_folder[i], s_folder[i], keyframe_condition[i], objects_a4[i], img_address])

model = YOLO("yolo11x.pt")

print(f'n_of_file to process: {len(keyframes_a4)}\n')

detection_results = []
cnt = 0
file_root_errors = []
e1 = cv2.getTickCount()
for keyframe in keyframes_a4:
    cnt += 1
    img_root = keyframe[6]
    # print(img_root)
    if os.path.exists(img_root):
        p_results = model(img_root)
        s_result = p_results[0].summary()
        # print(s_result)
        temp_classes = {'car': 0, 'bicycle': 0, 'motorcycle': 0, 'person': 0}
        for i in s_result:
            object_name = i['name']
            if object_name in temp_classes.keys():
                temp_classes[object_name] += 1
                
        new_filename = keyframe[1] + '/' + keyframe[2] + '/' + keyframe[3]
        new_img_name = keyframe[2] + '_' + keyframe[3].split('_')[-1].zfill(6)
        p_results[0].save(f'detection_results_1219/{new_img_name}.png')

        detection_results.append(f'{new_filename} => car: {temp_classes['car']}, bicycle: {temp_classes['bicycle']}, motorcycle: {temp_classes['motorcycle']}, person: {temp_classes['person']}')
    else:
        new_filename = keyframe[1] + '/' + keyframe[2] + '/' + keyframe[3]
        detection_results.append(f'{new_filename} :: error')
        file_root_errors.append(f'{new_filename} :: error')

    print(f'scanning...{cnt}/{len(keyframes_a4)}\n')
e2 = cv2.getTickCount()
t_time = (e2-e1)/cv2.getTickFrequency()
print(f'Total_time: {t_time} seconds')

with open('detection_result_1219.txt', '+w') as f:
    f.write('\n'.join(detection_results))
