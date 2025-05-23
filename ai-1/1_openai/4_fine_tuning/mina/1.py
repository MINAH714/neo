import os
import json

root_dir = 'archiv'  # archiv 폴더 경로 (필요하면 절대 경로로 바꾸세요)
all_data = []

# archiv 폴더 안 모든 하위 폴더 탐색
for subfolder in os.listdir(root_dir):
    subfolder_path = os.path.join(root_dir, subfolder)
    if os.path.isdir(subfolder_path):  # 폴더인지 확인
        # 해당 하위 폴더 내 모든 파일 중 .json 파일만 처리
        for filename in os.listdir(subfolder_path):
            if filename.endswith('.json'):
                file_path = os.path.join(subfolder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # data가 리스트면 extend, 아니면 append
                    if isinstance(data, list):
                        all_data.extend(data)
                    else:
                        all_data.append(data)

# 합친 데이터를 하나의 JSON 파일로 저장
with open('merged_all.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)