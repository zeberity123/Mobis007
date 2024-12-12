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
# curation_1 = ['20241004_174606_Mabook2Banpo',
#                   '20241007_095120_Anyang2Dangjin',
#                   '20241007_100316_Anyang2Dangjin',
#                   '20241031_164639_Sinwol2Kanghwh_20241031_183546',
#                   '20241031_195810_Kwanghwa2KwangMyung']
curation_1 = ['20241004_174606_Mabook2Banpo',
                  '20241007_095120_Anyang2Dangjin',
                  '20241007_100316_Anyang2Dangjin',
                  '20241031_195810_Kwanghwa2KwangMyung']

curation_2 = ['20241008_110805_Kangdonggu2Yangpyeong',
              '20241008_153547_Gapyung2Songpa',
              '20241008_153702_Gapyung2Songpa',
              '20241010_102551_GwangMyeong2Muuido',
              '20241031_164639_Sinwol2Kanghwh',
              '20241111_182858_Gwacheon2Kwangmyung',
              '20241112_083308_Gwangmyung2Anyang']

curation_3 = ['20241112_102249_Anyang2Ansung',
              '20241113_160529_Guri2Namisum',
              '20241113_211041_Chulsan2Indeogwon',
              '20241116_171243_Danyang2Wonju']

curation_4 = ['20241113_191104_Namisum2Gwangmyung',
              '20241114_083223_Anyang2Chungdam',
              '20241116_110423_Osan2Chungju',
              '20241116_150014_Chungju2Danyang']

curation_5 = ['20241008_153702_Gapyung2Songpa',
              '20241010_102551_GwangMyeong2Muuido',
              '20241010_123336_Muido2Daebudo',
              '20241010_165046_Daebudo2Anyang',
              '20241011_083357_Anyang2Panmunjum',
              '20241011_155941_Songpa2Banpo',
              '20241011_160659_Songpa2Banpo',
              '20241014_101511_Anyang2Pochun',
              '20241030_194046_KwangMyung2Anyang',
              '20241116_124323_Gamgok2Chungju']

step_1_folders = curation_1 + curation_2 + curation_3 + curation_4 + curation_5

# step_1_dir = '/home/ubuntu/MOBIS_MCAM1.0_Curation'

# step_1_folders = ['20241031_164639_Sinwol2Kanghwh_20241031_183546',
#                   '20241031_164639_Sinwol2Kanghwh',
#                   '20241031_195810_Kwanghwa2KwangMyung']
# set_1_folders = list(set(step_1_folders))
# print(len(step_1_folders), len(set_1_folders))


def check_step_2(folder_dir):
    len_img = len(os.listdir(f'{folder_dir}/img'))
    len_pcd = len(os.listdir(f'{folder_dir}/pcd'))
    len_raw = len(os.listdir(f'{folder_dir}/raw'))
    len_yuv = len(os.listdir(f'{folder_dir}/yuv'))
    # print(f'checking cs2_{folder_dir}')
    # print(f'img:{len_img},raw:{len_raw},yuv:{len_yuv}')

    if len_img == 10 and len_raw == 10 and len_yuv == 10 and len_pcd == 10:
        return 0
    else:
        return [len_img, len_pcd, len_yuv, len_raw]
    
complete_files = []
incomplete_files = []

# cnt = 0
n_files = 0
for folder_name in step_1_folders:
    temp_folder_list = os.listdir(f'{step_1_dir}/{folder_name}')
    cnt = 0
    for i in temp_folder_list:
        cnt += 1
        print(f'scanning...{folder_name}/{i}, {cnt}/{len(temp_folder_list)}')
        i_split = i.split('_')
        if len(i_split) == 5:
            i_folder_list = os.listdir(f'{step_1_dir}/{folder_name}/{i}')
            # if 'pcd' not in i_folder_list:
            if ('8879_ldr2cam_calib.json' in i_folder_list) and ('pcd' in i_folder_list):
                n_files += 1
                result = check_step_2(f'{step_1_dir}/{folder_name}/{i}')
                if result == 0:
                    complete_files.append(f'{folder_name}/{i}::{i_split[-1]}')

                else:
                    incomplete_files.append([f'{folder_name}/{i}::{i_split[-1]}', result])
            else:
                files_for_step_3.append(f'{folder_name}/{i}::{i_split[-1]}')

print('\n')
print('\n')
for i in incomplete_files:
    print(i[0], i[1])

print('n_files:', n_files)