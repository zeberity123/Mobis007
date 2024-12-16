import os
import list_step_1
import cv2

origin_tw_root = f'Z:\TW'
txt_file = f'모비스_mcam_v5/auto_test_ubuntu/file_list.txt'
# home_root = f'/home/ubuntu/Curation_MOBIS_MCAM'
home_root = f'Z:\step_1_241203'

f = open(txt_file, 'r')
tw_folder_list = f.read().split()


# yuuv_file, result_rootd, head_file
tw_list = []

for folder_name in tw_folder_list:
    videos_root = f'{origin_tw_root}/{folder_name}/Front/Video'
    for i in os.listdir(videos_root):
        if i[-9:] == '_30Hz.bin':
            tw_file_roots = []
            tw_file_roots.append(f'{videos_root}/{i}')
            tw_file_roots.append(f'{home_root}/{folder_name}')
            tw_file_roots.append(f'{videos_root}/{i.split('.')[0]}.timestamp')
            tw_list.append(tw_file_roots)

cnt = 0

# 12/03 4,5번 재시작 필요 (20241004_175506,20241004_175206)
# 12/04 20241007_100316_Anyang2Dangjin 멈춤 예상. 20241007_100317 재시작 필요.
# 20241007_100616 없음
#  20241008_110805_Kangdonggu2Yangpyeong 시작 [:700] 

# 12/5 20241014_122416_Pochun2Chulwon\20241014_123016 멈춤. 293/1389
# 145개 폴더중 약 14개 완료
# 총 45개 폴더 완료
# 20241011_155941_Songpa2Banpo 부터 시작 [:400]
# Z:\step_1_241203\20241105_100522_Anyang2chunchun 멈춤. 100/1095
# 20241105_133321_Hwado2Sobgpa 부터 시작 [:400]

# 20241107_182943_Dang2Anyang 멈춤. 234/995
# 20241107_182943_Dang2Anyang 부터 20241104_083919_Banpo2Anyang
# 20241104_083919_Banpo2Anyang 멈춤. 4/
# 20241108_163646_Mabook2Mapo 부터 시작

for i in tw_list[:120]:
    cnt+=1
    e1 = cv2.getTickCount()
    list_step_1.auto_step_1(i[0], i[1], i[2])
    e2 = cv2.getTickCount()

    total_time = (e2-e1)/cv2.getTickFrequency()
    print(f'Total time: {total_time}seconds.....{cnt}/{len(tw_list)}')
