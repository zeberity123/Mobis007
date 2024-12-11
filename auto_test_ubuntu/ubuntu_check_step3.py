import os
import ubuntu_list_step_3
import set_step_4
import cv2

# 상위폴더 이름
origin_tw_root = f'/run/user/1000/gvfs/smb-share:server=192.168.2.1,share=fc3_nas_007/TW'
step_1_dir = f'/run/user/1000/gvfs/smb-share:server=192.168.2.1,share=fc3_nas_007/step_1_241203'
step_1_folders = os.listdir(step_1_dir)
files_for_step_3 = []
pcd_already_done = []
# search only input folders:
# step_1_folders = ['20241114_104214_Chungdam2songpa']


def check_step_2(folder_dir):
    len_img = len(os.listdir(f'{folder_dir}/img'))
    len_raw = len(os.listdir(f'{folder_dir}/raw'))
    len_yuv = len(os.listdir(f'{folder_dir}/yuv'))
    # print(f'checking cs2_{folder_dir}')
    # print(f'img:{len_img},raw:{len_raw},yuv:{len_yuv}')

    if len_img == 10 and len_raw == 10 and len_yuv == 10:
        return True
    else:
        return False
    

for folder_name in step_1_folders:
    temp_folder_list = os.listdir(f'{step_1_dir}/{folder_name}')
    for i in temp_folder_list:
        i_split = i.split('_')
        if len(i_split) == 5:
            i_folder_list = os.listdir(f'{step_1_dir}/{folder_name}/{i}')
            # if 'pcd' not in i_folder_list:
            if ('8879_ldr2cam_calib.json' not in i_folder_list) and ('pcd' not in i_folder_list) and check_step_2(f'{step_1_dir}/{folder_name}/{i}'):
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
diff_headfile_names = []
print(f'files to process: {len(files_for_step_3)}')
for i in files_for_step_3:
    cnt+=1
    e1 = cv2.getTickCount()
    diff_headfile_name = ubuntu_list_step_3.check_headfile_filename(i[2])
    if diff_headfile_name != 0:
        diff_headfile_names.append(diff_headfile_name)
        
    else:
        ubuntu_list_step_3.auto_step_3(i[0], i[1], i[2], int(i[3]))
        set_step_4.auto_step_4(i[4])
        done.append(f'done: {i[0]}::{i[3]}')
    # set_step_4.delete_json(i[4])
    e2 = cv2.getTickCount()
    
    total_time = (e2-e1)/cv2.getTickFrequency()
    print(f'Total time: {total_time}seconds.....{cnt}/{len(files_for_step_3)}')


# for i in pcd_already_done:
#     print(i)

done_txt = 'step_3_4_1212_01.txt'
with open(done_txt, 'w+') as f:
    f.write('\n'.join(done))

diff_headfile_txt = 'diff_head_1212_01.txt'
with open(diff_headfile_txt, 'w+') as f:
    f.write('\n'.join(diff_headfile_names))

# for i in done:
#     print(i)

# print(diff_headfile_names)
# for i in diff_headfile_names:
#     print(i)

print(f'n_of_done: {len(done)}')
print(f'n_of_pcd_already_done: {len(pcd_already_done)}')