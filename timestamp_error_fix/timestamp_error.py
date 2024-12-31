# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import os
import numpy as np
import cv2
import time
import random
# head 파일에서 읽어들인 timestamp 값을 unix timestamp 포맷으로 출력해주는 값.
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


def extract_info_from_yplane(raw_data):
    str_F = raw_data[1:2].decode()  # 'F'
    str_R = raw_data[3:4].decode()  # 'R'
    str_C = raw_data[5:6].decode()  # 'C'
    str_M = raw_data[7:8].decode()  # 'M'
    str_2nd_R = raw_data[9:10].decode()  # 'R'

    vid_str = str_F + str_R + str_C + str_M + str_2nd_R

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

    Context = raw_data[35]


    return vid_str, int(frame_id), int(Context)


def yuv422_to_rgb(raw_data):
    # YUV Frame Total Size(in Bytes) : 64 + 1920*1080*2 = 4,147,264 Bytes
    #r_raw_data = raw_data[64:]
    width = 1920
    height = 1080

    yuv_frame = np.frombuffer(raw_data, dtype=np.uint8)
    
    # 현재 모비스 데이터를 확인해보니 yuv422 포맷 중, UYVY 포맷이었다.
    y = yuv_frame[1::2].reshape((height, width))  # 모든 홀수 인덱스는 Y 값
    u = yuv_frame[0::4].reshape((height, width // 2))  # U 값 (U는 4개당 1개)
    v = yuv_frame[2::4].reshape((height, width // 2))  # V 값 (V는 4개당 1개)

    # u와 v가 높이가 절반이므로 업샘플링을 수행한다.
    u = u.repeat(2, axis=1)
    v = v.repeat(2, axis=1)

    # u, v에는 -128을 적용한다.
    u = u.astype(np.int16) - 128
    v = v.astype(np.int16) - 128
    y = y.astype(np.int16)

    # YUV to RGB
    # b = (4096 * y) + (7600 * u) + (2 * v)) / 4096
    # g = (4096 * y) + (-767 * u) + (-1918 * v)) / 4096
    # r = (4096 * y) + (-3 * u) + (6449 * v)) / 4096
    b = (y + (1.85546875 * u) + (0.00048828125 * v)).astype(np.int16)
    g = (y - (0.187255859375 * u) - (0.46826171875 * v)).astype(np.int16)
    r = (y - (0.000732421875 * u) + (1.574462890625 * v)).astype(np.int16)

    # # 값 범위를 0-255로 클램핑하고 uint8 형식으로 변환
    r = np.clip(r, 0, 255).astype(np.uint8)
    g = np.clip(g, 0, 255).astype(np.uint8)
    b = np.clip(b, 0, 255).astype(np.uint8)

    # RGB 채널을 합쳐서 이미지 생성
    # opencv는 BGR 방식을 활용하기 떄문에 BGR 순서로 배포
    rgb_image = np.stack([b, g, r], axis=-1)

    return rgb_image


if __name__ == '__main__':
    # yuuv 파일(.bin) 지정
    yuuv_file = fr'../Video/FRCMR_IMG_FR_UYVY_20241031_200110_1920_1080_30Hz.bin'
    dummy_nums = [0,1,2,3,4,5,6,7,8,9]
    dummy_num = random.choice(dummy_nums)
    
    # png 파일을 보관할 최상위 폴더경로 지정
    result_rootd = fr'mobis_yuuv_sample'
    os.makedirs(result_rootd, exist_ok=True)

    fname_list = list()
    # dummy number 1초당 하나씩 샘플링 하기 위한 변수
    dummy_num1 = random.choice([0,2,4,6,8])
    dummy_num2 = random.choice([1,3,5,7,9])
    # # 대상 YUV 폴더 내 파일 이름을 확인하기 위한 loop
    # for eachf in os.listdir(yuuv_dir):
    #     fname, ext = os.path.splitext(eachf)
    #
    #     if ext.lower() == '.bin':
    #         fname_list.append(fname)

    # for each_fname in fname_list:
    # 파일 이름의 구조가 FRCMR_IMG_FR_UYVY_{yyyymmdd}_{HHMMDD}_1920_1080_60Hz 로 저장되는 걸 가정하고 진행한다.
    each_fname, ext = os.path.splitext(os.path.basename(yuuv_file))
    fname_split = each_fname.split('_')
    date_info = fname_split[4]
    time_info = fname_split[5]

    save_img_rootd = os.path.join(result_rootd, f'{date_info}_{time_info}')
    normal_img_dir = os.path.join(save_img_rootd, 'Img_full')
    #dark_img_dir = os.path.join(save_img_rootd, 'Dark_img_full')
    os.makedirs(save_img_rootd, exist_ok=True)
    #os.makedirs(normal_img_dir, exist_ok=True)
    #os.makedirs(dark_img_dir, exist_ok=True)

    head_file = '../Video/FRCMR_IMG_FR_UYVY_20241031_200110_1920_1080_30Hz.timestamp'#os.path.join(os.path.dirname(yuuv_file), f'{each_fname}.head')
    yuv_bin_file = os.path.join(os.path.dirname(yuuv_file), f'{each_fname}.bin')

    img_timestamp = []

    # ================================================================================================================
    # Phase1. head 파일로부터 YUV422 timestamp 확인하는 코드
    # ================================================================================================================
    # yuuv 폴더 내 json 파일을 확인해보면, indexing을 확인할 수 있다.
    # 이미지 index는 0 ~ 10,799 프레임이며 1초에 60프레임, 총 3분(180초)의 데이터가 저장되어있음.
    # json 파일에서는 index와 frame_num 이란 key 값을 확인했다.
    # ================================================================================================================
    with open(head_file, "r") as file:
        for line in file:
            timestamp_sec = float(line.strip()) # 각 라인의 앞뒤 공백 제거

            cur_timestamp = int(timestamp_sec * 1_000_000_000)#int.from_bytes(data[:8], byteorder='little')
            unix_timestamp = nanoseconds_to_unix_timestamp(cur_timestamp)

            img_timestamp.append(unix_timestamp)

    # ================================================================================================================
    # Phase2. bin 파일로부터 png 파일을 추출하는 코드
    # ================================================================================================================

    with open(yuv_bin_file, 'rb') as raw_video_f:
        index = 0
        
        while True:
            # YUV422 형식은 Y, U, V 화소가 분리된 형식이라고 한다.
            # field size = Y_plane(1920*1080) + U_plane(1920*540) + V_plane(1920*540) = 4147200이 나온다고 한다.
            raw_video_data = raw_video_f.read(4147264)#raw_video_f.read(4147200)
            
            if not raw_video_data:
                    break
            
            # frameid, context, timestamp를 저장하는 txt 파일 생성
            yuuv_info_txt = os.path.join(save_img_rootd, 'timestamp_info.txt')
            txtf = open(yuuv_info_txt, 'a', encoding='utf-8')
            video_string, cur_frameid, cur_context = extract_info_from_yplane(raw_video_data[64:])

            txtf.write(f'{str(cur_frameid)}, {str(cur_context)}, {img_timestamp[index]}\n')
            txtf.close()

            yuv_to_rgb_imgdata = yuv422_to_rgb(raw_video_data[64:])


            if cur_context == 1:
                img_path = os.path.join(normal_img_dir, str(cur_frameid).zfill(6) + '.png')

            try:
                #cv2.imwrite(img_path, yuv_to_rgb_imgdata)
                print(f"이미지가 {img_path}에 저장되었습니다.")

            except Exception:
                print(f'{str(cur_frameid).zfill(6)} 프레임 이미지 저장 시 오류가 발생합니다. keyframe 선정 시 포함되지 않도록 주의해주세요.')
            #print(index)
            index += 1
