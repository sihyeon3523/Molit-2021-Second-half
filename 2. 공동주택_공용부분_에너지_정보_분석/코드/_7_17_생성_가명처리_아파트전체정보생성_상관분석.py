# -*- coding: utf-8 -*-
"""#7 ~ 17 생성_가명처리_아파트전체정보생성_상관분석

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1H_Aq9hl4IVFAbDo5HbBp2DwQfe81JNeN

## 분석 데이터 생성 및 상관분석
- 가명처리 : "단지기본정보_ver3.csv" 생성
- 관리비정보 + 단지기본정보 + 관리시설정보 = "아파트전체정보.csv" 생성
- 상관분석 진행 

**분석 데이터 생성 후, 엑셀 작업**
- #7 Graph. 전기계약방식과 준공년도별 평균 공용 전기료
- #8 Graph. 전기계약방식과 세대수별 평균 공용 전기료
- #9 Graph. 단일계약 공동주택 연평균 공용 전기료
- #10 Graph. 종합계약 공동주택 연평균 공용 전기료
- #11 Graph. 단일계약 공동주택 승강기수와 연평균 공용 전기료
- #12 Graph. 종합계약 공동주택 승강기수와 연평균 공용 전기료
- #13 Graph. 단일계약 공동주택 부대복리시설수와 연평균 공용 전기료 
- #14 Graph. 종합계약 공동주택 부대복리시설수와 연평균 공용 전기료
- #15 Graph. 단일계약 공동주택 주차 대수와 연평균 공용 전기료
- #16 Graph. 종합계약 공동주택 주차 대수와 연평균 공용 전기료
- #17 Graph. 공동주택 단지 시설 특성과 전기공용금액과의 상관관계
"""

import pandas as pd

df_fee = pd.read_csv("관리비정보.csv", engine = 'python', encoding = 'utf-8')

df_basic = pd.read_csv("단지기본정보_ver2.csv", engine = 'python')

df_fac = pd.read_excel("관리시설정보.xlsx")

df_fee.head()

df_basic.head()

df_fac.head()

"""### 사용하지 않는 열 제거"""

df_fee.columns

df_basic.columns

df_fac.columns

df_fee_drop = df_fee.drop(['난방공용_우리단지총액', '난방전용_우리단지총액', '급탕공용_우리단지총액',
       '급탕전용_우리단지총액', '가스공용_우리단지총액', '가스전용_우리단지총액', 
             '전기전용_우리단지총액', '수도공용_우리단지총액', '수도전용_우리단지총액'], axis = 1)

df_basic_drop = df_basic.drop(['도로명주소', '분양형태', '관리방식', '난방방식',
       '복도유형', '연면적','주거전용면적', '시공사', '시행사', '60㎡이하',
       '60㎡초과 \n\n85㎡이하)', '85㎡초과\n\n135㎡이하)', '135㎡초과' ], axis = 1)

df_fac_drop = df_fac.drop(['일반관리', '경비관리', '청소관리', '소독관리', '건물구조', '수전용량',
                           '전기안전관리자법정선임여부', '화재수신반방식', '급수방식', '승강기관리형태',
                          '부대복리시설1', '부대복리시설2', '부대복리시설3',
       '부대복리시설4', '부대복리시설5', '부대복리시설6', '부대복리시설7', '부대복리시설8', '부대복리시설9',
       '부대복리시설10', '부대복리시설11'], axis = 1)

df_fee_drop.head()

df_basic_drop.head()

df_fac_drop.head()

"""### 가명처리
- 가명칭 : 법정동 명 + 임의의 숫자  
"""

df_basic_drop = df_basic_drop.drop('가명칭', axis = 1)

df_basic_drop['가명칭'] = ''

df_basic_drop['법정동'][0][:-1]

법정동 = list(df_basic_drop['법정동'].unique())

법정동.sort()

법정동

df_basic_drop = df_basic_drop.sort_values(by = '법정동', ascending = False)

df_basic_drop

cnt  = 1
for j in 법정동:
    for i in range(len(df_basic_drop)):
        print(j)
        if df_basic_drop.loc[i, '법정동'] == j:
            df_basic_drop.loc[i, '가명칭'] = df_basic_drop.loc[i, '법정동'][:-1] + str(cnt)
            cnt += 1
        else:
            cnt = 1
            continue

df_basic_drop = df_basic_drop.sort_index()

df_basic_drop

df_basic_drop.to_csv("단지기본정보_ver3.csv", encoding = 'utf-8', index = False)

"""### 아파트전체정보 생성
- 관리비정보 + 단지기본정보 + 관리시설정보
- 명칭(단지코드) 기준으로 데이터 셋 병합
"""

df_fee_drop = df_fee_drop.drop('의무', axis = 1)

df_basic_drop = df_basic_drop.drop('의무', axis = 1)

df_fac_drop = df_fac_drop.drop('의무', axis = 1)

df_fee_drop.head()

df_basic_drop.head()

df_fac_drop.head()

# df_fee_drop, df_basic_drop, df_fac_drop 합치기 
merge_left = pd.merge(df_fee_drop, df_basic_drop, how = 'left', left_on = '명칭(단지코드)', right_on = '명칭(단지코드)')

merge_whole = pd.merge(merge_left, df_fac_drop, how = 'left', left_on = '명칭(단지코드)', right_on = '명칭(단지코드)')

merge_whole.info()

merge_whole.head(5)

merge_whole.shape

merge_whole.to_csv("아파트전체정보.csv", index = False, encoding = 'utf-8')



"""### 상관분석"""

import pandas as pd
merge_whole = pd.read_csv("아파트전체정보.csv", engine = 'python', encoding = 'utf-8')

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
# %matplotlib inline

# Commented out IPython magic to ensure Python compatibility.
# 레티나 디스플레이(고밀도 화소를 가진 화질)를 지원하도록 해서 한글이 흐릿하게 보이는 현상을 개선
# %config InlineBackend.figure_format = 'retina'

mpl.rcParams['axes.unicode_minus'] = False

# Commented out IPython magic to ensure Python compatibility.
plt.rc('font', family = 'NanumBarunGothic')
print(plt.rcParams['font.family'])
# %matplotlib inline

plt.figure(figsize=(5,5))
plt.plot([0,1], [0,1], label='한글테스트용')
plt.legend()
plt.show()

merge_whole.columns

merge_whole.head(5)

df_corr = merge_whole.loc[:, ['전기공용_우리단지총액',  '승강기대수', '부대복리시설수', '지상', '지하']]

df_corr = df_corr.dropna(axis = 0)

df_corr = df_corr.rename({'전기공용_우리단지총액': '공용 전기료', '지상': '지상주차대수', '지하':'지하주차대수'}, axis = 1)

df_corr.head()

df_corr_result = df_corr.corr(method='pearson')

plt.figure(figsize=(12,8))
plt.rc('font', size=15)    
sns.heatmap(data = df_corr_result, 
            annot=True, fmt='.2f',  
            linewidths=.5, # 경계면 실선으로 구분하기 
            cbar_kws={"shrink": .5}, # 컬러바 크기 절반으로 줄이기
           # vmin = -1,vmax = 1,  # 컬러바 범위 -1 ~ 1
            cmap='Greens')

type(df_corr_result)

df_corr_result.to_csv("아파트단지시설특성과전기공용금액과의상관관계.csv", encoding='cp949', index =False)