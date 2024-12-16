import os
import list_step_2
import cv2
from datetime import datetime


def step2():

    # 상위폴더 이름 ex: f'20241004_174606_Mabook2Banpo'
    result_folder_name = f'20241104_203410_Namyangju2Anyang'
    # 키프레임 ex: '042693, 042753, 042813'
    key_frames = '015877	017397	022797	023937	032753	033773	035153	036833	044283	046983	055137	058437	060291	061491	065811	076613	083213	088533	091013	097133	099833	102233	108409	109309	111829	117291	118791	120291	126243	132063	139201	141241	143281	148619	149819	152879	164623	169785	174225	177285	181129	188749	196855	199315	200459	202079	204899	210659	212337	217377	218397	219777	211109	232787	235487	236387	238607	240047	242207	244319	250259	257563	259063	265543	270703	271423	283131	294111'

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