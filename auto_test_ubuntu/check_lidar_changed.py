import os
import cv2

# 상위폴더 이름
changed_lidar_list = ['20241004_174606_Mabook2Banpo/Front/LiDAR/FRCMR_Lidar1_20241004_180406.timestamp',
                      '20241007_095120_Anyang2Dangjin/Front/LiDAR/FRCMR_Lidar1_20241007_095121.timestamp',
                      '20241008_110805_Kangdonggu2Yangpyeong/Front/LiDAR/FRCMR_Lidar1_20241008_110806.timestamp',
                      '20241008_153547_Gapyung2Songpa/Front/LiDAR/FRCMR_Lidar1_20241008_153548.timestamp',
                      '20241008_153702_Gapyung2Songpa/Front/LiDAR/FRCMR_Lidar1_20241008_153703.timestamp',
                      '20241111_182858_Gwacheon2Kwangmyung/Front/LiDAR/FRCMR_Lidar1_20241111_182859.timestamp',
                      '20241112_083308_Gwangmyung2Anyang/Front/LiDAR/FRCMR_Lidar1_20241112_094208.timestamp',
                      '20241112_102249_Anyang2Ansung/Front/LiDAR/FRCMR_Lidar1_20241112_104349.timestamp',
                      '20241112_102249_Anyang2Ansung/Front/LiDAR/FRCMR_Lidar1_20241112_104949.timestamp',
                      '20241112_102249_Anyang2Ansung/Front/LiDAR/FRCMR_Lidar1_20241112_105249.timestamp',
                      '20241113_160529_Guri2Namisum/Front/LiDAR/FRCMR_Lidar1_20241113_160530.timestamp',
                      '20241116_171243_Danyang2Wonju/Front/LiDAR/FRCMR_Lidar1_20241116_171244.timestamp',
                      '20241116_150014_Chungju2Danyang/Front/LiDAR/FRCMR_Lidar1_20241116_150015.timestamp',
                      '20241113_191104_Namisum2Gwangmyung/Front/LiDAR/FRCMR_Lidar1_20241113_191105.timestamp',
                      '20241116_110423_Osan2Chungju/Front/LiDAR/FRCMR_Lidar1_20241116_110424.timestamp',
                      '20241114_083223_Anyang2Chungdam/Front/LiDAR/FRCMR_Lidar1_20241114_083224.timestamp'
                      ]
origin_tw_root = f'/run/user/1000/gvfs/smb-share:server=192.168.2.1,share=fc3_nas_007/TW'
step_1_dir = f'/run/user/1000/gvfs/smb-share:server=192.168.2.1,share=fc3_nas_007/step_1_241203'

changed_lidar_dirs = []
for i in changed_lidar_list:
    if os.path.isfile(f'{origin_tw_root}/{i}'):
        timestamp_num = i.split('.')[0][-15:]
        changed_lidar_dirs.append([f'{origin_tw_root}/{i}', timestamp_num, f'{origin_tw_root}/{i.split('.')[0]}.{'bin'}'])
        # changed_lidar_dirs.append(f'{origin_tw_root}/{i.split('.')[0]}.{'bin'}')


# for i in changed_lidar_dirs:
#     print(i)

used_changed_lidars = []

step_1_folders = os.listdir(step_1_dir)
for folder_name in step_1_folders:
    temp_folder_list = os.listdir(f'{step_1_dir}/{folder_name}')
    for i in temp_folder_list:
        i_split = i.split('_')
        if len(i_split) == 5:
            for timestamp in changed_lidar_dirs:
                if timestamp[1] in i:
                    # used_changed_lidars.append(f'{step_1_dir}/{folder_name}/{i}')
                    used_changed_lidars.append([f'{timestamp[0]}', f'{step_1_dir}/{folder_name}/{i}', f'{timestamp[2]}'])

for i in used_changed_lidars:
    print(i[0].split('nas_007/TW/')[1])
    
for i in used_changed_lidars:
    print(i[2].split('nas_007/TW/')[1])

for i in used_changed_lidars:
    print(i[1].split('step_1_241203/')[1])