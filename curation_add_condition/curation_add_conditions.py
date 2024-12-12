import cv2
import pandas as pd
import os
import json

nx4_excel = 'NX4 curation list (1).xlsx'
mcam_excel = 'MCAM Curation.xlsx'
hm_excel = 'hm_curation_list_3.xlsx'

cols_nx4_excel = ['data 생성일', '하위 폴더명', 'PNG 개수', 
                 'JSON 개수', 'PCD 개수', 'RAW BIN', 
                 'YUV BIN', 'BO생성', '큐레이션 조건', 'ex0', 'ex1', 'ex2', 'ex3', 'ex4']

cols_mcam_excel = ['file name', '키프레임명', 
                 '이미지명', '큐레이션 조건', '작업자', '작업자	메모', '업로드 날짜', 'Step3', '담당자']

cols_hm_excel = ['filename', 'curation1', 'curation2']

def nx4_excel_to_list(nx4_excel):
    df = pd.read_excel(f'{nx4_excel}', engine='openpyxl', sheet_name=0, names=cols_nx4_excel)
    folder_name = df['하위 폴더명'].tolist()
    return df, folder_name

def mcam_excel_to_list(mcam_excel):
    df = pd.read_excel(f'{mcam_excel}', engine='openpyxl', sheet_name=0, names=cols_mcam_excel)
    folder_name = df['file name'].tolist()
    conditions = df['큐레이션 조건'].tolist()
    return df, folder_name, conditions

def hm_excel_to_list(hm_excel):
    df = pd.read_excel(f'{hm_excel}', engine='openpyxl', sheet_name=0, names=cols_hm_excel)
    folder_name = df['filename'].tolist()
    conditions1 = df['curation1'].tolist()
    conditions2 = df['curation2'].tolist()
    return df, folder_name, conditions1, conditions2


nx4_excel_list = nx4_excel_to_list(nx4_excel)
mcam_excel_list = mcam_excel_to_list(mcam_excel)
hm_excel_list = hm_excel_to_list(hm_excel)

# print(hm_excel_list[3])

nx4_conditions_from_mcam = {}

len_nx4 = len(nx4_excel_list[1])
len_mcam = len(mcam_excel_list[1])
len_hm = len(hm_excel_list[1])

for i_nx4 in range(len_nx4):
    fname_nx4 = nx4_excel_list[1][i_nx4]
    cnt = 0

    for j_mcam in range(len_mcam):
        fname_j_mcam = mcam_excel_list[1][j_mcam]
        if fname_nx4 == fname_j_mcam:
            nx4_conditions_from_mcam[f'{fname_nx4}'] = mcam_excel_list[2][j_mcam]
            # temp_data.append([fname_nx4, mcam_excel_list[2][j_mcam]])
            cnt += 1

    for k_hm in range(len_hm):
        fname_k_hm = hm_excel_list[1][k_hm]
        if fname_nx4 == fname_k_hm:
            # print('nnnn', fname_nx4, fname_k_hm)
            if nx4_conditions_from_mcam.get(f'{fname_k_hm}'):
                if str(hm_excel_list[3][k_hm]) == 'nan':
                    nx4_conditions_from_mcam[f'{fname_k_hm}'] = f'{nx4_conditions_from_mcam[f'{fname_k_hm}']}:::{hm_excel_list[2][k_hm]}'
                else:
                    nx4_conditions_from_mcam[f'{fname_k_hm}'] = f'{nx4_conditions_from_mcam[f'{fname_k_hm}']}:::{hm_excel_list[2][k_hm]}, {hm_excel_list[3][k_hm]}'
            else:
                if str(hm_excel_list[3][k_hm]) == 'nan':
                    nx4_conditions_from_mcam[f'{fname_k_hm}'] = f':::{hm_excel_list[2][k_hm]}'
                else:
                    nx4_conditions_from_mcam[f'{fname_k_hm}'] = f':::{hm_excel_list[2][k_hm]}, {hm_excel_list[3][k_hm]}'
            cnt += 1
            
    if cnt == 0:
        # nx4_conditions_from_mcam.append([fname_nx4, '준비중'])
        nx4_conditions_from_mcam[f'{fname_nx4}'] = '준비중'

folder_name_txt = []
val_1_txt = []
val_2_txt = []

for folder_name, value in nx4_conditions_from_mcam.items():
    if ':::' in value:
        sp_val = value.split(':::')
    #     val = sp_val[1]
        if sp_val[1] != sp_val[0] and sp_val[0]:
            print(folder_name, sp_val[0], sp_val[1])
    # # print(key)
        val_1_txt.append(sp_val[0])
        val_2_txt.append(sp_val[1])
        folder_name_txt.append(folder_name)
    else:
        val_1_txt.append(value)
        val_2_txt.append(value)
        folder_name_txt.append(folder_name)

curation_filenames_txt = 'curation_filenames.txt'
with open(curation_filenames_txt, 'w+') as f:
    f.write('\n'.join(folder_name_txt))

curation_val1_txt = 'curation_val1.txt'
with open(curation_val1_txt, 'w+') as f:
    f.write('\n'.join(val_1_txt))

curation_val2_txt = 'curation_val2.txt'
with open(curation_val2_txt, 'w+') as f:
    f.write('\n'.join(val_2_txt))


# print(len(nx4_conditions_from_mcam))

# new_df = pd.DataFrame(index=False, columns=['folder_name', 'Curation조건'])
# for i in nx4_conditions_from_mcam:
#     temp_df = pd.DataFrame({'folder_name': i[0], ''})

# new_df.to_excel('new_sorted_metadata.xlsx', index=False)