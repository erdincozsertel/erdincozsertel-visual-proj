import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
#import reverse_geocoder as rg



from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "NYC Taxi Data"

colors = {
    'background': '#6F884C',
    'text': '#131311'
}


df = pd.read_csv("updated.csv")

mapbox_access_token = 'pk.eyJ1IjoiZXJkaW5jb3pzZXJ0ZWwiLCJhIjoiY2s0eTNpNm9mMDZ1YzNmbDVycDh6MWV5dSJ9.h737qMnBPYg0pSJlSlu0JQ'





df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
df['pickup_hours'] = df['tpep_pickup_datetime'].dt.hour
df['pickup_minutes'] = df['tpep_pickup_datetime'].dt.minute



df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
df['dropoff_hours'] = df['tpep_dropoff_datetime'].dt.hour
df['dropoff_minutes'] = df['tpep_dropoff_datetime'].dt.minute



# pLat=df['pickup_latitude'].values.tolist()
# pLong=df['pickup_longitude'].values.tolist()

# pDCor=[]

# dfsize = (df.size).astype(int)-1
# #dfsize = df.size.to_datetime


# for i in range(dfsize):
#     pDCoor = (pLat[i], pLong[i])
#     pDCor.append(pDCoor)

# pDNames = rg.search(pDCor)

# for i in range(dfsize):
#     pDName = (pDNames[i])['name']
#     pDNames[i]=pDName    

# df['pickup_district']=pDNames


# dLat=df['dropoff_latitude']
# dLong=df['dropoff_longitude']

# dDCor=[]

# for i in range(dfsize):
#     dDCoor = (dLat[i], dLong[i])
#     dDCor.append(dDCoor)

# dDNames = rg.search(dDCor)

# for i in range(dfsize):
#     dDName = (dDNames[i])['name']
#     dDNames[i]=dDName

# df['dropoff_district']=dDNames



dfOriginal = df

dfMap = dfOriginal


### Graph 1: All (Vendor 1+Vendeor 2 by defult) pickup/dropoff by hour
### Style: Bar
### Parameter: Vendor A and/or Vendor B
### Chose: Hour

dfGraph1 = dfOriginal


### Graph 2: (All hours defult)Income per Vendor by district
### Style: Line
### Parameter: Hour
### Chose: Vendor

dfGraph2 = dfOriginal

layout_table = dict(
    autosize=True,
    height=500,
    font=dict(color="#383738"),
    titlefont=dict(color="#2C2C2C", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    legend=dict(font=dict(size=10), orientation='h'),
)
layout_table['font-size'] = '12'
layout_table['margin-top'] = '20'

layout_map = dict(
    autosize=True,
    height=500,
    mode='marker',
    marker=dict(size=5),
    font=dict(color="#383738"),
    titlefont=dict(color="#2C2C2C", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    legend=dict(font=dict(size=10), orientation='h'),
    title='New York City Pickup Locations',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-73.91251,
            lat=40.7342
        ),
        zoom=10,
    )
)

xData1 = []
yData1 = []

for group, data in df.groupby(['dropoff_hours']):
    xData1.append(str(group) + ":" + "00")
    yData1.append(data['total_amount'].sum())

  
trace_pickup = go.Scattermapbox(
        lat= df['pickup_latitude'],
        lon= df['pickup_longitude'],
		mode= "markers",
        marker= dict(size=6, color='#51884C', opacity=0.7),
        hoverinfo= "text",
        hovertext= [["PassengerCount: {} <br>Pickup Time: {} <br>Vendor: {}<br>Price: {}".format(i,j,k,l)]
        for i,j,k,l in zip(dfOriginal['passenger_count'].apply(str), dfOriginal['pickup_hours'].apply(str)+" : "+dfOriginal['pickup_minutes'].apply(str),dfOriginal['VendorID'].apply(str),dfOriginal['total_amount'].apply(str))],
        #layout = layout_map,

  )
