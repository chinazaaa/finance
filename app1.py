
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.offline as pyo
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import dash_table

app = dash.Dash()
server = app.server 
df2 = pd.read_csv('contents2.csv')
df3 = pd.read_csv('contents3.csv')
df4 = pd.read_csv('contents4.csv')
df = pd.read_csv('finance.csv')
np.random.seed(56)
x_values = np.linspace(0,1,100)
y_values = np.random.randn(100)

colors = {'background': '#111111', 'text': '#7FDBFF'}
app.layout = html.Div([html.Div(
    [
     
     html.Div([
        html.H3('This is a Bar Chart showing the todays close and symbols for the top 5 advancers',style={'textAlign':'center','color':colors['text']}),
        dcc.Graph(id='g3', figure={'data': [go.Bar(x = df2['SYMBOL'],y = df2['TODAYS_CLOSE'])],
        'layout': {'plot_bgcolor':colors['background'],'paper_bgcolor':colors['background'],
                   'font':{'color':colors['text']},'title': 'Top 5 Advancers'}})],className="six columns"),
     
     html.Div([
        html.H3('This is a Line Chart showing the todays close and symbols for the top 5 advancers',style={'textAlign':'center','color':colors['text']}),
        dcc.Graph(id='g4', figure={'data': [go.Scatter(x = df2['SYMBOL'],y = df2['TODAYS_CLOSE'],mode='lines',name='mylines')],
        'layout': {'plot_bgcolor':colors['background'],'paper_bgcolor':colors['background'],
                   'font':{'color':colors['text']},'title': 'Top 5 Advancers'}})],className="six columns"),
      html.Div([
        html.H3('This is a Bar Chart showing the todays close and symbols for the top 5 Decliners',style={'textAlign':'center','color':colors['text']}),
        dcc.Graph(id='g5', figure={'data': [go.Bar(x = df3['SYMBOL'],y = df3['TODAYS_CLOSE'])],
        'layout': {'plot_bgcolor':colors['background'],'paper_bgcolor':colors['background'],
                   'font':{'color':colors['text']},'title': 'Top 5 Decliners'}})],className="six columns"),
      html.Div([
        html.H3('This is a Line Chart showing the todays close and symbols for the top 5 Decliners',style={'textAlign':'center','color':colors['text']}),
        dcc.Graph(id='g6', figure={'data': [go.Scatter(x = df3['SYMBOL'],y = df3['TODAYS_CLOSE'],mode='lines',name='mylines')],
        'layout': {'plot_bgcolor':colors['background'],'paper_bgcolor':colors['background'],
                   'font':{'color':colors['text']},'title': 'Top 5 Decliners!'}})],className="six columns"),
      html.Div([
        html.H3('This is a Bar Chart showing the value and symbols for the top 5 Trades',style={'textAlign':'center','color':colors['text']}),
        dcc.Graph(id='g7', figure={'data': [go.Bar(x = df4['SYMBOL'],y = df4['VALUE'])],
        'layout': {'plot_bgcolor':colors['background'],'paper_bgcolor':colors['background'],
                   'font':{'color':colors['text']},'title': 'Top 5 Trades'}})],className="six columns"),
      html.Div([
        html.H3('This is a Line Chart showing the value and symbols for the top 5 Trades',style={'textAlign':'center','color':colors['text']}),
        dcc.Graph(id='g8', figure={'data': [go.Scatter(x = df4['SYMBOL'],y = df4['VALUE'],mode='lines',name='mylines')],
        'layout': {'plot_bgcolor':colors['background'],'paper_bgcolor':colors['background'],
                   'font':{'color':colors['text']},'title': 'Top 5 Trades'}})],className="six columns"),
     html.Div([
        html.H3('This is a Line Chart showing different values',style={'textAlign':'center','color':colors['text']}),
        dcc.Graph(id='g11', figure={'data': [go.Scatter( x=x_values,y=y_values+5,mode='lines',name='mylines')],
        'layout': {'plot_bgcolor':colors['background'],'paper_bgcolor':colors['background'],
                   'font':{'color':colors['text']},'title': 'A line chart'}})],className="six columns"),
     
      html.Div([
        html.H3('This is a Bar Chart showing the companies name and prices',style={'textAlign':'center','color':colors['text']}),
        dcc.Graph(id='g9', figure={'data': [go.Bar(x = df5['Name'],y = df5['Price'])],
        'layout': {'plot_bgcolor':colors['background'],'paper_bgcolor':colors['background'],
                   'font':{'color':colors['text']},'title': 'Companies and their Prices'}})],className="six columns"),
     
        html.Div([html.H3('This is a Line Chart showing the companies name and prices', style={'textAlign':'center','color':colors['text']}),
        dcc.Graph(id='g10', figure={'data': [go.Scatter(x = df['Name'],y = df['Price'],mode='lines',name='mylines')],'layout':{
        'plot_bgcolor':colors['background'],
        'paper_bgcolor':colors['background'],
        'font':{'color':colors['text']},
        'title': 'Companies and their Prices'
    }})], className="six columns")], className="row"),
                       dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        row_selectable="multi",
        row_deletable=True,
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
    ),
    html.Div(id='datatable-interactivity-container')
])


@app.callback(
    Output('datatable-interactivity-container', "children"),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows")])
def update_graphs(rows, derived_virtual_selected_rows):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncracy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff["NAME"],
                        "y": dff[column],
                        "type": "line",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in ["Symbol","Price","changes","changess","Volume","Avg_Vol","Market_Cap","PE_Ratio"] if column in dff
    
    ]

if __name__ == '__main__':
    app.run_server()

