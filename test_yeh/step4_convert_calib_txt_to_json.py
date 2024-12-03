# -*- coding: utf-8 -*-
import json
from ast import literal_eval

if __name__ == '__main__':
    # camera_calibration.txt 경로를 입력
    cam_calib_txt = r'8879_ldr2cam_calib.txt'

    # lidar_camera_calibaration.txt 경로를 입력
    lidar_to_cam_calib_txt = r'extrinsic_calib_ECO_result_NX4_8879_ECO_fisheye_trans_EOL143eco_updated.txt'

    with open(cam_calib_txt, 'r') as camf:
        cam_calib_data = camf.readlines()

    with open(lidar_to_cam_calib_txt, 'r') as lidar_2_camf:
        lidar2cam_calib_data = lidar_2_camf.readlines()

    cam_calib_str = ''
    lidar2cam_calib_str = ''

    for each_c in cam_calib_data:
        cam_calib_str += each_c

    for each_l in lidar2cam_calib_data:
        lidar2cam_calib_str += each_l


    # json object 형태 변환 시, literal_eval 함수를 사용한다고 한다.
    # 참고 블로그 : https://blog.metafor.kr/224
    cam_calib_dict = literal_eval(cam_calib_str)
    lidar2cam_calib_dict = literal_eval(lidar2cam_calib_str)

    # print(cam_calib_dict)
    # print(lidar2cam_calib_dict)

    # calib.txt 파일이 있는 경로에, 동일한 이름의 json으로 저장해준다.
    with open(cam_calib_txt.replace('.txt', '.json'), 'w') as cam_jf:
        json.dump(cam_calib_dict, cam_jf, indent=2)

    with open(lidar_to_cam_calib_txt.replace('.txt', '.json'), 'w') as lidar2cam_jf:
        json.dump(lidar2cam_calib_dict, lidar2cam_jf, indent=2)