import pandas as pd

file_path = 'airport_code.csv'

try:
    df = pd.read_csv(file_path, encoding='utf-8') 
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding='cp949')

print("columns")
print(df.columns)
print('-' * 50)

filtered_df = df.iloc[:, [2, 7]]

print("추출된 데이터")
print(filtered_df.head())

output_file = 'filtered_airport_codes.csv'
filtered_df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n '{output_file}' 파일로 저장 완료!")