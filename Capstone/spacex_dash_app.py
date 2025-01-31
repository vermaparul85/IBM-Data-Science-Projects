# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("10-3-spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
site_list = [{'label':launch_site, 'value':launch_site} for launch_site in spacex_df['Launch Site'].unique()]
site_list.insert(0, {'label': 'All Sites', 'value': 'ALL'})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=site_list, value='ALL',
                                             placeholder='Select a Launch Site here', searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload],
                                                marks={0: '0', 2500:'2500', 5000:'5000', 7500:'7500', 10000:'10000'}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(input_site):
    if input_site == 'ALL':
        fig = px.pie(data_frame=spacex_df, names='Launch Site', values='class', title='Total Success Launches By Site')
        return fig
    else:
        site_df = spacex_df[spacex_df['Launch Site'] == input_site]
        fig = px.pie(data_frame=site_df, names='class', title=f'Total Success Launches for Site {input_site}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
              [Input(component_id='site-dropdown',component_property='value'),
               Input(component_id='payload-slider',component_property='value')])
def get_scatter_chart(input_site, input_payload):
    if input_site == 'ALL':
        site_payload_df = spacex_df[spacex_df['Payload Mass (kg)'].between(input_payload[0], input_payload[1])]
        fig = px.scatter(data_frame=site_payload_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig
    else:
        site_payload_df = spacex_df[(spacex_df['Launch Site'] == 'KSC LC-39A') & (spacex_df['Payload Mass (kg)'].between(input_payload[0],input_payload[1]))]
        fig = px.scatter(data_frame=site_payload_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
