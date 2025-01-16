import os
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def find_files_in_directory(base_path, keyword, exclude_folders):
    """
    특정 디렉토리에서 키워드를 포함한 파일을 찾는 함수.
    """
    matching_files = []
    stack = [base_path]  # 탐색할 디렉토리 스택

    while stack:
        current_path = stack.pop()

        try:
            with os.scandir(current_path) as entries:
                for entry in entries:
                    if entry.is_dir(follow_symlinks=False):
                        # 제외할 폴더를 스킵
                        if entry.name not in exclude_folders:
                            stack.append(entry.path)
                    elif entry.is_file() and keyword in entry.name:
                        matching_files.append(entry.path)
        except PermissionError:
            # 접근 권한 오류를 무시
            continue

    return matching_files

def search_directories(directories, keyword, exclude_folders):
    """
    여러 디렉토리를 병렬로 처리하여 파일을 찾는 함수.
    """
    results = []
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(find_files_in_directory, directory, keyword, exclude_folders)
            for directory in directories
        ]
        for future in tqdm(futures, desc="Processing directories", unit="directory"):
            results.extend(future.result())

    return results
import json
import shutil
import os


def load_json_file(file_path):
    """
    JSON 파일을 불러오는 함수.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        print(f"JSON 파일 '{file_path}'이 성공적으로 로드되었습니다.")
        return data
    except FileNotFoundError:
        print(f"JSON 파일 '{file_path}'을 찾을 수 없습니다.")
        return None
    except json.JSONDecodeError:
        print(f"JSON 파일 '{file_path}'의 형식이 잘못되었습니다.")
        return None


if __name__ == '__main__':
    # 확인할 디렉토리와 키워드 정의
    base_directories = [
        # fr'Y:\\step1_241217'
        # fr'C:\\Users\\user\\Desktop\\test_timestamp_error\\error_original'
        # fr'Y:\\MOBIS_MCAM1.0_02\\step1_241227'
        # fr'Y:\\MOBIS_MCAM1.0_03\\step1_250101'
        # fr'Y:\\MOBIS_MCAM1.0_12\\step1_241228'
        fr'Y:\\MOBIS_MCAM1.0_02_2\\step1_250116'
        # fr'/run/user/1000/gvfs/smb-share:server=192.168.100.60,share=m_data/Step2_',
        # fr'/run/user/1000/gvfs/smb-share:server=192.168.100.60,share=m_data/Step1_2_3',
        # fr'/run/user/1000/gvfs/smb-share:server=192.168.100.60,share=m_data/Step2_All_Complete',
        # fr'/run/user/1000/gvfs/smb-share:server=192.168.100.60,share=m_data/NAS3_Step2',
        # fr'/run/user/1000/gvfs/smb-share:server=192.168.100.60,share=m_data/Step2_Keyframe_Complete'
    ]
    keyword = "timestamp_info.txt"
    exclude_folders = {"Dark_img_full", "Img_full"}  # 제외할 폴더 이름
    os.makedirs('timestamp', exist_ok=True)
    # 파일 경로 검색
    all_matching_files = search_directories(base_directories, keyword, exclude_folders)

    for da in all_matching_files:
        da_split = da.split('\\')
        print(da_split)
        save_base_dir  = os.path.join('timestamp',da_split[-3],da_split[-2])
        os.makedirs(save_base_dir, exist_ok=True)
        shutil.copy(da, os.path.join(save_base_dir, os.path.basename(da)))
        print(da)
        print(save_base_dir, os.path.basename(da))
        
    print('모든 Step1의 타임스템프가 추출되었습니다.')