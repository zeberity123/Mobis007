import os
import list_step_3
import set_step_4
import cv2

# 상위폴더 이름
origin_tw_root = f'/run/user/1000/gvfs/smb-share:server=192.168.2.1,share=fc3_nas_007/TW'
step_1_dir = f'/run/user/1000/gvfs/smb-share:server=192.168.2.1,share=fc3_nas_007/step_1_241203'
step_1_folders = os.listdir(step_1_dir)
files_for_step_3 = []
pcd_already_done = []
for folder_name in step_1_folders:
    temp_folder_list = os.listdir(f'{step_1_dir}/{folder_name}')
    for i in temp_folder_list:
        i_split = i.split('_')
        if len(i_split) == 5:
            i_folder_list = os.listdir(f'{step_1_dir}/{folder_name}/{i}')
            # if 'pcd' not in i_folder_list:
            if ('8879_ldr2cam_calib.json' not in i_folder_list) and ('pcd' not in i_folder_list):
                key_frame = i_split[-1]
                fname_no_frame = f'{i_split[0]}_{i_split[1]}'
                lidar_fname = f'{i_split[2]}_{i_split[3]}.bin'
                head_fname = f'{i_split[2]}_{i_split[3]}.timestamp'

                result_dir_from_1 = f'{step_1_dir}/{folder_name}/{fname_no_frame}'
                lh_base_dir = f'{origin_tw_root}/{folder_name}/Front/LiDAR/FRCMR_Lidar1_'
                lidar_dir = f'{lh_base_dir}{lidar_fname}'
                head_dir = f'{lh_base_dir}{head_fname}'
                step_4_dir = f'{step_1_dir}/{folder_name}/{i}'
                # print(result_dir_from_1)
                # print(lidar_dir)
                # print(head_dir)
                # print(key_frame)
                files_for_step_3.append([result_dir_from_1, lidar_dir, head_dir, key_frame, step_4_dir])

            else:
                pcd_already_done.append(f'pcd already exists: {i}')


cnt = 0
done = []
print(f'files to process: {len(files_for_step_3)}')
for i in files_for_step_3:
    cnt+=1
    e1 = cv2.getTickCount()
    # list_step_3.auto_step_3(i[0], i[1], i[2], int(i[3]))
    # set_step_4.auto_step_4(i[4])
    # set_step_4.delete_json(i[4])
    e2 = cv2.getTickCount()
    done.append(f'done: {i[0]}::{i[3]}')
    total_time = (e2-e1)/cv2.getTickFrequency()
    print(f'Total time: {total_time}seconds.....{cnt}/{len(files_for_step_3)}')


for i in pcd_already_done:
    print(i)

done_txt = 'step_3_4_1209_1001.txt'
with open(done_txt, 'w+') as f:
    f.write('\n'.join(done))
for i in done:
    print(i)

print(len(done))
print(len(pcd_already_done))