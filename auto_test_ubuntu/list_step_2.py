# -*- coding: utf-8 -*-
import os
import shutil
import numpy as np



def convert_12bit_to_16bit_1(packed_data, width, height):
    # 데이터 크기 확인
    num_pixels = width * height
    expected_size = num_pixels * 12 // 8
    if len(packed_data) != expected_size:
        raise ValueError(f"데이터 크기가 일치하지 않습니다. 예상: {expected_size} 바이트, 실제: {len(packed_data)} 바이트")
    
    # 12비트 데이터를 16비트로 변환
    unpacked_data = np.zeros(num_pixels, dtype=np.uint16)
    for i in range(0, len(packed_data), 3):
        # 3바이트에서 2개의 12비트 값을 추출
        b1, b2, b3 = packed_data[i:i+3]
        # 첫 번째 12비트 값
        first_pixel = ((b1 << 4) | (b2 >> 4)) & 0xFFF
        # 두 번째 12비트 값
        second_pixel = ((b2 << 8) | b3) & 0xFFF
        
        # 16비트 확장 (하위 12비트를 유지하고 상위 4비트는 0으로)
        unpacked_data[i // 3 * 2] = first_pixel  # 첫 번째 픽셀 (하위 12비트만 유지)
        unpacked_data[i // 3 * 2 + 1] = second_pixel  # 두 번째 픽셀 (하위 12비트만 유지)

    return bytearray(unpacked_data.tobytes())

def convert_12bit_to_16bit_2(packed_data, width, height):
    # 데이터 크기 확인
    num_pixels = width * height
    expected_size = num_pixels * 12 // 8
    if len(packed_data) != expected_size:
        raise ValueError(f"데이터 크기가 일치하지 않습니다. 예상: {expected_size} 바이트, 실제: {len(packed_data)} 바이트")
    
    # NumPy 배열로 변환
    packed_array = np.frombuffer(packed_data, dtype=np.uint8)

    # 3바이트씩 그룹화
    packed_array = packed_array.reshape(-1, 3)

    # 첫 번째 12비트 값 계산
    first_pixel = (packed_array[:, 0].astype(np.uint16) << 4) | (packed_array[:, 2].astype(np.uint16) & 0x0F)

    # 두 번째 12비트 값 계산
    second_pixel = (packed_array[:, 1].astype(np.uint16) << 4) | (packed_array[:, 2].astype(np.uint16) & 0xF0) >> 4


    # 16비트 배열 생성
    unpacked_data = np.empty(num_pixels, dtype=np.uint16)
    unpacked_data[0::2] = first_pixel  # 홀수 인덱스
    unpacked_data[1::2] = second_pixel  # 짝수 인덱스

    return bytearray(unpacked_data.tobytes())

def extract_active_image(raw_data: bytes, active_image_rows: int = 1080, active_image_cols: int = 1920, pixel_depth: int = 12) -> bytes:
    # 상수 정의
    frame_header_size = 64            # frame header 크기
    line_header_size = 16             # 각 row의 line header 크기
    row_size = 2880                   # 전체 row의 크기 (line header 포함)
    embedded_data_rows = 3            # embedded data rows 수

    # active image의 시작 위치를 계산
    start_offset = frame_header_size + (row_size * embedded_data_rows)

    # active image 데이터 추출 (row 마다 line header 16 bytes 제거)
    active_image_data = b''.join(
        raw_data[start_offset + i * row_size + line_header_size : start_offset + i * row_size + line_header_size + active_image_cols * pixel_depth // 8]
        for i in range(active_image_rows)
    )

    return active_image_data




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



# emb_line은 이미지 데이터의 메타 정보를 보관하고 있는 데이터 영역이라고 한다.
#Bayer Frame Total Size(in Bytes) = 64 + 1920*1096*1.5 + 16*1096 = 3,174,080 Bytes

emb_line = 6
img_width = 1920
img_height = 1080
bayer_frame_size = int(64 + 1920*1096*1.5 + 16*1096)
yuv_frame_size = int(64 + 1920*1080*2)

def auto_step_2(result_root, yuuv_root, rgb12_root, key_frame_num):
    # Step1 작업이 수행된 폴더 중 1개를 지정
    # result_rootd = fr'/home/ubuntu/Curation_MOBIS_MCAM/20241116_171243_Danyang2Wonju/20241116_175743'
    result_rootd = result_root
    # result_rootd에 해당하는 yuv 원본 binary가 들어있는 폴더 경로 지정
    # yuuv_dir = fr'R:\TW\20241004_173652_m2s\Front\Video'
    # yuuv_dir = fr'/run/user/1000/gvfs/smb-share:server=192.168.2.1,share=fc3_nas_007/TW/20241116_171243_Danyang2Wonju/Front/Video'
    yuuv_dir = yuuv_root
    # result_rootd에 해당하는 raw(bayer) binary가 들어있는 폴더 경로 지정
    # rgb12_dir = fr'R:\TW\20241004_173652_m2s\Front\Video'
    # rgb12_dir = fr'/run/user/1000/gvfs/smb-share:server=192.168.2.1,share=fc3_nas_007/TW/20241116_171243_Danyang2Wonju/Front/Video'
    rgb12_dir = rgb12_root
    # selection된 key frame 번호 지정
    # key_frame_no = 166427
    key_frame_no = int(key_frame_num)
 
    # 추출할 10개의 frame 번호에 대한 list
    frame_no_list = list()

    # Frame_ID가 겹치는지 확인하는 코드
    bayer_yuv_counter = 0
    
    
    for idx in range(10):
        # 60 frame 기준으로 앞 4장, 뒷 5장
        frame_no_list.append(key_frame_no + (idx - 4) * 60)
 

    Img_full_dir = os.path.join(result_rootd, 'Img_full')
    Dark_img_full_dir = os.path.join(result_rootd, 'Dark_img_full')

    target_timeline = os.path.basename(result_rootd)

    # yuv 영상 원본
    target_filename = f'FRCMR_IMG_FR_UYVY_{target_timeline}_1920_1080_30Hz.bin'

    # rggb 영상 원본
    target_bayer_filename = f'FRCMR_IMG_FR_RGGB12_{target_timeline}_1920_1096_60Hz.bin'

    result_parentd = os.path.dirname(result_rootd)


    # modified 241108, 09:08
    # 슬라이드 p20을 확인하면 1st Folder 이름을
    # yyyymmdd_hhmmss_yyyymmdd_hhmmss_keyframe  으로 지정하게 되어있다.
    result_saved_dir = os.path.join(result_parentd, f'{target_timeline}_{target_timeline}_{str(key_frame_no)}')
    os.makedirs(result_saved_dir, exist_ok=True)

    # Img, Dark_img, yuv, raw 폴더 생성
    Img_dir = os.path.join(result_saved_dir, 'img')
    #Dark_img_dir = os.path.join(result_saved_dir, 'Dark_img')
    yuv_dir = os.path.join(result_saved_dir, 'yuv')
    raw_dir = os.path.join(result_saved_dir, 'raw')
    os.makedirs(Img_dir, exist_ok=True)
    #os.makedirs(Dark_img_dir, exist_ok=True)
    os.makedirs(yuv_dir, exist_ok=True)
    os.makedirs(raw_dir, exist_ok=True)
    

    # keyframe 기준으로 yuv.bin 파일은 생성해주고,
    # Img, Dark_img 파일은 복사해주는 과정을 수행한다.
    with open(os.path.join(yuuv_dir, target_filename), 'rb') as raw_video_f:
        index = 0
        while True:
            # YUV422 형식은 Y, U, V 화소가 분리된 형식이라고 한다.
            #※ YUV Frame Total Size(in Bytes) : 64 + 1920*1080*2 = 4,147,264 Bytes
            raw_video_data = raw_video_f.read(yuv_frame_size)

            if not raw_video_data:
                break

            video_string, cur_frameid, cur_context = extract_info_from_yplane(raw_video_data[64:])

            if cur_frameid < frame_no_list[0]:
                continue

            elif cur_frameid > frame_no_list[-1]:
                break


            if cur_frameid in frame_no_list:

                # yuv 파일로부터 bin 파일을 chunk해서 저장하는 코드
                yuv_file = os.path.join(yuv_dir, f'{str(cur_frameid).zfill(6)}.bin')
                with open(yuv_file, 'wb') as yuvf:
                    yuvf.write(raw_video_data[64:])
                    print(yuv_file + ' 파일 저장이 완료되었습니다.')

                # img_full 폴더에서, 대상 png 파일을 복사해준다.
                target_png_path = os.path.join(Img_full_dir, f'{str(cur_frameid).zfill(6)}.png')
                #target_dark_png_path = os.path.join(Dark_img_full_dir, f'{str(cur_frameid + 1).zfill(5)}.png')
                # print('roooto', target_png_path, Img_dir)
                new_Img = target_png_path.split('/')[-1]
                shutil.copyfile(target_png_path, f'{Img_dir}/{new_Img}')
                print(f'{os.path.basename(target_png_path)}가 {Img_dir} 폴더로 복사되었습니다.')

                #shutil.copy2(target_dark_png_path, Dark_img_dir)
                #print(f'{os.path.basename(target_dark_png_path)}가 {Dark_img_dir} 폴더로 복사되었습니다.')



    with open(os.path.join(rgb12_dir, target_bayer_filename), 'rb') as rggbf:
        while True:
            # modified at 241108, 09:12
            #Bayer Frame Total Size(in Bytes) = 64 + 1920*1096*1.5 + 16*1096 = 3,174,080 Bytes
            #※ YUV Frame Total Size(in Bytes) : 64 + 1920*1080*2 = 4,147,264 Bytes
            #YUV 영상에는 Line header와 Embedded 16 rows가 없음
            raw_data = rggbf.read(bayer_frame_size)
            
            if not raw_data:
                break

            
            # 3. emb_data 부분 읽기
            emb_data = raw_data[64+16:] # 예시로, 첫 번째 row의 메타데이터를 포함하는 100 bytes
            
            
            # embed_line 만큼의 메타데이터 영역
           
            emb_fid = (emb_data[76]) | (emb_data[77] << 8) | (emb_data[79] << 16) | (emb_data[80] << 24) | (emb_data[82] << 32) \
                | (emb_data[83] << 40) | (emb_data[85] << 48) | (emb_data[86] << 56)

            if emb_fid < frame_no_list[0]:
                continue
 
            elif emb_fid > frame_no_list[-1]+1:
                break
            
            
            # 4. Active data 부분 읽기
            active_image_rows = 1080          # Acitve image rows
            active_image_cols = 1920         # Active image cols  
            pixel_depth = 12                 # Active image depth
            frame_header_size = 64           # frame header 크기
            line_header_size = 8            # 각 row의 line header 크기
            black_header_size = 8            # 각 row의 line header 크기
            row_size = 2880                  # 전체 row의 크기 (line header 포함)
            embedded_data_rows = 3           # embedded data rows 수

            start_offset = frame_header_size + ((row_size + line_header_size + black_header_size) * embedded_data_rows)  # active image의 시작 위치를 계산
            active_image_data = bytearray(active_image_rows * row_size)  # bytearray 크기 미리 할당

            for i in range(active_image_rows):
                start_index = start_offset + i * (row_size + line_header_size + black_header_size) + line_header_size
                end_index = start_index + row_size
                active_image_data[i * row_size:(i + 1) * row_size] = raw_data[start_index:end_index]  # 행별 데이터 할당

 
            # 12bit to 16bit,
            # 16-bit format, with lower 12 bits valid
            
            #active_image_data_16bit_1 = convert_12bit_to_16bit_1(active_image_data, active_image_cols, active_image_rows)
            active_image_data_16bit = convert_12bit_to_16bit_2(active_image_data, active_image_cols, active_image_rows)
            # # 결과 비교
            # if active_image_data_16bit_1 ==  active_image_data_16bit_2:
            #     print("두 결과가 동일합니다.")
            # else:
            #     print("결과가 다릅니다.")
            #     # 바이트 단위로 차이점 출력
            #     for i, (o, p) in enumerate(zip(active_image_data_16bit_1, active_image_data_16bit_2)):
            #         if o != p:
            #             print(f"위치 {i}: 원본 {o}, 최적화 {p}")
            #             break

            ###################################################################################################################
            
            
            if emb_fid in frame_no_list:
                bayer_yuv_counter += 1
                raw_file = os.path.join(raw_dir, f'{str(emb_fid).zfill(6)}.bin')
                
                with open(raw_file, 'wb') as rawf:
                    rawf.write(active_image_data_16bit)  # 전체 데이터를 한 번에 저장
                    #print(len(active_image_data_16bit))
                    print(f"{raw_file} 파일 저장이 완료되었습니다.")
            
            
            
            # # 4. Active data 부분 읽기
            # active_image_rows = 1080          # Acitve image rows
            # active_image_cols= 1920           # Active image cols  
            # pixel_depth = 12                  # Active image depth
            # frame_header_size = 64            # frame header 크기
            # line_header_size = 16             # 각 row의 line header 크기
            # row_size = 2880                   # 전체 row의 크기 (line header 포함)
            # embedded_data_rows = 3            # embedded data rows 수

            # start_offset = frame_header_size + ((row_size +line_header_size) * embedded_data_rows) # active image의 시작 위치를 계산
            # active_image_data = bytes()  # active image 데이터를 저장할 bytearray

            # for i in range(active_image_rows):
            #     start_index = start_offset + i * (row_size + line_header_size) + line_header_size
            #     end_index = start_index + row_size
            #     active_image_data += raw_data[start_index:end_index] # 행별 데이터 추가
                
            # if emb_fid in frame_no_list:
            #     bayer_yuv_counter +=1
            #     raw_file = os.path.join(raw_dir, f'{str(emb_fid).zfill(5)}.bin')
            
            #     with open(raw_file, 'wb') as rawf:
            #         # modified 241108, at 14:01
            #         # 고객사에서 bayer 영상은 yuv 영상과 동일한 크기로 추출이라고 적혀있어서, frame_size까지만 저장하도록 수정
            #         rawf.write(active_image_data)
            #         print(raw_file + ' 파일 저장이 완료되었습니다.')

            
            # if bayer_yuv_counter < len(frame_no_list):
            #     if frame_no_list[bayer_yuv_counter] < emb_fid:
            #         bayer_yuv_counter +=1
            #         raw_file = os.path.join(raw_dir, f'{str(emb_fid-1).zfill(5)}.bin')
                
            #         with open(raw_file, 'wb') as rawf:
            #             # modified 241108, at 14:01
            #             # 고객사에서 bayer 영상은 yuv 영상과 동일한 크기로 추출이라고 적혀있어서, frame_size까지만 저장하도록 수정
            #             rawf.write(raw_data[64 : ])
            #             print(raw_file + ' 파일 저장이 완료되었습니다.')


# if __name__ == '__main__':

    