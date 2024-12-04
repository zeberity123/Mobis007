import os
import list_step_2
import cv2

origin_tw_root = f'/run/user/1000/gvfs/smb-share:server=192.168.2.1,share=fc3_nas_007/TW'
txt_file = f'/run/user/1000/gvfs/smb-share:server=192.168.2.1,share=fc3_nas_007/TW/모비스_mcam_v5/auto_test_ubuntu/file_list.txt'
# home_root = f'/home/ubuntu/Curation_MOBIS_MCAM'
home_root = f'/run/user/1000/gvfs/smb-share:server=192.168.2.1,share=fc3_nas_007/step_1_241203'

f = open(txt_file, 'r')
tw_folder_list = f.read().split()

for i in tw_folder_list:
    print(i)