import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st

import plotly.io as io
io.renderers.default='browser' #이거 해야 ploty 실시간 확인 가능 fig.show()가 인터넷 창에
st.set_page_config(page_title='월간수출입통계',  layout='wide')
#%% 
data = pd.read_excel("발표 데이터.xlsx", sheet_name="showing_data")

chart_df = pd.DataFrame()
chart_df["month"] = pd.DatetimeIndex(data["date"]).month
chart_df["year"] = pd.DatetimeIndex(data["date"]).year
chart_df["date"] = pd.DatetimeIndex(data["date"]).strftime("%Y년 %m월")

chart_df["수입 금액"] = data["수입 금액"].astype("float")
chart_df["수출 금액"] = data["수출 금액"].astype("float")

chart_df["무역수지"] =data["무역수지"].astype("float")
chart_df["전년 동월 대비 수출 증감률"] = data["전년 동월 대비 수출 증감률"] * 100

chart_df = chart_df.sort_values("date")


#%% streamlit 출력
st.title("무역 수출입통계")
#%% 해당기 근황 출력
st.header("무역 통계 현황")


year_month_selected = st.selectbox(
     '어느 기의 값을 보시겠습니까?',
     chart_df["date"].iloc[12:].sort_index(ascending = False))
#year_month_selected = "2022년 01월"

selected = chart_df[chart_df["date"] == year_month_selected]

#selected.columns

year_calc = selected["year"].iloc[0]
month_calc = selected["month"].iloc[0]

is_before_12month = st.checkbox('전년동월비를 보시겠습니까?')

if is_before_12month:
    diff_help_message = "전년동월 대비 증감비"
    before_12month = (year_calc - 1), month_calc
    df_selection_for_diff = chart_df.query(
        "(year == @before_12month[0]) and (month == @before_12month[1])"
        )
else:
    diff_help_message = "전월 대비 증감비"
    before_1month = (year_calc-1, 12) if month_calc == 1 else (year_calc, month_calc-1)  
    df_selection_for_diff = chart_df.query(
        "(year == @before_1month[0]) and (month == @before_1month[1])"
        )


first_layer_col1, first_layer_col2, first_layer_col3 = st.columns(3)

first_layer_col1.metric("무역수지", 
            "{0:,.2f} 백 만불".format(selected["무역수지"].iloc[0]/1000),  
            #"{0:,.2f} %".format(selected["무역수지"].iloc[0]/ df_selection_for_diff["무역수지"].iloc[0]),
            help=diff_help_message)
first_layer_col2.metric("수출금액",
            "{0:,.2f} 백 만불".format(selected["수출 금액"].iloc[0]/1000),  
            "{0:,.2f} %".format(selected["수출 금액"].iloc[0]/ df_selection_for_diff["수출 금액"].iloc[0]),
            help=diff_help_message)
first_layer_col3.metric("수입금액",
            "{0:,.2f} 백 만불".format(selected["수입 금액"].iloc[0]/1000),  
            "{0:,.2f} %".format(selected["수입 금액"].iloc[0]/ df_selection_for_diff["수입 금액"].iloc[0]),
            help=diff_help_message)

#%% plotly 그래프 1 전체 다함께
st.header("종합 그래프")

start_index_fig_bar, end_index_fig_bar = st.select_slider(
    '표를 확인할 범위를 설정하시오',
    options= chart_df["date"],
    value=(chart_df.iloc[0]["date"], chart_df.iloc[-1]["date"] ))

df_column_slided = chart_df.query("(date >= @start_index_fig_bar) and (date<= @end_index_fig_bar)")

# 수출 금액은 음의 방향으로 되어 있음


main_fig = make_subplots(specs=[[{"secondary_y": True}]])


main_fig.add_trace(
    go.Scatter(
        x = df_column_slided["date"], 
        y = df_column_slided["수입 금액"], 
        name = "수입 금액 (천 불)"
        )
    )

main_fig.add_trace(
    go.Scatter(
        x = df_column_slided["date"], 
        y = df_column_slided["수출 금액"], 
        name = "수출 금액 (천 불)"
        )
    )

main_fig.add_bar(
    x = df_column_slided["date"], 
    y = df_column_slided["무역수지"], 
    name="무역 수지"
    )

main_fig.update_layout(title='무역량 그래프', xaxis_title='기간', yaxis_title='액수 (천 달러)')
main_fig.update_traces(hovertemplate='%{x}: %{y}')
#fig_bar.show()

st.plotly_chart(main_fig, use_container_width=True)