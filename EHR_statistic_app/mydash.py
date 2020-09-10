import os
import dash
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from django.shortcuts import render, HttpResponse, redirect, Http404

#################################################################
def make_data(request):
#-----------------------------------------------------------------
    datatest = pd.read_csv(os.getcwd() + r'/EHR_statistic_app/testdata.csv')
    print('i need', datatest.info(null_counts=True))
    year_num = request.POST.get('year_num')
    len_data, datatest_make = data_analyse(datatest)
    datatest_make_T = pd.DataFrame(datatest_make.values.T, index=datatest_make.columns, columns=datatest_make.index)
    datatest_index = datatest_make.columns.values
    year_list = datatest[year_num].unique()
    col_list = datatest_make.index.values
    constancy = distributions(datatest_make)
#-----------------------------------------------------------------
    app = DjangoDash('Chart1')
#-----------------------------------------------------------------
    app.layout = html.Div([
        ###
        html.Div([
            html.Div([
                dcc.RadioItems(
                    id='year_list',
                    options=[{'label': i, 'value': i} for i in year_list],
                    value=year_list[0],
                    labelStyle={'display': 'inline-block'}
                ),
                dcc.RadioItems(
                    id='sort_data',
                    options=[{'label': i, 'value': i} for i in datatest_index],
                    value='distinct',
                    labelStyle={'display': 'inline-block'}
                ),
                dcc.RadioItems(
                    id='sort_type',
                    options=[{'label': i, 'value': i} for i in ['asc', 'desc']],
                    value='asc',
                    labelStyle={'display': 'inline-block'}
                )
            ], style={'width': '50%', 'float': 'center', 'display': 'inline-block'}),
        ]),
        html.Div([
            dcc.Graph(
                id='fig1',
            ),
        ], style={'display': 'inline-block'}),
        html.Div([
            dcc.Graph(
                id='fig2',
            ),
        ], style={'display': 'inline-block', 'width': '20%'}),
        html.Div([
            dcc.Graph(
                id='fig3',
            ),
        ], style={'display': 'inline-block', 'width': '20%'}),
        html.Div([
            dcc.Graph(
                id='fig4',
            ),
        ], style={'display': 'inline-block', 'width': '20%'}),
        html.Div([
            dcc.Graph(
                id='fig5',
            ),
        ], style={'display': 'inline-block', 'width': '100%'}),
        html.Div([
            dcc.RadioItems(
                id='constancy_type',
                options=[{'label': i, 'value': i} for i in ['Line','Bar']],
                value='Line',
                labelStyle={'display': 'inline-block'}
            )]
        ),
        html.Div([
            dcc.Graph(
                id='fig_constancy',
            ),
        ], style={'display': 'inline-block', 'width': '50%'}),
        ###
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='chart_T_1',
                    options=[{'label': i, 'value': i} for i in col_list],
                    value=''
                ),
            ], style={'width': '50%', 'float': 'center', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='chart_T_2',
                    options=[{'label': i, 'value': i} for i in col_list],
                    value=''
                ),
            ], style={'width': '50%', 'float': 'center', 'display': 'inline-block'}),
            html.Div([
                dcc.RadioItems(
                    id='chart_T_type',
                    options=[{'label': i, 'value': i} for i in ['Line','Bar']],
                    value='Bar',
                    labelStyle={'display': 'inline-block'}
                ),
                dcc.RadioItems(
                    id='chart_T_sort',
                    options=[{'label': i, 'value': i} for i in ['asc', 'desc']],
                    value='asc',
                    labelStyle={'display': 'inline-block'}
                )
            ], style={'width': '50%', 'float': 'center', 'display': 'inline-block'}),
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),
        html.Div([
            dcc.Graph(
                id='mini_line_T_1'
            ),
            dcc.Graph(
                id='mini_line_T_1_box'
            ),
        ], style={'display': 'inline-block', 'width': '50%'}),
        html.Div([
            dcc.Graph(
                id='mini_line_T_2'
            ),
            dcc.Graph(
                id='mini_line_T_2_box'
            ),
        ], style={'display': 'inline-block', 'width': '50%'}),
        ###
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='chart1',
                    options=[{'label': i, 'value': i} for i in ['distinct','row_len','null_len','unique','value_length']],
                    value=''
                ),
            ], style={'width': '50%', 'float': 'center', 'display': 'inline-block'}),
            html.Div([
                dcc.Dropdown(
                    id='chart2',
                    options=[{'label': i, 'value': i} for i in ['distinct','row_len','null_len','unique','value_length']],
                    value=''
                ),
            ], style={'width': '50%', 'float': 'center', 'display': 'inline-block'}),
            html.Div([
                dcc.RadioItems(
                    id='chart_mini_type',
                    options=[{'label': i, 'value': i} for i in ['Line','Bar', 'Box']],
                    value='Bar',
                    labelStyle={'display': 'inline-block'}
                ),
                dcc.RadioItems(
                    id='chart_mini_sort',
                    options=[{'label': i, 'value': i} for i in ['asc', 'desc']],
                    value='asc',
                    labelStyle={'display': 'inline-block'}
                )
            ], style={'width': '50%', 'float': 'center', 'display': 'inline-block'}),
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),
        html.Div([
            dcc.Graph(
                id='mini_line1'
            ),
        ], style={'display': 'inline-block', 'width': '50%'}),
        html.Div([
            dcc.Graph(
                id='mini_line2'
            ),
        ], style={'display': 'inline-block', 'width': '50%'})
    ])
