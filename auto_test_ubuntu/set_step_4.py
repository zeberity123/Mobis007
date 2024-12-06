import shutil

json_1 = '8879_ldr2cam_calib.json'
json_2 = 'extrinsic_calib_ECO_result_NX4_8879_ECO_fisheye_trans_EOL143eco_updated.json'

def auto_step_4(folder_dir):
    shutil.copyfile(json_1, f'{folder_dir}/{json_1}')
    shutil.copyfile(json_2, f'{folder_dir}/{json_2}')
    # print(f'step_4: copied to {folder_dir}')