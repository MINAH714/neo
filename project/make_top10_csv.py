import requests
import pandas as pd

# 1. API URL (너가 준 링크 그대로)
url = "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MjQ0OWE0YWE1ZmRmMmYyZGRlZmFiM2FmODJkYjg2Nzk=&itmId=T10+T20+T30+&objL1=ALL&objL2=00+&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=Y&newEstPrdCnt=3&orgId=101&tblId=DT_1B28014"

# 2. API 요청 (JSON 형식으로 받아옴)
response = requests.get(url)
data = response.json()

# 3. JSON → pandas DataFrame으로 변환
df = pd.DataFrame(data)

# 4. 필요한 열만 추출해서 정리
df_filtered = df[['PRD_DE', 'C1_NM', 'DT']].copy()
df_filtered.columns = ['연도', '국가', '여행객수']

# 5. 여행객수 숫자형으로 변환
df_filtered['여행객수'] = pd.to_numeric(df_filtered['여행객수'], errors='coerce')

# 6. CSV 파일로 저장
filename = "KOSIS_한국인_출국국가별_여행객수.csv"
df_filtered.to_csv(filename, index=False, encoding='utf-8-sig')

print(f"✅ CSV 저장 완료: {filename}")
