import pandas as pd

# 1. 병합할 원본 CSV 파일 목록
file_paths = [
    "법무부_도착지별 내국인 출국자 현황(월별)_20221231.csv",
    "도착지별 내국인 출국자 현황(월별) 20231130.csv",
    "법무부_(요청) 행선국별 국민출국자 현황(2023년1월~7월).csv",
    "법무부 도착지별 내국인 출국자 현황(월별, 2023.12~2024.7).csv"
]

# 2. 파일들을 순차적으로 불러와서 전처리
dfs = []
for path in file_paths:
    try:
        df = pd.read_csv(path, encoding='euc-kr')  # 한글 처리용
    except:
        df = pd.read_csv(path, encoding='utf-8')
    dfs.append(df)

# 3. 각 데이터프레임에서 국가명 + 월별 수치만 추출
cleaned_dfs = []
for df in dfs:
    # 국가명 컬럼 자동 탐지
    country_col = [col for col in df.columns if '국가' in col or '행선국' in col or '지역' in col]
    if not country_col:
        continue
    country_col = country_col[0]

    # 월별 출국자 수 열 추출
    month_cols = df.select_dtypes(include='number').columns.tolist()
    if not month_cols:
        month_cols = [col for col in df.columns if '월' in col or '202' in col or '출국자' in col]

    # 필요한 열 정리
    df_clean = df[[country_col] + month_cols].copy()
    df_clean = df_clean.rename(columns={country_col: '국가'})
    cleaned_dfs.append(df_clean)

# 4. 병합 및 평균 출국자 수 계산
merged_df = pd.concat(cleaned_dfs, ignore_index=True)
merged_df['평균 출국자 수'] = merged_df.drop(columns=['국가']).mean(axis=1, skipna=True)

# 5. 국가별로 평균 다시 집계 (중복 제거)
avg_by_country = merged_df.groupby('국가', as_index=False)['평균 출국자 수'].mean()

# 6. 최종 CSV 저장
output_file = "국가별_평균출국자수.csv"
avg_by_country.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"✅ 파일 저장 완료: {output_file}")
