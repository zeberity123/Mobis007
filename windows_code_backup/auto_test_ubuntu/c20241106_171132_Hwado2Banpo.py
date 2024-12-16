import os
import list_step_2
import cv2
from datetime import datetime


def step2():
    result_folder_name = f'20241106_171132_Hwado2Banpo'
    key_frames = '007863	011463	014351	017771	021011	024915	026295	037447	050165	060861	068059	079813	090977	103809	111259	125421	132789	138189	146347	156189	162729	165243	175985	185465	186845	197589	208397	219065	230765	243197	246257	251639	263935	274575	282795	283991	289571	303667	304267	305589	307269	316389	330971	339599	348975	349695	359577	360957	364437	377579	390789	393909	404951	406811	414301	414601	422401	425701	435175	446035	456789	467581	479163	489233	502451	506951	507911	510777	520737	521571	524091	531471	532979	543179	551219	553977	555837	564771	571671	577493	591531	597177	607985	618727	631443'

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