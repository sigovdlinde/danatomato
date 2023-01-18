from dash import Dash, dcc, html, dash_table
from dash.dependencies import Output, Input

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

from datetime import datetime, timedelta

from create_datasets import *

all_fight_data = open_data('all_fight_data')
all_f_data = open_data('all_f_data')
all_r_data = open_data('all_r_data')

all_f_data_pf = open_data('all_f_data_pf')

all_f_names = all_fighter_names(all_fight_data)
all_r_names = all_referee_names(all_fight_data)

weights = ["Heavyweight", "Light Heavyweight", "Middleweight", "Welterweight", "Lightweight", "Featherweight", "Bantamweight", 
		  "Flyweight", "Women's Bantamweight", "Women's Strawweight", "Women's Flyweight", "Women's Featherweight", "Open Weight", "Super Heavyweight", "Catch Weight"]

weight_options = [{'label': s, 'value': s} for s in weights]
all_f_names_options = [{'label': s, 'value': s} for s in ['All'] + all_f_names]
all_r_names_options = [{'label': s, 'value': s} for s in ['All'] + all_r_names]

group_options = [{'label': s, 'value': s} for s in ["Fighters", "Referees"]]

cum_options_fighters = [{'label': s, 'value': s} for s in ["Cumulative", "Per Fight"]]
cum_options_refs = [{'label': s, 'value': s} for s in ["Cumulative"]]
cum_options_fights = [{'label': s, 'value': s} for s in ["Per Fight"]]

structure_f = ["Name", "Date", "Winlose Score","Finish Score", "Finish Rate", "KO/TKO", "Submission", "Decision", "Wins", "Losses", "Draws/NCs",
			   "Knockdowns", "Takedowns Landed", "Takedowns Attempted", "Reversals", "Submission Attempted", "Control Time", "Weight",
			   "Significant Strikes", "Attempted Strikes", "Accuracy", "Head", "Body", "Leg", "Distance", "Clinch", "Ground"]
structure_r = ["Name", "Date", "KO/TKO", "Submission", "Decision", "Finish Rate", "Weight"]

structure_f_pf = ["Name", "Date", "Venue", "Opponent", "Weight", "Method", "Win", "Details", "Knockdowns", "Takedowns Landed", "Takedowns Attempted", "Reversals", 
				 "Submission Attempted", "Control Time", "Significant Strikes", "Attempted Strikes", "Accuracy", 
				 "Head", "Body", "Leg", "Distance", "Clinch", "Ground"] 

by_fighter = ["Winlose Score","Finish Score", "Finish Rate", "KO/TKO", "Submission", "Decision", "Wins", "Losses", "Draws/NCs",
			   "Knockdowns", "Takedowns Landed", "Takedowns Attempted", "Reversals", "Submission Attempted", "Control Time",
			   "Significant Strikes", "Attempted Strikes", "Accuracy", "Head", "Body", "Leg", "Distance", "Clinch", "Ground"]
by_referee = ["KO/TKO", "Submission", "Decision", "Finish Rate"]

by_fighter_pf = ["Knockdowns", "Takedowns Landed", "Takedowns Attempted", "Reversals", "Submission Attempted", 
				"Control Time", "Significant Strikes", "Attempted Strikes", "Accuracy", "Head", "Body", "Leg", 
				"Distance", "Clinch", "Ground"] 

by_f = [{'label': s, 'value': s} for s in by_fighter]
by_r = [{'label': s, 'value': s} for s in by_referee]

by_f_pf = [{'label': s, 'value': s} for s in by_fighter_pf]

load_figure_template("sketchy")

style_button = {'border': 'none', 'display': 'block'}

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY, dbc_css, "/assets/style.cc"])
server = app.server

app.title = "MMA Dashboard"

