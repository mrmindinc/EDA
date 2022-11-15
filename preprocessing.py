from data_pre import data_merge, clean_data_generation
from s_EDA import EDA
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Data Preprocessing')

parser.add_argument('--f',
                    type=str,
                    default='user',
                    help='input column')

parser.add_argument('--s',
                    type=str,
                    default='system',
                    help='output column')

parser.add_argument('--t',
                    type=str,
                    default='sentiment',
                    help='sentiment column')

parser.add_argument('--min-len',
                    type=int,
                    default=4,
                    help='문장 최소 길이')

parser.add_argument('--max-len',
                    type=int,
                    default=32,
                    help='문장 최대 길이')

def preprocessing(args, *data):

    # 데이터 머지
    df = data_merge(data)

    # 데이터 전처리
    pre_df = clean_data_generation(df, args)
    print('>> Data Preprocessing Done', '\n')

    # CSV 생성
    import csv
    file_name = 'Test1_data.csv'
    f = open(f'data/{file_name}', 'a+', encoding='utf-8')
    wr = csv.writer(f)
    wr.writerow(['user', 'system', 'label'])

    input = pre_df[args.f]
    output = pre_df[args.s]
    sentiment = pre_df[args.t]

    # EDA
    cnt = 0
    for inp, out, sen in zip(input, output, sentiment):
        for eda_input in list(set(EDA(inp))):
            if len(eda_input) >= args.min_len:
                cnt += 1
                wr.writerow([eda_input, out, sen])

    print(f'>> EDA Data {cnt}개 생성')
    print(f'>> {file_name} Data Save Complete')


if __name__ == '__main__':
    args = parser.parse_args()
    df_large = pd.read_csv('data/[Ai_HUB]chatbot_data_large[34M].csv')
    df_small = pd.read_csv('data/[Ai_HUB]chatbot_data_small[2.7M].csv')
    df_voucher = pd.read_csv('data/[DATAVoucher]chatbot_data[2M].csv', encoding='cp949')
    df_sculpture = pd.read_csv('data/[MrMind]chatbot_data[0.57M].csv')
    df_doll = pd.read_csv('data/[MrMind]doll_chat_data[0.85M].csv')

    preprocessing(args, df_small, df_voucher, df_sculpture, df_doll)