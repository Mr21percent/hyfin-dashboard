# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 09:53:35 2023

@author: woneunglee
"""

import pandas as pd


url = "https://apis.data.go.kr/1220000/Itemtrade/getItemtradeList?"
인증키 = "WELKs76NiwpOK8rD5mIq4CrEEgswzBhwJOEaVc9S5vkmJL7mMUF03SBfmchN9BdnZCERARnfKOVQPNfj8t8mXA=="
시작년월 = "202201"
종료년월 = "202212"
#시작과 종료의 조회기간은 1년이내 기간만 가능합니다
final_url = url + "serviceKey=" + 인증키 + "&strtYymm=" + 시작년월 + "&endYymm=" + 종료년월
print(final_url)
#curdf = pd.read_xml(final_url , xpath=".//item")

# 해당 데이터의 hsCode는 강제적으로 10자리로 고정되어있음
# 즉 상위항목을 따로 추려내기 위해서는 21 ---- 와 같은 정규식 사용 필요


#데이터 공공 api에서 가져오는 코드
df_list = []
for year in range(1995, 2024):
    시작년월 = str(year) + "01"
    종료년월 = str(year) + "12"
    print(year)
    request_url = url + "serviceKey=" + 인증키 + "&strtYymm=" + 시작년월 + "&endYymm=" + 종료년월
    curdf = pd.read_xml(request_url , xpath=".//item")
    df_list.append(curdf)
df = pd.concat(df_list)

df.to_csv("data2.csv")