data = [trace_pickup]

	

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='NYC Taxi Data',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    #map head
    html.Div(children='Map', style={
        'textAlign': 'center',
        'color': colors['text']
    }
    ),
    #map
    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='map-graph',
                        figure={
                            'data':data,
                            'layout':layout_map
                        },
                        animate=True,
                        style={'width': '100%', 'display': 'inline-block'}
                    ),
                ],className = "twelve columns"
            ),
        ], className="row"
    ),
    #selector
    html.Div(
        className="four columns div-user-controls",
        children=[
            html.Div(
                className="div-for-dropdown",
                children=[
                    dcc.Dropdown(
                        id="time-selector",
                        options=[
                            {"label":str(i)+" : 00","value":i}
                            for i in dfOriginal['dropoff_hours'].unique()
                        ],
                        multi=False,
                        searchable = False,
                        placeholder="Hour to filter:",
                    ),
                    dcc.Dropdown(
                        id="vendor-selector",
                        options=[
                            {"label":str(i),"value":i}
                            for i in dfOriginal['VendorID'].unique()
                        ],
                        multi=False,
                        searchable = False,
                        placeholder="Vendor to filter:",
                    ),
                ],
            ),

        ],
    ),

    #Graph 1 head
    html.Div(children='Income per Hour.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    #Graph 1
    dcc.Graph(
        id='graph1',

    ),
	#Graph 2 head
	html.Div(children='Income per District.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
	#Graph 2
	dcc.Graph(
        id='graph2',

    )
])

@app.callback(
    Output('map-graph', 'figure'),
    [Input('vendor-selector','value'),Input('time-selector','value')]
)
def map_update(vendor, time):
    if vendor is not None:
        if time is not None:
            pass
        else:
            pass

    else:
        if time is not None:
            pass
        else:
            return{"data":[trace_pickup],"layout":layout_map}

### Graph 1: All (Vendor 1+Vendeor 2 by defult) income per hour
### Style: Bar
### Parameter: Vendor A and/or Vendor B
### Chose: Hour
@app.callback(
    Output('graph1','figure'),
    [Input('vendor-selector','value')]
)
def graph1_update(vendor):
    dfGraph1_1=dfOriginal[dfOriginal.VendorID==1]
    dfGraph1_2=dfOriginal[dfOriginal.VendorID==2]
    
    df_1 = dfOriginal[dfOriginal.VendorID == 1]
    df_2 = dfOriginal[dfOriginal.VendorID == 2]
    
    v1xData1 = []
    v1yData1 = []
    v2xData1 = []
    v2yData1 = []
    
    for group, data in df_1.groupby(['dropoff_hours']):
        v1xData1.append(str(group) + " : 00")
        v1yData1.append(data['total_amount'].sum())
    
    for group, data in df_2.groupby(['dropoff_hours']):
        v2xData1.append(str(group) + " : 00")
        v2yData1.append(data['total_amount'].sum())
	


    #51884C
    figure_def={
        'data':[{'x':xData1,'y':yData1, 'type':'bar','marker':dict(color='#51884C'),'name':'hourIncome'}],
        'layout':{
            'plot_bgcolor':colors['background'],
            'paper_bgcolor':colors['background'],
            'font':{
                'color':colors['text'],
            },
            'titlefont':dict(color=colors['text'], size='14'),
            'title':'Income per Hour.',
        }
    }

    figure_1={
        'data':[{'x':v1xData1,'y':v1yData1, 'type':'bar','marker':dict(color='#51884C'),'name':'hourIncome'}],
        'layout':{
            'plot_bgcolor':colors['background'],
            'paper_bgcolor':colors['background'],
            'font':{
                'color':colors['text'],
            },
            'titlefont':dict(color=colors['text'], size='14'),
            'title':'Income per Hour.',
        }
    }
    figure_2={
        'data':[{'x':v2xData1,'y':v2yData1, 'type':'bar','marker':dict(color='#51884C'),'name':'hourIncome'}],
        'layout':{
            'plot_bgcolor':colors['background'],
            'paper_bgcolor':colors['background'],
            'font':{
                'color':colors['text'],
            },
            'titlefont':dict(color=colors['text'], size='14'),
            'title':'Income per Hour.',
        }
    }

    if vendor == '1':
        return figure_1
    elif vendor=='2':
        return figure_2
    else:
        return figure_def


if __name__ == '__main__':
    app.run_server(debug=True)