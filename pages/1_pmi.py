import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
import plotly.io as io

def bgLevels(fig, df, variable, level, mode, fillcolor, layer):
    """
    Set a specified color as background for given
    levels of a specified variable using a shape.
    
    Keyword arguments:
    ==================
    fig -- plotly figure
    variable -- column name in a pandas dataframe
    level -- int or float
    mode -- set threshold above or below
    fillcolor -- any color type that plotly can handle
    layer -- position of shape in plotly fiugre, like "below"
    
    """
    
    if mode == 'above':
        m = df[variable].gt(level)
    
    if mode == 'below':
        m = df[variable].lt(level)
        
    df1 = df[m].groupby((~m).cumsum())['date'].agg(['first','last'])

    for index, row in df1.iterrows():
        #print(row['first'], row['last'])
        fig.add_shape(type="rect",
                        xref="x",
                        yref="paper",
                        x0=row['first'],
                        y0=0,
                        x1=row['last'],
                        y1=1,
                        line=dict(color="rgba(0,0,0,0)",width=3,),
                        fillcolor=fillcolor,
                        layer=layer) 
    return(fig)


 


io.renderers.default='browser' #이거 해야 ploty 실시간 확인 가능 fig.show()가 인터넷 창에
st.set_page_config(page_title='ISM PMI',  layout='wide')

st.title("PMI")
st.header("U.S. ISM Manufacturing PMI & U.S. ISM Non-Manufacturing PMI")



data = pd.read_excel("발표 데이터.xlsx", sheet_name="showing_data")

chart_df = pd.DataFrame()
chart_df["month"] = pd.DatetimeIndex(data["date"]).month
chart_df["year"] = pd.DatetimeIndex(data["date"]).year
chart_df["date"] = pd.DatetimeIndex(data["date"]).strftime("%Y년 %m월")
chart_df["Manufacturing PMI"] = data["Manufacturing PMI"].astype("float")
chart_df["Non-Manufacturing PMI"] = data["Non-Manufacturing PMI"].astype("float")
chart_df["PMI-diff"] = chart_df["Manufacturing PMI"] - chart_df["Non-Manufacturing PMI"]
chart_df["전년 동월 대비 수출 증감률"] = data["전년 동월 대비 수출 증감률"] * 100
chart_df = chart_df.sort_values("date")


start_index_fig_bar, end_index_fig_bar = st.select_slider(
    '표를 확인할 범위를 설정하시오',
    options= chart_df["date"],
    value=(chart_df.iloc[-45]["date"], chart_df.iloc[-1]["date"] ))
check_50_under= st.checkbox(' 제조업 경기 부진 기간 표기 ( 제조업 PMI < 50 ) ')



df_column_slided = chart_df.query("(date >= @start_index_fig_bar) and (date <= @end_index_fig_bar)")




main_fig = make_subplots(specs=[[{"secondary_y": True}]])

main_fig.add_traces(
    [
     go.Scatter(x = df_column_slided["date"], 
                y = df_column_slided["Manufacturing PMI"],
                name = "Manufacturing PMI"
                ),
     go.Scatter(x = df_column_slided["date"],
                y = df_column_slided["Non-Manufacturing PMI"],
                name = "Non-Manufacturing PMI"
                ),
     ])

main_fig.add_trace(
    go.Scatter(
        x = df_column_slided["date"],
        y = df_column_slided["전년 동월 대비 수출 증감률"],
        name = "전년 동월 대비 수출 증감률"
        ),
    secondary_y=True
    )

main_fig.add_trace(
    go.Scatter(
        x = df_column_slided["date"],
        y = [50] * len(df_column_slided),
        name = "PMI 기준",
        line = dict(dash = "dot")
        ),
    )

main_fig.add_trace(
    go.Scatter(
        x = df_column_slided["date"],
        y = [0] * len(df_column_slided),
        name = "증감률 0%",
        line = dict(dash = "dot")
        ),
    secondary_y=True
    )



main_fig.add_bar(
    x = df_column_slided["date"], 
    y = df_column_slided["PMI-diff"], 
    name = "PMI-diff"
    )

# main_fig.add_shape( # add a horizontal "target" line
#    type="line", line_width=3, opacity=1, line_dash="dot",
#    x0=0, x1=1, xref="paper", y0=50, y1=50, yref="y"
#)


main_fig.update_yaxes(title_text="<b> PMI 지수 </b> (기준 : 50)", secondary_y=False)
main_fig.update_yaxes(title_text="<b> 전년동월대비 수출 증감률 </b> (단위 : %)", secondary_y=True)



if check_50_under:
    main_fig = bgLevels(main_fig, 
                   df_column_slided, 
                   "Manufacturing PMI", 
                   level = 50, 
                   mode = 'below', 
                   fillcolor = 'rgba(100,100,100,0.2)', 
                   layer ='below')

st.plotly_chart(main_fig, use_container_width=True)