app.index_string = """
<!DOCTYPE html>
<html>
    <head>
		<!-- Google tag (gtag.js) -->
		<script async src="https://www.googletagmanager.com/gtag/js?id=G-273RFDY9XD"></script>
		<script>
		  window.dataLayer = window.dataLayer || [];
		  function gtag(){dataLayer.push(arguments);}
		  gtag('js', new Date());

		  gtag('config', 'G-273RFDY9XD');
		</script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

app.layout = dbc.Container(
    [
        # Body
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(dbc.Card(
                                    [
                                        dcc.Dropdown(id="filter_graph_group", 
                                    		style=style_button, 
                                    		options=group_options, 
                                    		placeholder='Select Group', 
                                    		value='Fighters'
                                    	),
                                        dcc.Dropdown(id="filter_graph_cum", 
                                    		style=style_button, 
                                    		options=cum_options_fighters, 
                                    		placeholder='Select Chart', 
                                    		value='Cumulative'
                                    	),
                                        dcc.Dropdown(id="filter_graph_by", 
                                    		style=style_button, 
                                    		options=by_f ,
                                    		placeholder='Select Option', 
                                    		value='Winlose Score'
                                    	),
                                        dcc.Dropdown(id="filter_graph_person", 
                                    		style=style_button, 
                                    		options=all_f_names_options ,
                                    		placeholder='Select Person(s)', 
                                    		value=['Tony Ferguson ', 'Khabib Nurmagomedov '], 
                                    		multi=True
                                    	),
                                        dcc.Dropdown(id="filter_graph_weight", 
                                        	style=style_button, 
                                        	options=weight_options, 
                                        	placeholder='Select Weight', 
                                        	value=['Lightweight'], 
                                        	multi=True
                                        ), 
                                    ], 
                                ),style={'padding-bottom': '15px'}),
				                dbc.Card(
				                    [
				                        html.Ul(
				                        	[
					                        	html.Li("Winlose Score = Wins - Losses.", style={'padding-bottom': '10px'}),
					                        	html.Li("Finish Score = KO/TKOs + Submissions - Decisions. Only counting wins.", style={'padding-bottom': '10px'}),
					                        	html.Li("Finish Rate = KO/TKOs + Submissions - Decisions."),
				                        	],
				                        ),
				                    ], style={'padding-top': '10px'}
				                    
				                ),
                            ],
                            id="column-1",
                            width=2,
                        ),
                        dbc.Col(dbc.Card(dcc.Graph(id="graph_line", config={"displayModeBar": False}, className="container")), width=7),
						dbc.Col(dbc.Card(dcc.Tabs(
							[
							    dcc.Tab(label='Top', children=[dash_table.DataTable(
								        id="datatable1",
								        cell_selectable=False,
								        style_table={'overflowY': 'scroll', 'height': '450px'},
								        style_cell={
								            'border': '0px solid white',
								            'backgroundColor': 'transparent'
								        },
								        style_cell_conditional=[
										    {
										        'textAlign': 'center'
										    },
								            {
								                'if': {'column_id': 'Name'},
								                'textAlign': 'left',
								                'padding-left': '30px'
								            },
								        ],
								        style_as_list_view=True,
								    )
							    ]),
							    dcc.Tab(label='Bottom', children=[dash_table.DataTable(
								        id="datatable2",
								        cell_selectable=False,
								        style_table={'overflowY': 'scroll', 'height': '450px'},
								        style_cell={
								            'border': '0px solid white',
								            'backgroundColor': 'transparent'
								        },
								        style_cell_conditional=[
										    {
										        'textAlign': 'center'
										    },
								            {
								                'if': {'column_id': 'Name'},
								                'textAlign': 'left',
								                'padding-left': '30px'
								            },
								        ],
								        style_as_list_view=True,
								    )
							    ]),

						    ], style={'height': '50px'}
						    )),
						    width=3,
						    className="dbc dbc-row-selectable"
						),
                    ]
                ),
                dbc.Row(dbc.Card(
                	dash_table.DataTable(
                		id="datatable3",
                		cell_selectable=False,
                		style_table={'overflowY': 'scroll', 'height': '600px'},
				        style_cell={
				            'border': '0px solid white',
				            'backgroundColor': 'transparent'
				        },
				        style_cell_conditional=[
						    {
						        'textAlign': 'left'
						    },
				            {
				                'if': {'column_id': 'Details'},
				                'padding-left': '50px'
				            },
				        ],
                		style_as_list_view=True,
                	)

                ), style={'padding-top': '15px'}),
                dbc.Row(
	                html.Div(
	                    [
	                        html.P("“I'm fuckin red I just gotta deal with it” - Dana White"),
	                    ],
	                    className="text-center"
	                ),
			        style={'padding-top': '10px'},
                ),
            ],
            fluid=True,
            style={'padding-top': '10px'}
        ),
	    ], 
	    fluid=True,
	    className="dbc",
)


@app.callback(
    Output("datatable3", "data"),
    Output("datatable3", "columns"),
    [Input("filter_graph_cum", "value"),
    Input("filter_graph_group", "value"),
    Input("filter_graph_person", "value"),
	Input("filter_graph_by", "value"),
	Input("filter_graph_weight", "value")])
def update_datatable3(cum, group, name, value, weight):
	all_data = all_f_data_pf
	structure = structure_f_pf

	if weight == None or weight == [] or group == "Referees":
		weight = weights

	df= pd.DataFrame(all_data, columns=structure)
	if weight == None or weight == []:
		weight = weights
	df = df[df['Weight'].isin(weight)]

	if name == None or name == ['All']:
		name = all_f_names
	df = df[df['Name'].isin(name)]

	columns = ["Name", "Date", "Opponent", "Win", "Method", "Weight", "Details"] 

	df["Win"] = df["Win"].replace([0, 1, 2], ["Win", "Loss", "Draw/NC"])
	df = df[columns]
	df = df.sort_values('Date').reset_index(drop=True)
	df.columns = columns
	df = df.rename(columns = {'Win':'Result'})
	df.Date = pd.DatetimeIndex(df.Date).strftime("%Y-%m-%d")
	columns =  [{"name": i, "id": i,} for i in (df.columns)]

	return df[::-1][:250].to_dict('records'), columns

@app.callback(
    Output("graph_line", "figure"), 
    [Input("filter_graph_cum", "value"),
    Input("filter_graph_group", "value"),
    Input("filter_graph_person", "value"),
	Input("filter_graph_by", "value"),
	Input("filter_graph_weight", "value")])
def update_line_chart(cum, group, names, value, weight):
	if group == "Fighters":
		if 'All' in names:
			names = all_f_names

		if cum == 'Per Fight':
			all_data = all_f_data_pf
			structure = structure_f_pf
		else:
			all_data = all_f_data
			structure = structure_f

	elif group == "Referees":
		if "All" in names:
			names = all_r_names

		all_data = all_r_data
		structure = structure_r

	if weight == None or weight == [] or group == "Referees":
		weight = weights

	df= pd.DataFrame(all_data, columns=structure)
	df = df[df['Name'].isin(names) & df['Weight'].isin(weight)]

	if value == "Control Time":
		df = df.fillna(value=timedelta())
		df['Control Time'] = df['Control Time'].apply(lambda x: x.total_seconds())

	if cum == 'Per Fight':
		if group == "Referees":
			fig = px.scatter(df, x="Date", y=value, color="Name")
		else:
			fig = px.scatter(df, x="Date", y=value, color="Name", hover_data={"Opponent":True})
		fig.update_traces(marker=dict(size=4, color='black'))
	else:
		fig = px.line(df, x="Date", y=value, color="Name")
		fig.update_traces(line_color='black', line_width=0.7)

	fig.update_layout(
	    xaxis=dict(
	        showgrid=False,
	        showline=True,
	        linecolor='rgb(102, 102, 102)',
	        tickcolor='rgb(102, 102, 102)',
	        showticklabels=True,
	        tickfont=dict(
	            size=14,
	            color='rgb(102, 102, 102)'
	        ),
	        zeroline=True,
	        zerolinecolor='rgb(255,255,255)',
	        zerolinewidth=2
	    ),
	    yaxis=dict(
	        showgrid=False,
	        showline=True,
	        linecolor='rgb(102, 102, 102)',
	        tickcolor='rgb(102, 102, 102)',
	        showticklabels=True,
	        tickfont=dict(
	            size=14,
	            color='rgb(102, 102, 102)'
	        )
	    )
	)
	fig.update_layout(showlegend=False)
	return fig

@app.callback(
    Output("datatable1", "data"),
    Output("datatable1", "columns"),
    Output("datatable2", "data"),
    Output("datatable2", "columns"),
    [Input("filter_graph_cum", "value"),
    Input("filter_graph_group", "value"),
	Input("filter_graph_by", "value"),
	Input("filter_graph_weight", "value")])
def update_datatable(cum, group, value, weight):
	if group == "Fighters":
		if cum == 'Per Fight':
			all_data = all_f_data_pf
			structure = structure_f_pf
		else:
			all_data = all_f_data
			structure = structure_f

	elif group == "Referees":
		all_data = all_r_data
		structure = structure_r

	if weight == None or weight == [] or group == "Referees":
		weight = weights

	df= pd.DataFrame(all_data, columns=structure)
	df = df[df['Weight'].isin(weight)]

	if cum == 'Cumulative':
		df = df.sort_values(by='Date', ascending=False)
		df = df.drop_duplicates(subset='Name', keep='first')

	df = df[["Name", value]]
	df = df.sort_values(value, ascending=False).reset_index(drop=True)
	df.index += 1
	df = df.reset_index(level=0)
	df.columns = ["#", "Name", value]
	columns =  [{"name": i, "id": i,} for i in (df.columns)]

	if value == "Control Time":
		df = df.fillna(value=timedelta())
		df[value] = df[value].apply(lambda x: (datetime(1900, 1, 1) + x).strftime('%H:%M:%S'))

	return df[:250].to_dict('records'), columns, df[::-1][:250].to_dict('records'), columns

@app.callback(
	Output("filter_graph_cum", "options"),
    Output("filter_graph_cum", "value"),
    [Input("filter_graph_group", "value")])
def update_filter_graph_cum(group):
	if group == 'Fighters':
		cum_options = cum_options_fighters
		cum_value = "Cumulative"

	elif group == 'Referees':
		cum_options = cum_options_refs
		cum_value = "Cumulative"

	elif group == 'Fights':
		cum_options = cum_options_fights
		cum_value = "Per Fight"
	
	return cum_options, cum_value

@app.callback(
    Output("filter_graph_by", "options"),
    Output("filter_graph_by", "value"),
    [Input("filter_graph_group", "value"),
    Input("filter_graph_cum", "value")])
def update_filter_graph_by(group, cum):
	if group == 'Fighters':
		if cum == 'Cumulative':
			by_options = by_f
			by_value = 'Winlose Score'

		elif cum == 'Per Fight':
			by_options = by_f_pf
			by_value = 'Significant Strikes'

	elif group == 'Referees':
		by_options = by_r
		by_value = 'Finish Rate'

	# temp options & value
	elif group == 'Fights':
		by_options = by_f_pf
		by_value = 'Significant Scrikes'

	return by_options, by_value


@app.callback(
    Output("filter_graph_person", "options"),
    Output("filter_graph_person", "value"),
    [Input("filter_graph_group", "value")])
def update_filter_graph_person(group):
	if group in ['Fighters', 'Fights']:
		person_options = all_f_names_options
		person_value = ['Tony Ferguson ', 'Khabib Nurmagomedov ']

	elif group == 'Referees':
		person_options = all_r_names_options
		person_value = ['Herb Dean', 'Keith Peterson']

	return person_options, person_value

@app.callback(
    Output("filter_graph_weight", "style"),
    [Input("filter_graph_group", "value")])
def update_filter_graph_weight(group):
	if group in ['Fighters', 'Fights']:
		weight_style = style_button

	elif group == 'Referees':
		weight_style = {"display":"none"}

	return weight_style


if __name__ == "__main__":
    app.run_server(debug=True)



