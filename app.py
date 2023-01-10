from dash import Dash, dcc, html, dash_table
from dash.dependencies import Output, Input

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

from datetime import datetime, timedelta

from functions import *

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
chart_options = [{'label': s, 'value': s} for s in ["Line", "Bar"]]
yesno_options = [{'label': s, 'value': s} for s in ["Yes", "No"]]
cum_options = [{'label': s, 'value': s} for s in ["Cumulative", "Per Fight"]]

structure_f = ["Name", "Date", "Winlose Score","Finish Score", "Finish Rate", "KO/TKO", "Submission", "Decision", "Wins", "Losses", "Draws/NCs",
			   "Knockdowns", "Takedowns Landed", "Takedowns Attempted", "Reversals", "Submission Attempted", "Control Time", "Weight",
			   "Significant Strikes", "Attempted Strikes", "Accuracy", "Head", "Body", "Leg", "Distance", "Clinch", "Ground"]
structure_r = ["Name", "Date", "KO/TKO", "Submission", "Decision", "Finish Rate", "Weight"]

structure_f_pf = ["Name", "Date", "Opponent", "Weight", "Method", "Win", "Knockdowns", "Takedowns Landed", "Takedowns Attempted", "Reversals", 
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
app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY, dbc_css])
server = app.server

app.title = "Tomato"

app.html_layout = """<!DOCTYPE html>
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
</head>"""

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
                                        # dcc.Dropdown(id="filter_graph_chart", style=style_button, options=chart_options, placeholder='Select Graph', value='Line'),
                                        dcc.Dropdown(id="filter_graph_cum", style=style_button, options=cum_options, value='Cumulative'),
                                        dcc.Dropdown(id="filter_graph_group", style=style_button, options=group_options, placeholder='Select Group', value='Fighters'),
                                        dcc.Dropdown(id="filter_graph_by", style=style_button, placeholder='Select Option'),
                                        dcc.Dropdown(id="filter_graph_person", style=style_button, placeholder='Select Person(s)', value=['All'], multi=True),
                                        dcc.Dropdown(id="filter_graph_weight", style=style_button, options=weight_options, placeholder='Select Weight', value=['Lightweight'], multi=True),
                                        # dcc.Dropdown(id="filter_graph_percentage", style=style_button, options=yesno_options, value='No'),
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
				            },
				            {
				                'if': {'column_id': 'Date'},
				                'textAlign': 'left',
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
			        style={
			            "position": "fixed",
			            "bottom": "0",
			            "width": "100%",
			        },
                ),
            ],
            fluid=True,
            style={'padding-top': '10px'}
        ),
	    ], 
	    fluid=True,
	    className="dbc",
	    style={'padding-top': '1px'}
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

	columns = ["Name", "Date", "Opponent", "Win", "Method", "Significant Strikes", "Attempted Strikes", "Accuracy", 
				 "Head", "Body", "Leg", "Knockdowns", "Takedowns Landed", "Takedowns Attempted", "Reversals"]
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
    Output("filter_graph_group", "disabled"),
    Output("filter_graph_group", "value"),
    [Input("filter_graph_cum", "value")])
def update_filter_graph_group(cum):
	if cum == 'Per Fight':
		disabled = True
	else:
		disabled = False
	
	value = "Fighters"
	return disabled, value

@app.callback(
    Output("filter_graph_person", "options"),
    Output("filter_graph_person", "value"),
    [Input("filter_graph_group", "value"),
    Input("filter_graph_person", "value")])
def update_filter_graph_person(value, name):
	if value == "Fighters":
		names = all_f_names_options
		name_check = all_f_names
	else:
		names = all_r_names_options
		name_check = all_r_names

	name_list = []
	for n in name:
		if n in ['All'] + name_check:
			name_list.append(name)

	return names, name

@app.callback(
    Output("filter_graph_by", "options"),
    Output("filter_graph_by", "value"),
    [Input("filter_graph_cum", "value"),
    Input("filter_graph_group", "value"),
    Input("filter_graph_by", "value")])
def update_filter_graph_by(cum, value, by_value):
	if value == "Fighters":
		if cum == 'Per Fight':
			structure = structure_f_pf
			by = by_f_pf
		else:
			structure = structure_f
			by = by_f
	else:
		structure = structure_r
		by = by_r

	if by_value not in structure:
		by_value = "KO/TKO"

	return by, by_value

@app.callback(
    Output("filter_graph_weight", "disabled"),
    Output("filter_graph_weight", "value"),
    [Input("filter_graph_group", "value")])
def update_filter_graph_group(group):
	if group == 'Referees':
		disabled = True
	else:
		disabled = False
	
	value = []
	return disabled, value

if __name__ == "__main__":
    app.run_server(debug=True)