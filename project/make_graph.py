import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (설치된 경우만 적용)
plt.rcParams['font.family'] = 'NanumBarunGothic'

# 1. CSV 불러오기
df = pd.read_csv("final_filled.csv", encoding="utf-8-sig")

# 2. '기타' 국가 제거
df = df[~df['행선국(지역)'].str.contains("기타")]

# 3. 출국자수 컬럼 리스트 (국가명 제외)
출국자수_컬럼들 = df.columns.difference(['행선국(지역)'])

# 4. NaN이 하나도 없는 국가만 필터링 (즉, 보간된 값이 없었던 국가만)
df_no_missing = df[df[출국자수_컬럼들].notnull().all(axis=1)]

# 5. 국가별 총합 계산
df_no_missing['총 출국자수'] = df_no_missing[출국자수_컬럼들].sum(axis=1)

# 6. 상위 5개국 추출
top5 = df_no_missing.sort_values(by='총 출국자수', ascending=False).head(5)

# 7. 그래프 시각화
plt.figure(figsize=(10, 6))
bars = plt.bar(top5['행선국(지역)'], top5['총 출국자수'], color='skyblue')
plt.title("출국자 수 상위 5개국 (보간 없이 완전한 데이터)")
plt.xlabel("국가")
plt.ylabel("출국자 수")
plt.xticks(rotation=45)

# 8. 막대 위에 수치 표시
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, f"{int(yval):,}", ha='center', va='bottom')

# 9. 그래프 저장
plt.tight_layout()
plt.savefig("출국자수_상위5_완전데이터만.png", dpi=400, bbox_inches='tight')
print("✅ 그래프 저장 완료: 출국자수_상위5_완전데이터만.png")
plt.show()
