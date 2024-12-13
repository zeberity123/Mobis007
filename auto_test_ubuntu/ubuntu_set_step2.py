import os
import list_step_2
import cv2

# 상위폴더 이름
result_folder_name = f'20241109_130313_Songpa2Namisum'
# 키프레임
# key_frames = '042693, 042753, 042813'

# key_frames = '042693'
key_frames = '005709'
key_frames = [i.strip() for i in key_frames.split('\t')]
print(key_frames)
origin_tw_root = f'/run/user/1000/gvfs/smb-share:server=192.168.2.1,share=fc3_nas_007/TW'
home_root = f'/run/user/1000/gvfs/smb-share:server=192.168.2.1,share=fc3_nas_007/step_1_241203'

result_folder_dir = f'{home_root}/{result_folder_name}'

result_folder_vids = [f'{result_folder_dir}/{i}' for i in os.listdir(result_folder_dir) if len(i.split('_')) == 2]

files_for_step_2 = []
for folders in result_folder_vids:
    folder_temp_dirs = f'{folders}/Img_full'
    for img_files in os.listdir(folder_temp_dirs):
        img_num = img_files.split('.')[0]
        for key_num in key_frames:
            if int(img_num) == int(key_num):
                # print(folders)
                only_folder_name = folders.split('/')[-2]
                original_vid_root = f'{origin_tw_root}/{only_folder_name}/Front/Video'
                # print(original_vid_root)
                files_for_step_2.append([folders, original_vid_root, original_vid_root, key_num])
                

cnt = 0
for i in files_for_step_2:
    cnt+=1
    e1 = cv2.getTickCount()
    for j in i:
        print(j)
    # print([0], i[1], i[2], i[3])
    list_step_2.auto_step_2(i[0], i[1], i[2], i[3])
    e2 = cv2.getTickCount()

    total_time = (e2-e1)/cv2.getTickFrequency()
    print(f'Total time: {total_time}seconds.....{cnt}/{len(files_for_step_2)}')
