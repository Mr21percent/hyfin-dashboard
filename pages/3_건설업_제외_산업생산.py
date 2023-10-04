import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
import plotly.io as io


data = pd.read_excel("발표 데이터.xlsx", sheet_name="show_data4")

chart_df = data
chart_df["month"] = pd.DatetimeIndex(data["date"]).month
chart_df["year"] = pd.DatetimeIndex(data["date"]).year
chart_df["date"] = pd.DatetimeIndex(data["date"]).strftime("%Y년 %m월")

st.header("Industrial production Manufacturing")
st.write("2015=100, Q2 2023 or latest available")

slider_range = chart_df["date"].drop_duplicates().sort_values()

start_index_fig_bar, end_index_fig_bar = st.select_slider(
    '표를 확인할 범위를 설정하시오',
    options= slider_range ,
    value=(slider_range.iloc[-24], slider_range.iloc[-1] ))

is_new_100 = st.checkbox('시작을 100으로 고정하시겠습니까?')


df_column_slided = chart_df.query("(date >= @start_index_fig_bar) and (date<= @end_index_fig_bar)")
df_column_slided["start_index_value"] = 0


if is_new_100 :
    for i in range(len(df_column_slided)):
       df_column_slided["start_index_value"].iloc[i] = df_column_slided.loc[(df_column_slided['date'] == start_index_fig_bar) & (df_column_slided['LOCATION'] == df_column_slided['LOCATION'].iloc[i])]["Value"]
    
    df_column_slided["Value2"] = df_column_slided["Value"] / df_column_slided["start_index_value"] * 100
else:
    df_column_slided["Value2"] = df_column_slided["Value"]


main_fig = px.line(df_column_slided,
                   x="date", 
                   y="Value2", 
                   color='LOCATION',
                   )
main_fig.update_traces(visible="legendonly")
st.plotly_chart(main_fig, use_container_width=True)




st.markdown('''
            제조업 중심국 : 한국(KOR), 독일(DEU), 일본(JPN) \n
            여타국 : 미국(USA), 멕시코(MEX), 인도(IND)
            ''')


st.write("OECD (2023), Industrial production (indicator). doi: 10.1787/39121c55-en (Accessed on 04 October 2023)")