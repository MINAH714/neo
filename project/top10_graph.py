import pandas as pd
import matplotlib.pyplot as plt

# ✅ 폰트 설정 (VS Code나 로컬에 NanumBarunGothic 설치되어 있어야 함)
plt.rcParams['font.family'] = 'NanumBarunGothic'

# 1. CSV 불러오기
filename = 'KOSIS_한국인_출국국가별_여행객수_2022_2024.csv'
df = pd.read_csv(filename)

# 2. 국가별 총합 계산
df_total = df.groupby('국가')['여행객수'].sum().reset_index()

# 3. 상위/하위 10개국 추출
top10 = df_total.sort_values(by='여행객수', ascending=False).head(10)
bottom10 = df_total.sort_values(by='여행객수').head(10)

# 4. 그래프 시각화
plt.figure(figsize=(14, 6))

# ▶ 상위 10개국
plt.subplot(1, 2, 1)
plt.bar(top10['국가'], top10['여행객수'], color='skyblue')
plt.title("출국 여행객 수 상위 10개국 (2022~2024)")
plt.xlabel("국가")
plt.ylabel("여행객 수")
plt.xticks(rotation=45)

# ▶ 하위 10개국
plt.subplot(1, 2, 2)
plt.bar(bottom10['국가'], bottom10['여행객수'], color='salmon')
plt.title("출국 여행객 수 하위 10개국 (2022~2024)")
plt.xlabel("국가")
plt.ylabel("여행객 수")
plt.xticks(rotation=45)

# 5. 그래프 저장
plt.tight_layout()
output_file = '출국여행객_상위하위10개국.png'
plt.savefig(output_file, dpi=400, bbox_inches='tight')
print(f"{output_file} 저장 완료!")

# 6. 화면 출력
plt.show()
