import os
import list_step_2
import cv2
from datetime import datetime


def step2():
    result_folder_name = f'20241106_111404_Songpa2Chuncheon'
    key_frames = '43467	44727	47607	52291	53551	60631	85033	86533	99319	109463	113483	119129	129855	139277	141437	146897	148753	150553	151813	153613	161243	186739	194667	199227	206601	207321	240791	243131	248657	251537	256465	280931	287291	293957	296417	297437	300373	304933	308713	309733	311063	312983	315623	316943	320603	334165	335065	340525	343219	348619	365949	382219	394641	398541	399861	402741	404481	411679	413959	415639	417139'

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