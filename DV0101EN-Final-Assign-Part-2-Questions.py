#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

year_list = sorted(data['Year'].unique())

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', "color":"#503D36", "font-size":24}),
    
    html.Label("Select Statistics:"),
    dcc.Dropdown(
        id='select-statistics',
        options=dropdown_options,
        value='Yearly Statistics',
        placeholder='Select a statistic'
    ),
    
    html.Label("Select Year:"),
    dcc.Dropdown(
        id='select-year',
        options=[{'label': str(i), 'value': i} for i in year_list],
        value=year_list[0]
    ),
    
    html.Div(id='output-container', className='chart-grid', style={"display":"flex"})
])

@app.callback(
    Output('select-year', 'disabled'),
    Input('select-statistics', 'value')
)
def update_year_dropdown(selected_statistics):
    return selected_statistics == 'Recession Period Statistics'

@app.callback(
    Output('output-container', 'children'),
    [Input('select-statistics', 'value'), Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                                            title="Average Automobile Sales Over Recession Period"))
        
        avg_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(avg_sales, x='Vehicle_Type', y='Automobile_Sales',
                                           title="Average Vehicles Sold by Type During Recession"))
        
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(exp_rec, names='Vehicle_Type', values='Advertising_Expenditure',
                                           title="Advertising Expenditure Share by Vehicle Type"))
        
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                                           title='Effect of Unemployment Rate on Vehicle Sales'))
        
        return [html.Div([R_chart1, R_chart2], style={'display': 'flex'}),
                html.Div([R_chart3, R_chart4], style={'display': 'flex'})]

    elif selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]
        
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales',
                                            title='Yearly Automobile Sales Trend'))
        
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas, x='Month', y='Automobile_Sales',
                                            title='Monthly Automobile Sales in {}'.format(input_year)))
        
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                                           title='Average Vehicles Sold by Type in {}'.format(input_year)))
        
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, names='Vehicle_Type', values='Advertising_Expenditure',
                                           title='Advertising Expenditure by Vehicle Type in {}'.format(input_year)))
        
        return [html.Div([Y_chart1, Y_chart2], style={'display': 'flex'}),
                html.Div([Y_chart3, Y_chart4], style={'display': 'flex'})]
    
    return None

if __name__ == '__main__':
    app.run(debug=True)
