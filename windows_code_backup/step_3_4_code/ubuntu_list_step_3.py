# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import os
import numpy as np


# Channel (index+1)의 horizontal offset
hor_off = [
	3.257, 3.263, 1.091, 3.268, 1.093, 3.273, 1.094, 3.278, 1.095, 3.283, 1.096, 3.288, 1.097, 3.291, 1.098, -1.101,
	1.100, -1.104, -3.306, -1.106, -3.311, -1.109, -3.318, -1.111, -3.324, -1.113, 7.72, 5.535, 3.325, -3.33, 1.107, -5.538,
	-7.726, -1.115, 7.731, 5.543, 3.329, -3.336, 1.108, -5.547, -7.738, -1.117, 7.743, 5.551, 3.335, -3.342, 1.110, -5.555,
	-7.750, -1.119, 7.757, 5.560, 3.340, -3.347, 1.111, -5.564, -7.762, -1.121, 7.768, 5.569, 3.345, -3.353, 1.113, -5.573,
	-7.775, -1.123, 7.780, 5.578, 3.351, -3.358, 1.115, -5.582, -7.787, -1.125, 7.792, 5.586, 3.356, -3.363, 1.116, -5.591,
	-7.799, -1.127, 7.804, 5.595, 3.360, -3.369, 1.118, -5.599, -7.811, -1.129, -3.374, -1.130, -3.379, -1.132, -3.383, 3.381,
	-3.388, 3.386, 1.129, 3.390, 1.129, 3.395, 1.131, 3.401, 1.133, 3.406, 1.135, 3.410, 1.137, 3.416, 1.139, -1.142,
	1.142, -1.143, -3.426, -1.143, -3.429, -1.145, -3.433, -1.145, -3.436, -1.146, -3.440, -1.146, -3.443, -1.146, -3.446, -3.449
]

# Channel (index+1)의 vertical angle
vert_ang = [
	14.436, 13.535, 13.082, 12.624, 12.165, 11.702, 11.239, 10.771, 10.305, 9.830, 9.356, 8.880, 8.401, 7.921, 7.438, 6.953,
	6.467, 5.978, 5.487, 4.996, 4.501, 4.007, 3.509, 3.013, 2.512, 2.013, 1.885, 1.761, 1.637, 1.511, 1.386, 1.258,
	1.13, 1.008, 0.88, 0.756, 0.63, 0.505, 0.379, 0.251, 0.124, 0, -0.129, -0.254, -0.380, -0.506, -0.632, -0.760,
	-0.887, -1.012, -1.141, -1.266, -1.393, -1.519, -1.646, -1.773, -1.901, -2.027, -2.155, -2.282, -2.409, -2.535, -2.663, -2.789,
	-2.916, -3.044, -3.172, -3.299, -3.425, -3.552, -3.680, -3.806, -3.933, -4.062, -4.190, -4.318, -4.444, -4.571, -4.699, -4.824,
	-4.951, -5.081, -5.209, -5.336, -5.463, -5.589, -5.718, -5.843, -5.968, -6.100, -6.607, -7.117, -7.624, -8.134, -8.640, -9.149,
	-9.652, -10.160, -10.665, -11.170, -11.672, -12.174, -12.673, -13.173, -13.67, -14.166, -14.66, -15.154, -15.645, -16.135, -16.622, -17.106,
	-17.592, -18.072, -18.548, -19.030, -19.501, -19.978, -20.445, -20.918, -21.379, -21.848, -22.304, -22.768, -23.219, -23.678, -24.123, -25.016
]

def nanoseconds_to_unix_timestamp(nanoseconds, gmt_offset_hours=9):
    # 나노초를 초로 변환 (10^9 나누기)
    # seconds : 정수 초
    # microseconds : 마이크로 초
    seconds = nanoseconds // 1e9
    microseconds = (nanoseconds % 1e9) // 1e3

    # 1970년 1월 1일 기준 시간 (Unix epoch)
    epoch = datetime(1970, 1, 1)

    # 나노초로부터 현재 시간을 계산
    timestamp_datetime = epoch + timedelta(seconds=seconds)

    # GMT+09:00 오프셋을 적용하여 현지 시간으로 변환
    timestamp_with_offset = timestamp_datetime + timedelta(hours=gmt_offset_hours)

    formatted_time = timestamp_with_offset.strftime("%Y%m%d%H%M%S")

    # 최종적으로 UNIX timestamp (초 단위) 반환
    return f"{formatted_time}.{int(microseconds):06d}"


def get_azimuth_from_data(raw_data):
    get_intval = int.from_bytes(raw_data, byteorder='little')
    return_val = get_intval / 100

    return return_val


# def cur_block_xyzrs(block, azimuth):
#     points = []
#     for i in range(0, len(block), 3):
#         # 4mm 이므로 m단위 변환을 위해 최종적으로 1000 나눠줘야한다.
#         distance = int.from_bytes(block[i:i+2], byteorder='little') * 4

