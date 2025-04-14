import pandas as pd
import matplotlib.pyplot as plt

# 📌 한글 폰트 설정 (설치된 경우만)
plt.rcParams['font.family'] = 'NanumBarunGothic'

# 1. 파일 불러오기
df = pd.read_csv("국가별_평균출국자수.csv", encoding="utf-8-sig")

# 2. '기타' 국가 제거 (선택 사항)
df = df[~df['국가'].str.contains("기타")]

# 3. 국가 이름 기준 정렬 (또는 평균 출국자 수 기준 정렬도 가능)
df = df.sort_values(by='평균 출국자 수', ascending=False)

# 4. 전체 그래프 시각화
plt.figure(figsize=(16, 8))
plt.bar(df['국가'], df['평균 출국자 수'], color='mediumseagreen')
plt.title("국가별 평균 출국자 수 (전체 비교)")
plt.xlabel("국가")
plt.ylabel("평균 출국자 수")
plt.xticks(rotation=75, ha='right')

# 5. 그래프 저장 및 출력
plt.tight_layout()
plt.savefig("국가별_평균출국자수_전체그래프.png", dpi=400, bbox_inches='tight')
print("✅ 전체 비교 그래프 저장 완료!")
plt.show()
