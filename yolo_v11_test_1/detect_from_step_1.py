import pandas as pd
from ultralytics import YOLO
import numpy as np
import cv2
import os

nas_root = f'Z:/step_1_241203'
save_root = f'Y:/vol_1_detection'
keyframes_list = []

b_folder_list = os.listdir(nas_root)
for b_folder in b_folder_list:
    m_folder_list = os.listdir(f'{nas_root}/{b_folder}')
    for m_folder in m_folder_list:
        if len(m_folder.split('_')) == 2:
            keyframes = os.listdir(f'{nas_root}/{b_folder}/{m_folder}/Img_full')
            for keyframe in keyframes:
                keyframes_list.append(f'{nas_root}/{b_folder}/{m_folder}/Img_full/{keyframe}')


# print(len(keyframes_list))


model = YOLO("yolo11x.pt")

print(f'n_of_file to process: {len(keyframes_list)}\n')

detection_results = []
cnt = 0
only_a4_list = []
e1 = cv2.getTickCount()

with open('step1_detection_result_1224.txt', '+w') as f:
    f.write('\n'.join(detection_results))

with open('step1_only_a4_list.txt', '+w', encoding='utf-8') as f:
    f.write('\n'.join(only_a4_list))

for keyframe in keyframes_list:
    cnt += 1
    img_root = keyframe
    # print(img_root)
    p_results = model(img_root)
    s_result = p_results[0].summary()
    # print(s_result)
    temp_classes = {'car': 0, 'bicycle': 0, 'motorcycle': 0, 'person': 0}
    for i in s_result:
        object_name = i['name']
        if object_name in temp_classes.keys():
            temp_classes[object_name] += 1
            
    new_filename = keyframe
    key_names = keyframe.split('/')
    save_root_mkdir = f'{save_root}/{key_names[-4]}/{key_names[-3]}'
    # os.makedirs(save_root_mkdir, exist_ok=True)
    # p_results[0].save(f'{save_root_mkdir}/{key_names[-1]}')

    # detection_results.append(f"{new_filename} => car: {temp_classes['car']}, bicycle: {temp_classes['bicycle']}, motorcycle: {temp_classes['motorcycle']}, person: {temp_classes['person']}")
    with open('step1_detection_result_1224.txt', 'a', encoding='utf-8') as f:
        f.write(f"{new_filename} => car: {temp_classes['car']}, bicycle: {temp_classes['bicycle']}, motorcycle: {temp_classes['motorcycle']}, person: {temp_classes['person']}\n")
    if temp_classes['bicycle'] + temp_classes['motorcycle'] + temp_classes['person'] >= 1:

        os.makedirs(save_root_mkdir, exist_ok=True)
        p_results[0].save(f'{save_root_mkdir}/{key_names[-1]}')

        object_classification_str = ''
        if temp_classes['person'] >= 1:
            object_classification_str += '보행자, '
        if temp_classes['motorcycle'] >= 1:
            object_classification_str += '오토바이, '
        if temp_classes['bicycle'] >= 1:
            object_classification_str += '자전거, '

        object_classification_str = object_classification_str[:-2]

        # only_a4_list.append(f"{new_filename} => {object_classification_str}")
        with open('step1_only_a4_list.txt', 'a', encoding='utf-8') as g:
            g.write(f"{new_filename} => {object_classification_str}\n")


    print(f'scanning...{cnt}/{len(keyframes_list)}\n')
e2 = cv2.getTickCount()
t_time = (e2-e1)/cv2.getTickFrequency()
print(f'Total_time: {t_time} seconds')

# with open('step1_detection_result_1224.txt', '+w') as f:
#     f.write('\n'.join(detection_results))

# with open('step1_only_a4_list.txt', '+w', encoding='utf-8') as f:
#     f.write('\n'.join(only_a4_list))

f.close()
g.close()