#         # 0 ~ 255 사이의 값이라고 하는데, distance가 0(not valid value인 경우 0이던)
#         reflectivity = int.from_bytes(block[i+2:i+3], byteorder='little')
#         channel = i // 3

#         vertical_angle = vert_ang[channel]
#         horiz_offset = hor_off[channel]
#         adjusted_azimuth = azimuth + horiz_offset
#         x = distance * np.cos(np.radians(vertical_angle)) * np.sin(np.radians(adjusted_azimuth))
#         y = distance * np.cos(np.radians(vertical_angle)) * np.cos(np.radians(adjusted_azimuth))
#         z = distance * np.sin(np.radians(vertical_angle))

#         points.append((x / 1000, y / 1000, z / 1000, reflectivity))

#     return points


def cur_block_xyzrs(block, azimuth):
    points = []
    for i in range(0, len(block), 3):
        # 4mm 이므로 m단위 변환을 위해 최종적으로 1000 나눠줘야한다.
        distance = int.from_bytes(block[i:i+2], byteorder='little') * 4

        # 0 ~ 255 사이의 값이라고 하는데, distance가 0(not valid value인 경우 0이던)
        reflectivity = int.from_bytes(block[i+2:i+3], byteorder='little')
        channel = i // 3

        vertical_angle = vert_ang[channel]
        horiz_offset = hor_off[channel]
        adjusted_azimuth = azimuth + horiz_offset

        # 방위각 필터링 (0 ~ 180도 사이만 저장)
        if 90 <= adjusted_azimuth <= 270:
            x = distance * np.cos(np.radians(vertical_angle)) * np.sin(np.radians(adjusted_azimuth))
            y = distance * np.cos(np.radians(vertical_angle)) * np.cos(np.radians(adjusted_azimuth))
            z = distance * np.sin(np.radians(vertical_angle))

            points.append((x / 1000, y / 1000, z / 1000, reflectivity))

    return points


def save_pcd(points, save_dir, keyframe_no):
    # 저장할 PCD 파일의 header 부분
    header = f"""# .PCD v0.7 - Point Cloud Data file format
VERSION 0.7
FIELDS x y z intensity
SIZE 4 4 4 4
TYPE F F F F
COUNT 1 1 1 1
WIDTH {len(points)}
HEIGHT 1
VIEWPOINT 0 0 0 1 0 0 0
POINTS {len(points)}
DATA ascii
"""

    pcd_path = os.path.join(save_dir, f"{str(keyframe_no).zfill(6)}.pcd")

    with open(pcd_path, 'w') as f:
        f.write(header)

        for each_p in points:
            f.write(f"{each_p[0]:.6f} {each_p[1]:.6f} {each_p[2]:.6f} {each_p[3]}\n")

    print(f"{pcd_path} 저장이 완료되었습니다.")


def check_headfile_filename(head_dir):
    head_file = head_dir
    # filename test:
    if os.path.exists(head_file):
        return 'head_exists'
    else:
        # return False
        num_headfile = head_file[-16:]
        original_headnum = int(num_headfile.split('.')[0]) - 1
        str_original_headnum = str(original_headnum).zfill(6)
        str_new_headnum = str(original_headnum+1).zfill(6)
        original_headfile = f'{head_file[:-16]}{str_original_headnum}.timestamp'
        original_bin_file = f'{head_file[:-16]}{str_original_headnum}.bin'
        new_bin_file = f'{head_file[:-16]}{str_new_headnum}.bin'
        print('errrorrrrr', num_headfile)
        if os.path.isfile(original_headfile) and os.path.isfile(original_bin_file):
            # print(f'changing {original_headfile} to {head_file}')
            print(f'***Using{original_headfile} instead of {head_file}')
            # os.rename(original_headfile, head_file)
            # os.rename(original_bin_file, new_bin_file)
            return [original_headfile, original_bin_file]
        else:
            return 'no_header'
    # try:
    #     with open(head_file, "r") as file:
    #         return 0
    # except:
    #     num_headfile = head_file[-16:]
    #     original_headnum = int(num_headfile.split('.')[0]) - 1
    #     str_original_headnum = str(original_headnum).zfill(6)
    #     str_new_headnum = str(original_headnum+1).zfill(6)
    #     original_headfile = f'{head_file[:-16]}{str_original_headnum}.timestamp'
    #     original_bin_file = f'{head_file[:-16]}{str_original_headnum}.bin'
    #     new_bin_file = f'{head_file[:-16]}{str_new_headnum}.bin'
    #     print('errrorrrrr', num_headfile)
    #     if os.path.isfile(original_headfile) and os.path.isfile(original_bin_file):
    #         print(f'changing {original_headfile} to {head_file}')
    #         # os.rename(original_headfile, head_file)
    #         # os.rename(original_bin_file, new_bin_file)
    #         return f'{head_file}'
    #     return f'{head_file}'

