# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

sites = spacex_df['Launch Site'].drop_duplicates().array

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                        options=[{'label': 'All Sites','value':'ALL'},
                                        {'label':f'{sites[0]}','value':f'{sites[0]}'},
                                        {'label':f'{sites[1]}','value':f'{sites[1]}'},
                                        {'label':f'{sites[2]}','value':f'{sites[2]}'},
                                        {'label':f'{sites[3]}','value':f'{sites[3]}'}],
                                        value='ALL',
                                        placeholder='Select Launch Site(s)',
                                        searchable=True
                                        ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=min_payload, max=max_payload,
                                                step = 1000,
                                                value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id = 'success-pie-chart', component_property = 'figure'),
			  Input(component_id = 'site-dropdown', component_property = 'value'))

def get_pie_chart(entered_site):
    #filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
            names='Launch Site', #'pie chart names', 
            title='Success Counts for All Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        data_onesite = spacex_df[spacex_df['Launch Site'] == entered_site]
        data_grouped = data_onesite['class'].value_counts().reset_index()
        data_grouped.columns = ['class', 'count']
        fig_one = px.pie(data_grouped, values='count',
            names='class',
            title=f'Success Counts for {entered_site}')
        return fig_one

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
			  [Input(component_id = 'site-dropdown', component_property = 'value'),
              Input(component_id = 'payload-slider', component_property = 'value')])

def get_slider_scatter_chart(entered_site,payload_range):
    spacex_df_PLrange = spacex_df[((spacex_df['Payload Mass (kg)'] > payload_range[0])
                                & (spacex_df['Payload Mass (kg)'] < payload_range[1]))]
    if entered_site == 'ALL':
        fig = px.scatter(spacex_df_PLrange, 
                        x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Payload vs. Outcome for All Sites')
        fig.update_xaxes(range=[0,10000])  #range=[max_payload, max_payload])
        return fig
    else:
        spacex_df_PLrange_one = spacex_df_PLrange[spacex_df_PLrange['Launch Site'] == entered_site]
        fig = px.scatter(spacex_df_PLrange_one, 
                        x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Payload vs. Outcome for All Sites')
        fig.update_xaxes(range=[0,10000])  #range=[max_payload, max_payload])
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(port=8052)