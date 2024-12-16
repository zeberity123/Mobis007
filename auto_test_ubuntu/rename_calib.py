import os

cnt = 0
for curation_num in os.listdir():
    # if 'Curation' in curation_num:
    if 'step_1_241203' in curation_num:
        date_routes = os.listdir(curation_num)
        for date_route in date_routes:
            curation_folders = os.listdir(f'{curation_num}/{date_route}')
            for curation_folder in curation_folders:
                json_1_root = f'{curation_num}/{date_route}/{curation_folder}'
                if os.path.exists(f'{json_1_root}/8879_ldr2cam_calib.json'):
                    cnt += 1
                    os.rename(f'{json_1_root}/8879_ldr2cam_calib.json', f'{json_1_root}/ldr2cam_calib.json')
                    os.rename(f'{json_1_root}/extrinsic_calib_ECO_result_NX4_8879_ECO_fisheye_trans_EOL143eco_updated.json', f'{json_1_root}/Cam_calib.json')
                    print(f'renamed: {json_1_root}')

print(f'Renamed total: {cnt}pairs')

while True:
    user_input = input("\nEnter q to quit: ")
    if user_input.lower() == 'q':
        break