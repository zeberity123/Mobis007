from distutils.dir_util import copy_tree
import cv2


# tw_home = f'Z:/step_1_241203'
copy_dest = f'files_to_copy'

# success_txt = '01021156_step4.txt'
success_txt = '01241401_step4.txt'
with open(success_txt, 'r') as f:
    data = f.read()
success_list = data.splitlines()

files_to_process = []

for i in success_list:
    i_split = i[6:].split('/')
    last_split = i_split[-1].split('::')
    last_folder_name = f'{last_split[0]}_{last_split[0]}_{last_split[1]}'
    copy_root = f'{i_split[0]}/{i_split[1]}/{i_split[2]}/{i_split[3]}/{last_folder_name}'
    dest_root = f'{copy_dest}/{i_split[1]}/{i_split[2]}/{i_split[3]}/{last_folder_name}'
    files_to_process.append([copy_root, dest_root])
    print(copy_root)
    print(dest_root)

print(f'files to copy: {len(files_to_process)}')

cnt = 0
for i in files_to_process:
    e1 = cv2.getTickCount()
    copy_tree(i[0], i[1])
    e2 = cv2.getTickCount()
    time_spent = (e2-e1)/cv2.getTickFrequency()
    cnt += 1
    print(f'copied {i[0]}')
    print(f'time: {time_spent}seconds')
    print(f'{cnt}/{len(files_to_process)}')