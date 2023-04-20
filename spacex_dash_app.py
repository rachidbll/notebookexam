# Import required libraries
import pandas as pd
import dash
from dash import html
#import dash_html_components as html
#import dash_core_components as dcc
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=[{
                                                    'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40','value':'CCAFS LC-40'},
                                                    {'label':'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                    {'label':'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label':'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                                    ],
                                                    value = 'ALL',
                                                    placeholder = 'Select a Launch Site Here',
                                                    searchable = True

                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    5000: '5000',
                                                    10000: '10000'},
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title=f'Total Launch For {entered_site} Site')
        return fig
    else:
        data = filtered_df[filtered_df['Launch Site'] == entered_site]
        info = {'class':['1','0'], 'total': [data['class'].value_counts()[1],data['class'].value_counts()[0]]}
        data2 = pd.DataFrame(info)
        print(info)
        fig = px.pie(data2, values='total', 
        names='class',
        title=f'Total Launch For {entered_site} Site')
        return fig
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Define the app callback
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def update_scatter_plot(site, payload_range):
    if site == 'ALL':
        # Render a scatter plot for all sites
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    else:
        # Filter the dataset for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == site]
        # Render a scatter plot for the selected site
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    # Set the payload range for the scatter plot
    fig.update_xaxes(range=payload_range)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
   