#-----------------------------------------------------------------
    def update_chart1(df):
        '''更新图表'''
        fig1 = px.bar(df,x='distinct',orientation = 'h',barmode='group')
        fig1.update_xaxes(visible=False, fixedrange=True)

        # fig1.update_yaxes(visible=True, fixedrange=True, secondary_y=False)
        fig1.update_layout(overwrite=True)
        fig1.add_annotation(
            x=0.5, y=1, xanchor='left', yanchor='bottom', xref='paper', yref='paper', showarrow=False, text='distinct'
        )
        fig1.update_layout(                                  # strip down the rest of the plot
            showlegend=True,
            plot_bgcolor="white",
            # height=500,
            width=600
            # margin=dict(t=10,l=10,b=10,r=10)
        )
        fig1.write_image("./fig1.pdf")
        return fig1
    def update_chart2(df):
        fig2 = px.bar(df, x='row_len', orientation = 'h', barmode="group")
        fig2.update_xaxes(visible=False, fixedrange=True)
        fig2.update_yaxes(visible=False, fixedrange=True)
        fig2.update_layout(annotations=[], overwrite=True)
        fig2.add_annotation(
            x=0.5, y=1, xanchor='left', yanchor='bottom', xref='paper', yref='paper', showarrow=False, text='num-rows'
        )
        fig2.update_layout(                                  # strip down the rest of the plot
            showlegend=True,
            plot_bgcolor="white",
            # height=500,
            # width=300
            # margin=dict(t=10,l=10,b=10,r=10)
        )
        fig2.write_image("./fig2.pdf")
        return fig2
    def update_chart3(df):
        fig3 = px.bar(df, x='null_len', orientation = 'h', barmode="group")
        fig3.update_xaxes(visible=False, fixedrange=True)
        fig3.update_yaxes(visible=False, fixedrange=True)
        fig3.update_layout(overwrite=True)
        fig3.add_annotation(
            x=0.5, y=1, xanchor='left', yanchor='bottom', xref='paper', yref='paper', showarrow=False, text='null values'
        )
        fig3.update_layout(                                  # strip down the rest of the plot
            showlegend=True,
            plot_bgcolor="white",
            # height=500,
            # width=300
            # margin=dict(t=10,l=10,b=10,r=10)
        )
        fig3.write_image("./fig3.pdf")
        return fig3
    def update_chart4(df):
        fig4 = px.bar(df, x='unique', orientation = 'h', barmode="group")
        fig4.update_xaxes(visible=False, fixedrange=True)
        fig4.update_yaxes(visible=False, fixedrange=True)
        fig4.update_layout(overwrite=True)
        fig4.add_annotation(
            x=0.5, y=1, xanchor='left', yanchor='bottom', xref='paper', yref='paper', showarrow=False, text='uniqueness'
        )
        fig4.update_layout(                                  # strip down the rest of the plot
            showlegend=True,
            plot_bgcolor="white",
            # height=500,
            # width=300
            # margin=dict(t=10,l=10,b=10,r=10)
        )
        fig4.write_image("./fig4.pdf")
        return fig4
    def update_chart5(len_data):
        fig5 = px.box(len_data, x='len', y='name')
        fig5.update_xaxes(visible=False, fixedrange=True)
        # fig5.update_yaxes(visible=False, fixedrange=True)
        fig5.update_layout(overwrite=True)
        fig5.add_annotation(
            x=0.5, y=1, xanchor='left', yanchor='bottom', xref='paper', yref='paper', showarrow=False, text='value length'
        )
        fig5.update_layout(                                  # strip down the rest of the plot
            showlegend=True,
            plot_bgcolor="white",
            # height=600,
            # width=800
            # margin=dict(t=10,l=10,b=10,r=10)
        )
        fig5.write_image("./fig5.pdf")
        return fig5
    def update_chart6(constancy_type):
        if constancy_type == 'Bar':
            fig_constancy = px.bar(y=constancy, x=datatest_make.columns.values, barmode="group")
        elif constancy_type == 'Line':
            fig_constancy = px.line(y=constancy, x=datatest_make.columns.values)
        # fig_constancy.update_xaxes(visible=False, fixedrange=True)
        # fig_constancy.update_yaxes(visible=False, fixedrange=True)
        fig_constancy.update_layout(overwrite=True)
        fig_constancy.add_annotation(
            x=0.5, y=1, xanchor='left', yanchor='bottom', xref='paper', yref='paper', showarrow=False, text='distributions-constancy'
        )
        fig_constancy.update_layout(                                  # strip down the rest of the plot
            showlegend=True,
            plot_bgcolor="white",
            height=300,
            width=500,
            # margin=dict(t=10,l=10,b=10,r=10)
        )
        fig_constancy.write_image("./fig_constancy.pdf")
        return fig_constancy

    def update_chart_T(df, chart, chart_T_type):
        '''更新图表'''
        if chart_T_type == 'Line':
            fig = px.line(df, y=chart,x=df.index, height=200, width=1024)
        elif chart_T_type == 'Bar':
            fig = px.bar(df, x=chart,y=df.index ,orientation = 'h', barmode="group")
        fig.update_xaxes(visible=False, fixedrange=True)
        # fig.update_yaxes(visible=False, fixedrange=True)
        fig.update_layout(
            annotations=[],                                 # remove facet/subplot labels
            overwrite=True,
            showlegend=True,                                # strip down the rest of the plot
            plot_bgcolor="white",
            height=300,
            # width=450,
            # margin=dict(t=10,l=10,b=10,r=10)
        )
        fig.write_image("./fig_chart_T.pdf")
        return fig

    def update_chart_T_box(len_data):
        '''更新图表'''
        fig = px.box(len_data, x='len', y='name')
        # fig.update_xaxes(visible=False, fixedrange=True)
        # fig.update_yaxes(visible=False, fixedrange=True)
        fig.update_layout(
            annotations=[],                                 # remove facet/subplot labels
            overwrite=True,
            showlegend=True,                                # strip down the rest of the plot
            plot_bgcolor="white",
            height=300,
            # width=450,
            # margin=dict(t=10,l=10,b=10,r=10)
        )
        fig.write_image("./fig_chart_T_box.pdf")
        return fig


    def update_chart(df, chart, chart_mini_type, len_data):
        '''更新图表'''
        print('chart is:', chart)
        if chart_mini_type == 'Box':
            fig = px.box(len_data, x='len', y='name')
        elif chart_mini_type == 'Line':
            fig = px.line(df, y=chart,x=df.index, height=200, width=1024)
        elif chart_mini_type == 'Bar':
            fig = px.bar(df, x=chart,y=df.index ,orientation = 'h', barmode="group")
        fig.update_xaxes(visible=False, fixedrange=True)
        # fig.update_yaxes(visible=False, fixedrange=True)
        fig.update_layout(
            annotations=[],                                 # remove facet/subplot labels
            overwrite=True,
            showlegend=True,                                # strip down the rest of the plot
            plot_bgcolor="white",
            height=500,
            # width=450,
            margin=dict(t=10,l=10,b=10,r=10)
        )
        fig.write_image("./fig_mini_line.pdf")
        return fig
