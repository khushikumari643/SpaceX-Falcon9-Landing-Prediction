#imports 

from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Create a Dash application instance
app = JupyterDash(__name__)

# Get unique years for the slider
min_year = yearly_success['Date'].min()
max_year = yearly_success['Date'].max()

# Define the app layout
app.layout = html.Div([
    html.H1("SpaceX Launch Success Dashboard", 
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    html.Div([html.P("Filter by Year:"),
              dcc.RangeSlider(
                  id='year-slider',
                  min=min_year,
                  max=max_year,
                  step=1,
                  marks={str(year): str(year) for year in range(min_year, max_year + 1)},
                  value=[min_year, max_year]
              )], style={'width': '80%', 'padding': '20px', 'margin': 'auto'}),

    html.Div(dcc.Graph(id='yearly-success-graph')),

    html.Div([html.P("Select Launcher Type:"),
              dcc.Dropdown(
                  id='launcher-type-dropdown',
                  options=[
                      {'label': 'All Launchers', 'value': 'All'},
                      {'label': 'Falcon 9', 'value': 'Falcon 9'},
                      {'label': 'Other', 'value': 'Other'}
                  ],
                  value='All',
                  placeholder="Select a launcher type",
                  searchable=False
              )], style={'width': '50%', 'padding': '20px', 'margin': 'auto'}),

    html.Div(dcc.Graph(id='launcher-comparison-graph'))
])

# Callback for Yearly Success Rate Graph
@app.callback(
    Output('yearly-success-graph', 'figure'),
    Input('year-slider', 'value')
)
def update_yearly_success_graph(selected_years):
    filtered_df = yearly_success[
        (yearly_success['Date'] >= selected_years[0]) &
        (yearly_success['Date'] <= selected_years[1])
    ]
    fig = px.line(filtered_df, 
                  x='Date', 
                  y='Class', 
                  title=f'Yearly Success Rate ({selected_years[0]}-{selected_years[1]})',
                  markers=True
                 )
    fig.update_layout(yaxis_title="Success Rate", xaxis_title="Year")
    return fig

# Callback for Launcher Comparison Graph
@app.callback(
    Output('launcher-comparison-graph', 'figure'),
    Input('launcher-type-dropdown', 'value'),
    Input('year-slider', 'value')
)
def update_launcher_comparison_graph(selected_launcher_type, selected_years):
    filtered_df1 = df1[
        (pd.to_numeric(df1['Date']) >= selected_years[0]) &
        (pd.to_numeric(df1['Date']) <= selected_years[1])
    ]
    
    if selected_launcher_type == 'All':
        data_to_plot = filtered_df1.groupby('LauncherType')['Class'].mean().reset_index()
        title = f'Success Rate by Launcher Type ({selected_years[0]}-{selected_years[1]})'
    else:
        data_to_plot = filtered_df1[filtered_df1['LauncherType'] == selected_launcher_type]
        if data_to_plot.empty:
            # Handle case where selected launcher type has no data in the filtered year range
            return go.Figure().update_layout(title='No data for selected launcher type in this period')
        
        # Group by year or just show overall success for that launcher if not enough yearly data
        data_to_plot = data_to_plot.groupby('Date')['Class'].mean().reset_index()
        fig = px.line(data_to_plot, 
                      x='Date', 
                      y='Class', 
                      title=f'Success Rate for {selected_launcher_type} ({selected_years[0]}-{selected_years[1]})',
                      markers=True
                     )
        fig.update_layout(yaxis_title="Success Rate", xaxis_title="Year")
        return fig

    fig = px.bar(data_to_plot, 
                 x='LauncherType', 
                 y='Class', 
                 title=title,
                 color='LauncherType'
                )
    fig.update_layout(yaxis_title="Success Rate", xaxis_title="Launcher Type")
    return fig


if __name__=='__main__':
  app.run(debug=True)


