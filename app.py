import pandas as pd
import numpy as np
import dash
from dash import html 
from dash import dcc
import plotly.graph_objects as go
from dash.dependencies import Input ,Output
import dash_bootstrap_components as dbc
import plotly_express as px
from plotly.subplots import make_subplots
from dash import dcc, html, callback, Output
# load the data ------------------------------------------------------------------------
df=pd.read_excel('unemplo_figures_1991.xlsx')

YEARS=[2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
       2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021,
       1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999]
# set the layout for the application----------------------------------------------
app=dash.Dash(external_stylesheets=[dbc.themes.CYBORG],meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],suppress_callback_exceptions=True)
server=app.server
app.layout=dbc.Container([
                dbc.Row(dbc.Col(html.H3("Unemployement Rate Worldwide Since 1991",className='text-center mb-4'),width=12)),
                dbc.Row( html.Marquee("Unemployment Rates Worldwide Since 1991 -Bahageel Dashboard-Data Compiled from World Bank "), style = {'color':'cyan'}), 
                dbc.Row([dbc.Col([html.H6(['Choose Years to view Unemployment Rate :']),]),
                                      html.Div(dcc.RangeSlider(id='yearslider',
                                                 marks={str(year):{'label':str(year),'style':{"color": "#7fafdf"},} for year in YEARS},
                                                        step=1
                                                        ,
                                                 min=min(YEARS),
                                                 max=max(YEARS),
                                                 value=[2010,2020],
                                                 dots=True, 
                                                 allowCross=False, 
                                                 disabled=False, 
                                                 pushable=2, updatemode='drag', 
                                                 included=True,vertical=False,
                                                 verticalHeight=900, className='None', 
                                                 tooltip={'always_visible':False, 'placement':'bottom'}),

                                                 style={'width':'95%'})]),
              dbc.Row([dbc.Col([dcc.Graph(id="map",figure={})]),dbc.Col(html.Div(id='show_data'))]),
             
              


              ]),

              
                                                 
                                                                                        
                                                                                       

# the call back functions------------------------------------------------------------------------------------------------------------------------------------------------------
@app.callback(
    Output('map','figure'),
    Input('yearslider','value')
)
def update_map(years):
    year_0 ,year_1=years
    filtered_df=df[(df['Year']>=year_0)&(df['Year']<=year_1)]
    fig1=px.choropleth(filtered_df,locations='Countrycode',hover_data=['Unemployment','Country'],color='Unemployment',
                  hover_name='Country', color_continuous_scale=px.colors.sequential.Plasma,projection='orthographic')
    fig1.update_layout(plot_bgcolor='#000000',paper_bgcolor='#000000', height=600,margin=dict(l=0,r=0,t=0,b=0) ,geo=dict(bgcolor= '#000000'), )
    fig1.layout.template='plotly_dark'
    return fig1
@app.callback(
    Output('show_data','children'),
    [Input('map','clickData')],
    Input('yearslider','value')

)
def update_line_chart(clickdata,years):
    if clickdata:
        df['AnnualChange']=df['Unemployment']/df['Unemployment'].shift()-1
        df.dropna(inplace=True)
        points=clickdata['points'][0]['location']
        year_0,year_1=years
        filtered_df=df[(df['Year']>=year_0)&(df['Year']<=year_1)]
        filtered_df=filtered_df[filtered_df['Countrycode']==points]
        filtered_df["Color"] = np.where(filtered_df["AnnualChange"]<0, 'green', 'red')
        clickedcountry=filtered_df.Country.unique()[0]
        fig4=make_subplots(rows=2,cols=1,shared_xaxes=True,shared_yaxes=False ,vertical_spacing=0.02,
                        y_title='Changes      Unemployment Rate',
                        row_heights=[0.7,0.3] )

        fig4.layout.template="plotly_dark"

        fig4.add_trace(go.Scatter(x=filtered_df['Year'],y=filtered_df['Unemployment'],line=dict(color='#00FFFF'),line_shape='spline',fill='tonexty' ,fillcolor='rgba(0,255,255,0.1)',name="unemployment Rate",mode='lines'),row=1,col=1,secondary_y=False)

        fig4.add_trace(go.Bar( x=filtered_df['Year'],y=filtered_df['AnnualChange'],marker_color=filtered_df['Color'],name='change%'),row=2,col=1,secondary_y=False)
        fig4.update_layout(title=f"Unemployment Rate in {clickedcountry}  Since {year_0}",xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),
                        hovermode='x unified', plot_bgcolor='#000000',paper_bgcolor='#000000' ,showlegend=False,height=600)
        fig4.update_traces(xaxis='x2' )
        return dcc.Graph(figure=fig4)
    else:
        df['AnnualChange']=df['Unemployment']/df['Unemployment'].shift()-1
        df.dropna(inplace=True)
        year_0,year_1=years
        filtered_df2=df[(df['Year']>=year_0)&(df['Year']<=year_1)]
        filtered_df2=filtered_df2[filtered_df2['Country']=='Africa Eastern and Southern']
        filtered_df2["Color"] = np.where(filtered_df2["AnnualChange"]<0, 'green', 'red')
        fig5=make_subplots(rows=2,cols=1,shared_xaxes=True,shared_yaxes=False ,vertical_spacing=0.02,
                        y_title='Changes      Unemployment Rate',
                        row_heights=[0.7,0.3] )

        fig5.layout.template="plotly_dark"

        fig5.add_trace(go.Scatter(x=filtered_df2['Year'],y=filtered_df2['Unemployment'],line=dict(color='#00FFFF'),line_shape='spline',fill='tonexty' ,fillcolor='rgba(0,255,255,0.1)',name="unemployment Rate",mode='lines'),row=1,col=1,secondary_y=False)

        fig5.add_trace(go.Bar( x=filtered_df2['Year'],y=filtered_df2['AnnualChange'],marker_color=filtered_df2['Color'],name='change%'),row=2,col=1,secondary_y=False)
        fig5.update_layout(title=f"Unemployment Rate in Africa Eastern and Southern Since {year_0}",xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),
                        hovermode='x unified', plot_bgcolor='#000000',paper_bgcolor='#000000' ,showlegend=False)
        fig5.update_traces(xaxis='x2' )
        return dcc.Graph(figure=fig5)


        


if __name__=='__main__':
    app.run_server(debug=True, port=8000)
    
         