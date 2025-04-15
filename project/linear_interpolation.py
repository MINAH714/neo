import pandas as pd
import numpy as np

# 1. CSV 불러오기
df = pd.read_csv("final.csv")

# 2. 0을 NaN으로 변환 (첫 번째 열 제외)
df.iloc[:, 1:] = df.iloc[:, 1:].replace(0, np.nan)

# 3. 선형 보간 적용
df.iloc[:, 1:] = df.iloc[:, 1:].interpolate(method='linear', axis=0)

# 4. NaN 남았는지 체크
if df.iloc[:, 1:].isna().sum().sum() > 0:
    raise ValueError("보간 후에도 NaN이 남아 있어요!")

# 5. 정수로 변환
df.iloc[:, 1:] = df.iloc[:, 1:].round().astype(int)

# 6. CSV 저장 시 소수점 없이 저장되게 설정
df.to_csv("final_filled.csv", index=False, float_format='%d')

print("🎉 완벽 저장 완료! .0 없이 깔끔한 정수 CSV 완성")
