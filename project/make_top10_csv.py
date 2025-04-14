import pandas as pd
import matplotlib.pyplot as plt

# 📌 한글 폰트 설정
plt.rcParams['font.family'] = 'NanumBarunGothic'

# 1. 데이터 불러오기
df = pd.read_csv("국가별_평균출국자수.csv", encoding='utf-8-sig')

# 2. '기타' 국가 제거
df = df[~df['국가'].str.contains("기타")]

# 3. 정렬
df_sorted = df.sort_values(by='평균 출국자 수', ascending=False)

# 4. 상위 / 하위 10개국 추출
top10 = df_sorted.head(10)
bottom10 = df_sorted.tail(10)

# ✅ y축 최대값 통일
y_max = df_sorted['평균 출국자 수'].max() * 1.1  # 상위국 기준 최대치의 110%

# 5. 시각화
plt.figure(figsize=(14, 6))

# ▶ 상위 10개국
plt.subplot(1, 2, 1)
plt.bar(top10['국가'], top10['평균 출국자 수'], color='skyblue')
plt.title("평균 출국자 수 상위 10개국")
plt.xlabel("국가")
plt.ylabel("평균 출국자 수")
plt.xticks(rotation=45)
plt.ylim(0, y_max)

# ▶ 하위 10개국
plt.subplot(1, 2, 2)
plt.bar(bottom10['국가'], bottom10['평균 출국자 수'], color='salmon')
plt.title("평균 출국자 수 하위 10개국")
plt.xlabel("국가")
plt.ylabel("평균 출국자 수")
plt.xticks(rotation=45)
plt.ylim(0, y_max)

# 저장 및 출력
plt.tight_layout()
plt.savefig("평균출국자수_상하위10_공통축.png", dpi=400, bbox_inches='tight')
print("✅ 저장 완료: 평균출국자수_상하위10_공통축.png")
plt.show()