import os
import time

root = r'C:\Users\user\Desktop\test_timestamp_error\error_original'

cnt = 0
w = os.listdir(root)
for s in w:
    folder = os.path.join(root, s)
    folder_list = os.listdir(folder)
    for i in folder_list:
        time_root = os.path.join(folder, i)
        stamp_root = os.path.join(time_root, 'timestamp_info.txt')
        if os.path.exists(stamp_root):
            print(stamp_root)
            os.remove(stamp_root)
            cnt += 1

print(cnt)