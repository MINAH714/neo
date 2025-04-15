import pandas as pd

# 1. 병합할 CSV 파일 목록
file_paths = [
    "법무부_도착지별 내국인 출국자 현황(월별)_20221231.csv",
    "도착지별 내국인 출국자 현황(월별) 20231130.csv",
    "법무부_(요청) 행선국별 국민출국자 현황(2023년1월~7월).csv",
    "법무부 도착지별 내국인 출국자 현황(월별, 2023.12~2024.7).csv"
]

# 2. 파일별로 정리
dfs = []
for path in file_paths:
    try:
        df = pd.read_csv(path, encoding='euc-kr')
    except:
        df = pd.read_csv(path, encoding='utf-8')

    # 국가 컬럼 자동 탐지
    country_col = [col for col in df.columns if '국가' in col or '행선국' in col or '지역' in col]
    if not country_col:
        continue
    country_col = country_col[0]

    # 월별 수치 컬럼 탐지
    value_cols = [col for col in df.columns if '월' in col or '202' in col or '출국자' in col]

    # melt (행: 국가, 날짜 / 열: 출국자수)
    df_melted = df.melt(id_vars=[country_col], value_vars=value_cols,
                        var_name='날짜', value_name='출국자수')
    df_melted = df_melted.rename(columns={country_col: '국가'})

    # 날짜 포맷 정리
    df_melted['날짜'] = df_melted['날짜'].str.extract(r'(\d{4}[\.-]?\d{1,2})')[0]
    df_melted['날짜'] = df_melted['날짜'].str.replace('.', '-', regex=False)
    df_melted['날짜'] = pd.to_datetime(df_melted['날짜'], format='%Y-%m', errors='coerce')

    # 출국자수 숫자 변환
    df_melted['출국자수'] = pd.to_numeric(df_melted['출국자수'], errors='coerce')

    dfs.append(df_melted)

# 3. 병합
merged = pd.concat(dfs, ignore_index=True)

# 4. 국가별로 정렬 + 선형보간
merged = merged.sort_values(by=['국가', '날짜'])
merged['출국자수'] = merged.groupby('국가')['출국자수'].transform(lambda x: x.interpolate(method='linear'))

# 5. 결측치 제거
merged_cleaned = merged.dropna(subset=['국가', '날짜', '출국자수'])

# 6. 최종 저장
output_file = "국가별_월별_출국자수_보간적용.csv"
merged_cleaned.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"✅ 저장 완료: {output_file}")
