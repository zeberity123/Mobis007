import os
import list_step_1
import cv2

vol_2 = f'Y:/MOBIS_MCAM1.0_11'

origin_tw_root = vol_2

home_root = f'Y:/MOBIS_MCAM1.0_11/step1_250120'

tw_folder_list = []
for i in os.listdir(origin_tw_root):
    # if len(i.split('_')) == 3 and i != '20241119_145440_Yangsuri2Mabook':
    if len(i.split('_')) == 2:
        tw_folder_list.append(i)

print(tw_folder_list)
print(len(tw_folder_list))

# yuuv_file, result_rootd, head_file
tw_list = []

for folder_name in tw_folder_list:
    videos_root = f'{origin_tw_root}/{folder_name}/Front/Video'
    try:
        for i in os.listdir(videos_root):
            if i[-9:] == '_30Hz.bin':
                tw_file_roots = []
                tw_file_roots.append(f'{videos_root}/{i}')
                tw_file_roots.append(f'{home_root}/{folder_name}')
                tw_file_roots.append(f'{videos_root}/{i.split(".")[0]}.timestamp')
                tw_list.append(tw_file_roots)
    except:
        print(f'error: {videos_root}')

cnt = 0
for i in tw_list:
    cnt+=1
    e1 = cv2.getTickCount()
    list_step_1.auto_step_1(i[0], i[1], i[2])
    print(i)
    e2 = cv2.getTickCount()
    # print(i[0])
    # print(i[1])
    # print(i[2])
    total_time = (e2-e1)/cv2.getTickFrequency()
    print(f'Total time: {total_time}seconds.....{cnt}/{len(tw_list)}')