#-----------------------------------------------------------------
    @app.callback(
        Output('fig1', 'figure'),
        [Input('sort_type', 'value'),
        Input('sort_data', 'value'),
        Input('year_list', 'value')]
        )
    def update_chart_select(sort_type, sort_data, year):
        '''更新图表'''
        len_data, datatest_make = data_analyse(datatest[datatest[year_num] == int(year)])
        if sort_type == 'asc':
            datatest_make_sort = datatest_make.sort_values(by=sort_data, ascending = True,inplace = False)
        elif sort_type == 'desc':
            datatest_make_sort = datatest_make.sort_values(by=sort_data, ascending = False,inplace = False)
        return update_chart1(datatest_make_sort)

    @app.callback(
        Output('fig2', 'figure'),
        [Input('sort_type', 'value'),
        Input('sort_data', 'value'),
        Input('year_list', 'value')]
        )
    def update_chart_select(sort_type, sort_data, year):
        '''更新图表'''
        len_data, datatest_make = data_analyse(datatest[datatest[year_num] == int(year)])
        if sort_type == 'asc':
            datatest_make_sort = datatest_make.sort_values(by=sort_data, ascending = True,inplace = False)
        elif sort_type == 'desc':
            datatest_make_sort = datatest_make.sort_values(by=sort_data, ascending = False,inplace = False)
        return update_chart2(datatest_make_sort)

    @app.callback(
        Output('fig3', 'figure'),
        [Input('sort_type', 'value'),
        Input('sort_data', 'value'),
        Input('year_list', 'value')]
        )
    def update_chart_select(sort_type, sort_data, year):
        '''更新图表'''
        len_data, datatest_make = data_analyse(datatest[datatest[year_num] == int(year)])
        if sort_type == 'asc':
            datatest_make_sort = datatest_make.sort_values(by=sort_data, ascending = True,inplace = False)
        elif sort_type == 'desc':
            datatest_make_sort = datatest_make.sort_values(by=sort_data, ascending = False,inplace = False)
        return update_chart3(datatest_make_sort)

    @app.callback(
        Output('fig4', 'figure'),
        [Input('sort_type', 'value'),
        Input('sort_data', 'value'),
        Input('year_list', 'value')]
        )
    def update_chart_select(sort_type, sort_data, year):
        '''更新图表'''
        len_data, datatest_make = data_analyse(datatest[datatest[year_num] == int(year)])
        if sort_type == 'asc':
            datatest_make_sort = datatest_make.sort_values(by=sort_data, ascending = True,inplace = False)
        elif sort_type == 'desc':
            datatest_make_sort = datatest_make.sort_values(by=sort_data, ascending = False,inplace = False)
        return update_chart4(datatest_make_sort)

    @app.callback(
        Output('fig5', 'figure'),
        [Input('year_list', 'value')]
        )
    def update_chart_select(year):
        '''更新图表'''
        len_data, datatest_make = data_analyse(datatest[datatest[year_num] == int(year)])
        return update_chart5(len_data)

    @app.callback(
        Output('mini_line_T_1', 'figure'),
        [Input('chart_T_1', 'value'),
        Input('chart_T_type', 'value'),
        Input('chart_T_sort', 'value')]
        )
    def update_chart_select(chart, chart_T_type, chart_T_sort):
        '''更新图表'''
        if chart_T_sort == 'asc':
            datatest_make_T_sort = datatest_make_T.sort_values(by=chart, ascending = True,inplace = False)
        elif chart_T_sort == 'desc':
            datatest_make_T_sort = datatest_make_T.sort_values(by=chart, ascending = False,inplace = False)
        return update_chart_T(datatest_make_T_sort, chart, chart_T_type)

    @app.callback(
        Output('mini_line_T_1_box', 'figure'),
        [Input('chart_T_1', 'value')]
        )
    def update_chart_select(chart):
        '''更新图表'''
        return update_chart_T_box(len_data[len_data['name']==chart])

    @app.callback(
        Output('mini_line_T_2', 'figure'),
        [Input('chart_T_2', 'value'),
        Input('chart_T_type', 'value'),
        Input('chart_T_sort', 'value')]
        )
    def update_chart_select(chart, chart_T_type, chart_T_sort):
        '''更新图表'''
        if chart_T_sort == 'asc':
            datatest_make_T_sort = datatest_make_T.sort_values(by=chart, ascending = True,inplace = False)
        elif chart_T_sort == 'desc':
            datatest_make_T_sort = datatest_make_T.sort_values(by=chart, ascending = False,inplace = False)
        return update_chart_T(datatest_make_T_sort, chart, chart_T_type)

    @app.callback(
        Output('mini_line_T_2_box', 'figure'),
        [Input('chart_T_2', 'value')]
        )
    def update_chart_select(chart):
        '''更新图表'''
        return update_chart_T_box(len_data[len_data['name']==chart])

    @app.callback(
        Output('mini_line1', 'figure'),
        [Input('chart1', 'value'),
        Input('chart_mini_type', 'value'),
        Input('chart_mini_sort', 'value')]
        )
    def update_chart_select(chart, chart_mini_type, chart_mini_sort):
        '''更新图表'''
        if chart_mini_type != 'Box' and chart != 'value_length':
            if chart_mini_sort == 'asc':
                datatest_make_sort = datatest_make.sort_values(by=chart, ascending = True,inplace = False)
            elif chart_mini_sort == 'desc':
                datatest_make_sort = datatest_make.sort_values(by=chart, ascending = False,inplace = False)
            len_data = ''
        else:
            len_data, datatest_make_sort = data_analyse(datatest)
        return update_chart(datatest_make_sort, chart, chart_mini_type, len_data)

    @app.callback(
        Output('mini_line2', 'figure'),
        [Input('chart2', 'value'),
        Input('chart_mini_type', 'value'),
        Input('chart_mini_sort', 'value')]
        )
    def update_chart_select(chart, chart_mini_type, chart_mini_sort):
        '''更新图表'''
        if chart_mini_type != 'Box' and chart != 'value_length':
            if chart_mini_sort == 'asc':
                datatest_make_sort = datatest_make.sort_values(by=chart, ascending = True,inplace = False)
            elif chart_mini_sort == 'desc':
                datatest_make_sort = datatest_make.sort_values(by=chart, ascending = False,inplace = False)
            len_data = ''
        else:
            len_data, datatest_make_sort = data_analyse(datatest)
        return update_chart(datatest_make_sort, chart, chart_mini_type, len_data)


    @app.callback(
        Output('fig_constancy', 'figure'),
        [Input('constancy_type', 'value')]
        )
    def update_chart_select(constancy_type):
        '''更新图表'''
        return update_chart6(constancy_type)
