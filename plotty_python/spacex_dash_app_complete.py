# Import required libraries using anaconda local libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data and  creating a pandas dataframe
#wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"  download in local pc 
spacex_df = pd.read_csv("spacex_launch_dash.csv")
print(spacex_df.head())
#getting max and min values of payload
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#converting type
spacex_df.astype({'Payload Mass (kg)': 'int64'}).dtypes
print(spacex_df.dtypes)


# Create a list object of dictionaries for each sites
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
sites_list = [] #list object

#loop for  fllling list of sites 
for i in launch_sites_df['Launch Site']:
    temp_dict= dict()
    temp_dict['label'] = str(i)
    temp_dict['value'] = str(i)
    sites_list.append(temp_dict)
sites_list.insert(0,{'label': 'ALL', 'value': 'ALL'})


# Creating dash app
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 30}), # default 40 reduce to 30
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site-dropdown',
                                        options=sites_list,
                                            value="ALL",
                                            placeholder="Select a Launch site here",
                                            searchable=True,
                                            ),
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                            min=0, max=10000, step=2000,
                                            marks={0: '0', 2000: '2000', 4000: '4000', 6000: '6000', 8000: '8000', 10000: '10000'},
                                            value=[min_payload, max_payload]),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
        [Output(component_id= 'success-pie-chart', component_property= 'figure'),
        Output(component_id='success-payload-scatter-chart', component_property='figure')],
        [Input(component_id= 'site-dropdown', component_property='value'),
        Input(component_id="payload-slider", component_property="value")]
        )

def get_pie_chart(entered_site, payload): #this needs to contain the scatter graph also.
    filtered_df = spacex_df
    print(payload)
    #for item in enumerate(payload):
    #    payload[item] = float(item)
    
    
    if entered_site == 'ALL':
        total_sites = filtered_df.groupby(['Launch Site'])['class'].sum().reset_index()
        fig = px.pie(total_sites, values='class', 
        names='Launch Site', 
        title='Total sucessful launches')
        
        fig1 = px.scatter(filtered_df,
                        x="Payload Mass (kg)", 
                        y= "class", 
                        color="Booster Version Category")
        return fig, fig1
    else:
        entered_site == str(entered_site)
        
        entered_df = spacex_df[spacex_df['Launch Site'] == str(entered_site)]
        fig = px.pie(entered_df, 
            values="class", 
            names="Launch Site", 
            title="Success vs failed")
        filtered_df = spacex_df[
                        spacex_df["Payload Mass (kg)"]> float(payload[0]) &
                        spacex_df["Payload Mass (kg)"] < float(payload[1])]
        print(filtered_df.head())
        fig1 = px.scatter(filtered_df,
                        x="Payload Mass (kg)", 
                        y= "class", 
                        color="Booster Version Category")
        return fig, fig1
    fig.show()    




# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
                [Input(component_id='site-dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')])

def scatter (site_dropdown,payload_slider):
    low,high=(payload_slider)
    mask=(spacex_df['Payload Mass (kg)']>low)&(spacex_df['Payload Mass (kg)']<high)
    filtered_df=spacex_df[mask]
    if site_dropdown == 'ALL':
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class',
                            color='Booster Version Category',
                            title='Payload vs. Outcome for All Sites')
        fig=px.scatter(spacex_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                        title="Payload vs. Outcome for All Sites")
        return fig
    else:
        filtered_df1 = filtered_df[filtered_df['Launch Site']==site_dropdown]
        fig = px.scatter (filtered_df1, x='Payload Mass (kg)', y='class',
                            color='Booster Version Category',
                            title='Payload and Booster Versions for site')
        filtered_df1=filtered_df[filtered_df['Launch Site']==site_dropdown]
        fig=px.scatter(filtered_df1,x='Payload Mass (kg)',y='class',color='Booster Version Category',
                        title="Payload and Booster Versions for site")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()