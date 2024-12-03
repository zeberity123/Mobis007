import os
import list_step_1
import cv2

origin_tw_root = f'/run/user/1000/gvfs/smb-share:server=192.168.2.1,share=fc3_nas_007/TW'
txt_file = f'/run/user/1000/gvfs/smb-share:server=192.168.2.1,share=fc3_nas_007/TW/모비스_mcam_v5/auto_test_ubuntu/file_list.txt'
home_root = f'/home/ubuntu/Curation_MOBIS_MCAM'
home_root = f'/run/user/1000/gvfs/smb-share:server=192.168.2.1,share=fc3_nas_007/step_1_241203'

f = open(txt_file, 'r')
tw_folder_list = f.read().split()


# yuuv_file, result_rootd, head_file
tw_list = []

for folder_name in tw_folder_list:
    videos_root = f'{origin_tw_root}/{folder_name}/Front/Video'
    for i in os.listdir(videos_root):
        if i[-9:] == '_30Hz.bin':
            tw_file_roots = []
            tw_file_roots.append(f'{videos_root}/{i}')
            tw_file_roots.append(f'{home_root}/{folder_name}')
            tw_file_roots.append(f'{videos_root}/{i.split('.')[0]}.timestamp')
            tw_list.append(tw_file_roots)

for i in tw_list:
    e1 = cv2.getTickCount()
    list_step_1.auto_step_1(i[0], i[1], i[2])
    e2 = cv2.getTickCount()

    total_time = (e2-e1)/cv2.getTickFrequency()
    print(f'Total time: {total_time}seconds')
