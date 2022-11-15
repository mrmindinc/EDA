import pandas as pd
import re


def data_merge(data):
    df = pd.concat(data)
    df = df.reset_index(drop=True)

    return df


def build_corpus(src):
    src = str(src)

    try:    # 대문자가 있을시
        src = src.lower()

    except: # 대문자가 없을시
        pass

    src = src.replace('・·-', ' ')                           # 특수문자 ・·- 제거
    src = src.replace('00님', '어르신')
    src = src.replace('-----희망의 전화 129청소년 전화 1388자살예방핫라인 1577-0199생명의 전화 1588-9191사랑의 전화 상담센터 1566-2525', '')
    src = re.sub(r'\([^)]*\)', '', src)                       # (abc) -> ()안 단어 및 () 제거
    src = re.sub(r'\[[^)]*\]', '', src)                       # [abc] -> []안 단어 및 [] 제거
    src = re.sub('[^a-z A-Z 가-힣 0-9 .,?!_-]', '', src)      # 영어 소문자. 영어 대문자, 한글, 숫자 .,?!_- 를 제외한 모든 문자 제거

    return src


def clean_data_generation(data, parser):
    
    parser

    # 중복 제거
    print(f'>> 기존 데이터 {len(data)}개')
    new_data = data.drop_duplicates(subset=parser.f, keep='first', inplace=False, ignore_index=True)
    print(f'>> 중복 제거 데이터 {len(new_data)}개')

    # null값 제거  
    new_data = new_data.dropna(subset=[parser.f, parser.s], how='any', axis=0, inplace=False)
    print(f'>> null 제거 데이터 {len(new_data)}개')

    # 특수문자 제거
    new_data[parser.f] = new_data[parser.f].apply(lambda x: build_corpus(x))
    new_data[parser.s] = new_data[parser.s].apply(lambda x: build_corpus(x))
    print(f'>> 전처리 데이터 {len(new_data)}개')

    # 길이가 특정 이하 데이터 제거
    new_data = new_data[new_data[parser.f].apply(lambda x: len(x) >= parser.min_len)]
    new_data = new_data[new_data[parser.s].apply(lambda x: len(x) >= parser.min_len)]
    print(f'>> 길이가 {parser.min_len}이하 데이터 제거 데이터 {len(new_data)}개')

    # 길이가 특정 이상 데이터 제거
    new_data = new_data[new_data[parser.f].apply(lambda x: len(x) <= parser.max_len)]
    new_data = new_data[new_data[parser.s].apply(lambda x: len(x) <= parser.max_len)]
    print(f'>> 길이가 {parser.max_len}이상 데이터 제거 데이터 {len(new_data)}개')

    # 데이터 길이 확인
    max_len = max([len(w) for w in new_data[parser.f]])
    min_len = min([len(w) for w in new_data[parser.f]])

    print('>> 문장 최장 길이 :', max_len)
    print('>> 문장 최단 길이 :', min_len, '\n')

    return new_data.reset_index(drop=True)
