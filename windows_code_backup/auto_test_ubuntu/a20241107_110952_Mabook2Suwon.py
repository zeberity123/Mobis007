import os
import list_step_2
import cv2
from datetime import datetime

def step2():

    # 상위폴더 이름 ex: f'20241004_174606_Mabook2Banpo'
    result_folder_name = f'20241107_110952_Mabook2Suwon'
    # 키프레임 ex: '042693, 042753, 042813'
    key_frames = '10071	11331	21773	25013	31077	34077	41033	47393	50879	53099	62327	70487	77579	80939	87297	88797	90057	95691	96951	99531	100791'

    key_frames = [i.strip() for i in key_frames.split('\t')]

    print(key_frames)
    origin_tw_root = f'Z:/TW'                                      
    home_root = f'Z:/step_1_241203'

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
                    
    error_list = []
    cnt = 0
    for i in files_for_step_2:
        cnt+=1
        e1 = cv2.getTickCount()
        try:
            list_step_2.auto_step_2(i[0], i[1], i[2], i[3])
        except:
            error_list.append(f'{i[0].split('step_1_241203/')[1]} :: {i[3]}')
        e2 = cv2.getTickCount()

        total_time = (e2-e1)/cv2.getTickFrequency()
        print(f'Total time: {total_time}seconds.....{cnt}/{len(files_for_step_2)}')


    time_now = datetime.now()
    file_prefix = f'{time_now.strftime('%m%d%H%M')}'

    error_txt = f'{file_prefix}_error_step2.txt'
    with open(error_txt, 'w+') as f:
        f.write('\n'.join(error_list))