import dash
from dash import dcc,html
from dash.dependencies import Input,Output
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import mysql.connector

cnx=mysql.connector.connect(
    username='root',
    password='Lengqiu_0',
    host='localhost',
    database='origin'
)

cursor=cnx.cursor()

query='''SELECT * FROM world_gdp_ranking_2023_with_rank'''

cursor.execute(query)

data=cursor.fetchall()

cursor.close()
cnx.close()
# 读取数据
column_names=['Country', 'GDP (USD Million)', 'ISO', 'Rank']
df=pd.DataFrame(data,columns=column_names)

# 初始化dash
app=dash.Dash(__name__)

# 设置布局
app.layout=html.Div([
    # 地图组件
    dcc.Graph(id='world-map'),
    # 显示GDP排名组件
    html.Div(
        id='country-gdp-rank',
        className='country-gdp-rank'
        )
])

# 更新回调
@app.callback(
    Output('world-map','figure'),
    [Input('world-map','clickData')])

def update_map(clickData):
    # 创建地图
    fig=px.choropleth(df,locations='ISO',hover_name="Country",color='Rank',projection='natural earth')
    return fig

# 显示GDP排名回调
@app.callback(
    Output("country-gdp-rank","children"),
    [Input('world-map','clickData')])

def display_gdp_rank(clickData):
    # 用户点击地图上国家显示GDP排名
    if clickData is not None:
        country_iso=clickData['points'][0]['location']
        rank = df[df['ISO'] == country_iso]['Rank'].iloc[0]
        country_name=df[df['ISO']==country_iso]['Country'].iloc[0]
        return f'{country_name}GDP排名:{rank}'
    else:
        return '点击一个国家查看GDP排名'

# 运行服务器
if __name__ == '__main__':
    app.run_server(debug=True)