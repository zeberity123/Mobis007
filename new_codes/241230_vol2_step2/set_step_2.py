import os
import list_step_2
import cv2
from datetime import datetime

# 상위폴더 이름 ex: f'20241004_174606_Mabook2Banpo'
result_folder_name = f'20241108_163646_Mabook2Mapo'
# 키프레임 ex: '042693, 042753, 042813'
key_frames = '25545	26805	30943	34123	39395	42755	53565	55605	59325	61603	63463	76773	78993	80673	84523	90943	93755	95135	96515	104425	106525	113245	116487	118527	121767	123207	127647	132747	136411	138691	144571	148001	155681	162281	171569	182189	184229	192865	194125	203785	205945	212961	215001	219981	224363	230663	232163	239963	242603	244345	246565	251185	256165	264505	265833	271413	272673	283941	289597	291697	307773	315633	322761	327261	328761	330923	332303	344539	355109	356369	358889	361169	363453	365613	367473	378633	379893	383313	392121	401429	410425	411685	417269	422849	424409	431493	439877	441257	442937	451409	453749	455129	464181	465861	469161	471015	474915	479235	480555	481829	483089	485789	487649	495017	497117	498377	501977	503963	506063	508163	509903	517045	519385	521545	529095	533355	540613	542053	550705	558373	560233	562453	563773'

key_frames = [i.strip() for i in key_frames.split('\t')]

print(key_frames)
origin_tw_root = f'R:/TW'                                      
home_root = f'R:/step_1_241203'

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