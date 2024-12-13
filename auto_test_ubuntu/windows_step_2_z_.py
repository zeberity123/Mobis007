import os
import list_step_2
import cv2
from datetime import datetime

# 상위폴더 이름 ex: f'20241004_174606_Mabook2Banpo'
result_folder_name = f'20241101_170050_Mabook2Youido'
# 키프레임 ex: '042693, 042753, 042813'
key_frames = '221723	230003	232943	237443	239785	242125	243565	250045	252445	254305	260427	261807	272295	284365	285805	287905	290605	294615	296175	297795	308357	312377	317357	319277	320957	323177	325817	328457	331937	333797	340339	343279	345319	348331	349771	351151	356131	364821	396931	398611	401291	406871	409031	411869	414569	421049	423671	426191	427331	434305	435685	441985	447079	448459	458185	460885	466287	480669	485169	487815	489615	492435	498671	502091	507491	517705	520337	521657	536723	538643	539843	543793	545293	552923	554903	576865	584711	586631	591851	596291	598571	306071	609677	611657	613577	615437	620165	622265	624305	626285	627965	631325'
key_frames = '221723'
key_frames = [i.strip() for i in key_frames.split('\t')]
# key_frames = '097789, 100189, 101449, 104929'
# key_frames = [i for i in key_frames.split(', ')]

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
        error_list.append([i[0].split('step_1_241203/')[1], i[3]])
    e2 = cv2.getTickCount()

    total_time = (e2-e1)/cv2.getTickFrequency()
    print(f'Total time: {total_time}seconds.....{cnt}/{len(files_for_step_2)}')


time_now = datetime.now()
file_prefix = f'{time_now.strftime('%m%d%H%M')}'

error_txt = f'{file_prefix}_error_step2.txt'
with open(error_txt, 'w+') as f:
    f.write('\n'.join(error_list))