#-----------------------------------------------------------------
    return render(request, 'make_data.html', locals())

#################################################################
def datagrid(request):
    try:
        datatest = pd.read_csv(os.getcwd() + r'/EHR_statistic_app/testdata.csv', error_bad_lines=False, lineterminator="\n")
    except:
        datatest = pd.read_csv(os.getcwd() + r'/EHR_statistic_app/testdata.csv', error_bad_lines=False, lineterminator="\n")
    else:
        datatest = pd.read_csv(os.getcwd() + r'/EHR_statistic_app/testdata.csv', error_bad_lines=False, lineterminator="\n")
    list = datatest.to_dict(orient='records')
    year_list = datatest.columns.values
    if request.method=="POST":
        try:
            handle_upload_file(request.FILES['file'])
        except:
            return HttpResponse('Defeat. Please back up.')
        else:
            return redirect(to='../datagrid')#此处简单返回一个成功的消息，在实际应用中可以返回到指定的页面中
    return render(request, 'datagrid.html', locals())

#################################################################
def data_analyse(datatest):
    len_list = []
    for i in datatest.columns.values:
        for l in datatest[i]:
            list_res = []
            list_res.append(i)
            list_res.append(len(str(l)))
            len_list.append(list_res)
    len_data = pd.DataFrame(len_list, columns=['name','len'])
    datatest_make = pd.DataFrame(index=datatest.columns.values)
    distinct_res = []
    row_len_res = []
    null_len_res = []
    unique_res = []
    for i in datatest.columns.values:
        distinct_res.append(len(datatest[i].value_counts()))
        row_len_res.append(len(datatest[i]))
        unique_res.append(np.sum((datatest[i].value_counts().values == 1) !=0))
    datatest_make['distinct'] = distinct_res
    datatest_make['row_len'] = row_len_res
    datatest_make['null_len'] = datatest.isnull().sum(axis=0).values
    datatest_make['unique'] = unique_res
    return len_data, datatest_make

def distributions(datatest_make):
    constancy = []
    length = len(datatest_make)
    for i in datatest_make.columns.values:
        res_list = datatest_make[i].value_counts().sort_values(ascending = False,inplace = False).values.tolist()
        if res_list:
            constancy.append(res_list[0]/length)
        else:
            constancy.append(0)
    return constancy

def handle_upload_file(file):
    path=os.getcwd() + r'/EHR_statistic_app/testdata.csv'     #上传文件的保存路径，可以自己指定任意的路径
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path,'wb+')as destination:
        for chunk in file.chunks():
            destination.write(chunk)
