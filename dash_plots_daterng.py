from data_by_daterng import VolByDateRange, SS_DENSITY, MCO_DENSITY
from dash import Dash, Input, Output, html, dcc
from datetime import date
import plotly.express as px
from datetime import datetime, timedelta, date
import pytz

def get_plots():
    app = Dash()

    app.layout = html.Div([html.Div([html.Br(), html.Div(html.H1('Volume Comparison', style={"textAlign": "center"})),
                        html.Div([html.Label("Date : ", className='label'), dcc.DatePickerRange(id='ddate', className='cal',  min_date_allowed=date(2000, 1,1) , stay_open_on_select=True, start_date = date(2022,2,1), end_date=date(2022,2,3), max_date_allowed=datetime.now(pytz.timezone('America/Los_Angeles')).date(), initial_visible_month=date(2022, 2, 1))]),
                        html.Br(),
                        html.Div([html.Label('Unit : ', className='label'), dcc.RadioItems(id='dunit', options=[{'label': 'Cubic Meter', 'value': 'CM'}, {'label': 'Metric Ton', 'value': 'MT'}], value='CM', className='label')])]),
                        html.Div(dcc.Graph(id='ss_gr'), className='divpadd'), html.Br(), html.Div(dcc.Graph(id='mco_gr'), className='divpadd')], style={"position": "realtive"})


    # most effective 
    @app.callback(Output('ddate','start_date'), Output('ddate', 'end_date'), Input('ddate', 'start_date'), Input('ddate', 'end_date'))
    def set_dates(sdate, edate):
        sdate = datetime.fromisoformat(sdate)
        edate = datetime.fromisoformat(edate)
        if (sdate.date() == datetime.now(pytz.timezone('America/Los_Angeles')).date()):
            edate = sdate
            sdate = sdate - timedelta(days=2)
        sel_days = (edate - sdate).days

        if sel_days <= 2 and sel_days >= 0:
            sdate = sdate
            edate = edate
        else:
            sdate = sdate
            edate = sdate

        return sdate, edate
    
    @app.callback(Output('ss_gr', 'figure'), Output('mco_gr', 'figure'), Input('ddate', 'start_date'), Input('ddate', 'end_date'), Input('dunit', 'value'))
    def fgraphs(vdate, edate, vunit):
        df2 = VolByDateRange(vdate, edate)
        y_label = 'Volume (cubic meter)'
        color_list = ['#FB81D2', '#81A4FB', '#9BFB81']
        date_list = df2['Date'].unique()
        color_dict = {}
        for i in range(len(date_list)):
            color_dict[date_list[i]] = color_list[i]
        if vunit == 'MT':
            y_label = 'Volume (Metric Ton)'
            df2['Total Volume SS'] = df2['Total Volume SS'] * SS_DENSITY
            df2['Total Volume MCO'] = df2['Total Volume MCO'] * MCO_DENSITY
        fbar = px.bar(df2, x='Hours', y='Total Volume SS',category_orders={'Hours': df2['Hours'].to_list()}, 
                    color_discrete_map=color_dict, color='Date', title='Single Stream', text='Total Volume SS', 
                    barmode='group', labels={'Total Volume SS': y_label, 'Hours': 'Time (PST)'}, text_auto='.2f')
        fbar.update_layout(title=dict(x=0.5), xaxis={'type':'category', 'showgrid': False}, yaxis={'showgrid': False}, margin=dict(l=50, r=50, t=60, b=20), paper_bgcolor='#4F4F61', plot_bgcolor= '#4F4F61', font_color='white', title_font_color='white')
        

        fbar1 = px.bar(df2, x='Hours', y='Total Volume MCO', color='Date', category_orders={'Hours': df2['Hours'].to_list()},
                     color_discrete_map=color_dict, title='Mixed Containers', text='Total Volume MCO', barmode='group',
                      labels={'Total Volume MCO': y_label, 'Hours': 'Time (PST)'}, text_auto='.2f')
        fbar1.update_layout(title=dict(x=0.5), margin=dict(l=50, r=50, t=60, b=20), xaxis={'type':'category', 'showgrid': False}, yaxis={'showgrid': False}, font_color='white', title_font_color='white', paper_bgcolor='#4F4F61', plot_bgcolor='#4F4F61')
        

        return fbar, fbar1
    return app
