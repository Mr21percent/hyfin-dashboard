import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
import plotly.io as io


data = pd.read_excel("발표 데이터.xlsx", sheet_name="show_data2")

chart_df = data
chart_df["month"] = pd.DatetimeIndex(data["date"]).month
chart_df["year"] = pd.DatetimeIndex(data["date"]).year
chart_df["date"] = pd.DatetimeIndex(data["date"]).strftime("%Y년 %m월")

st.header("종합 그래프")

start_index_fig_bar, end_index_fig_bar = st.select_slider(
    '표를 확인할 범위를 설정하시오',
    options= chart_df["date"],
    value=(chart_df.iloc[-18]["date"], chart_df.iloc[-1]["date"] ))

df_column_slided = chart_df.query("(date >= @start_index_fig_bar) and (date<= @end_index_fig_bar)")

# 수출 금액은 음의 방향으로 되어 있음


main_fig = go.Figure(
    data = [
        go.Bar(    
            x = df_column_slided["date"], 
            y = df_column_slided["PCEC"], 
            name="소비지출",
            offsetgroup = 0
            ),
        
        go.Bar(    
            x = df_column_slided["date"], 
            y = df_column_slided["PCESV"], 
            name="서비스 소비지출",
            offsetgroup = 1
            ),
        
        go.Bar(    
            x = df_column_slided["date"], 
            y = df_column_slided["PCDG"], 
            name="내구재 소비지출",
            offsetgroup = 1,
            base = df_column_slided["PCESV"],
            ),
        
        ]
)


main_fig.update_layout(title='소비지출', xaxis_title='기간', yaxis_title='액수 (Billions of Dollars)')
st.plotly_chart(main_fig, use_container_width=True)

sub_fig = make_subplots(specs=[[{"secondary_y": True}]])
sub_fig.add_trace(
    go.Scatter(
        x = df_column_slided["date"], 
        y = df_column_slided["내구재 지출비중"]*100, 
        name = "내구재 지출비중"
        ),
    )
sub_fig.add_trace(
    go.Scatter(
        x = df_column_slided["date"], 
        y = df_column_slided["서비스 지출비중"]*100, 
        name = "서비스 지출비중"
        ),
    secondary_y=True
    )
sub_fig.update_layout(title='지출 비중', xaxis_title='기간', yaxis_title=' 비중 (%) ')
st.plotly_chart(sub_fig, use_container_width=True)