def auto_step_3(result_dir_from_1, lidar_dir, head_dir, key_frame_num):
    # Step1 작업이 수행된 폴더 중 1개를 지정
    # result_rootd = fr'C:\Users\user\Desktop\FC3_NAS_007_Curation\20241008_130405'
    # lidar_file = fr'20241008_124305_Yangpyeong2Chungpyeong\Front\LiDAR\FRCMR_Lidar1_20241008_130405.bin'
    # head_file = fr'20241008_124305_Yangpyeong2Chungpyeong\Front\LiDAR\FRCMR_Lidar1_20241008_130405.timestamp'
    # key_frame_no = 81943

    result_rootd = result_dir_from_1
    lidar_file = lidar_dir
    head_file = head_dir
    key_frame_no = key_frame_num


    # Step1.이 수행된 폴더에 있는(또는 해당 결과물의) timestamp.txt 경로
    img_timestamp_txt = open(os.path.join(result_rootd, 'timestamp_info.txt'), 'r')
    img_timestamp_lines = img_timestamp_txt.readlines()
    img_timestamp_txt.close()

    # selection된 key frame 번호 지정
    

    # img_keyf_list : image의 keyframe에 대한 list
    # img_times_list : image의 keyframe에 대응하는 timestamp에 대한 list
    img_keyf_list = list()
    img_times_list = list()

    for idx in range(10):
        # 60 frame 기준으로 앞 4장, 뒷 5장
        img_keyf_list.append(key_frame_no + (idx - 4) * 60)


    # 대상 keyframe 이미지들의 timestamp를 list 형태로 저장
    for each_l in img_timestamp_lines:
        # keyframe_no, context_num, timestamp
        cur_keyf, cur_cnum, cur_tstamp = each_l.strip().split(', ')

        if int(cur_keyf) in img_keyf_list:
            img_times_list.append(float(cur_tstamp))

    # print(img_times_list)

    result_parentd = os.path.dirname(result_rootd)
    target_timeline = os.path.basename(result_rootd)

    # 슬라이드 p20을 확인하면 1st Folder 이름을
    # yyyymmdd_hhmmss_yyyymmdd_hhmmss_keyframe  으로 지정하게 되어있다.
    result_saved_dir = os.path.join(result_parentd, f'{target_timeline}_{target_timeline}_{str(key_frame_no)}')
    os.makedirs(result_saved_dir, exist_ok=True)

    pcd_dir = os.path.join(result_saved_dir, 'pcd')
    os.makedirs(pcd_dir, exist_ok=True)

    # Step1. 수행 결과 result_rootd에 대응하는 lidar 데이터 경로를 입력
    
    lidar_time_idx_list = list()

    # image timestamp 기준으로, 가장 가까운 timestamp 찾는다.
    # 전/후 기준으로, 대상 timestamp 바로 다음번 lidar timestamp 기준으로 -899 ~ 0(가장 가까운 lidar timestamp) ~ 900 = 1800
    
    with open(head_file, "r") as file:
        index = 0
        img_times_idx = 0
        for line in file:
            cur_target_time = img_times_list[img_times_idx]
            timestamp_sec = float(line.strip()) # 각 라인의 앞뒤 공백 제거
            # print(timestamp_sec)
            

            cur_timestamp = int(timestamp_sec * 1_000_000_000)#int.from_bytes(data[:8], byteorder='little')
            unix_timestamp = nanoseconds_to_unix_timestamp(cur_timestamp)

            if float(unix_timestamp) > cur_target_time:
                lidar_time_idx_list.append(index)
                img_times_idx += 1

            if img_times_idx >= len(img_times_list):
                break

            index += 1

    # print(lidar_time_idx_list)

    # 찾은 timestamp 
    with open(lidar_file, 'rb') as hf:
        index = 0
        lidar_time_idx_list_no = 0
        point_idx = 0
        points = []

        while True:
            # lidar 패킷 정보를 받아옴
            data = hf.read(865)
    
            if not data:
                break

            if (index >= (lidar_time_idx_list[lidar_time_idx_list_no] - 900)) and (index < (lidar_time_idx_list[lidar_time_idx_list_no] + 900)):
                raw_pcd_data = data[16:]

                pcd_body = raw_pcd_data
                block1_azimuth = get_azimuth_from_data(pcd_body[0:2])
                block1 = pcd_body[2:386]

                points.extend(cur_block_xyzrs(block1, block1_azimuth))
                block2_azimuth = get_azimuth_from_data(pcd_body[386:388])
                block2 = pcd_body[388:772]

                points.extend(cur_block_xyzrs(block2, block2_azimuth))

                point_idx += 1


            elif index == (lidar_time_idx_list[lidar_time_idx_list_no] + 900):

                save_pcd(points=points, save_dir=pcd_dir, keyframe_no=img_keyf_list[lidar_time_idx_list_no])

                lidar_time_idx_list_no += 1

                points = []

                point_idx = 0


            if lidar_time_idx_list_no >= len(lidar_time_idx_list):
                break

            index += 1