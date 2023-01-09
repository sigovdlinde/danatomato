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

structure_f = ["Name", "Date", "Winlose Score","Finish Score", "Finish Rate", "KO/TKO", "Submission", "Decision", "Wins", "Losses", "Draws/NCs",
			   "Knockdowns", "Takedowns Landed", "Takedowns Attempted", "Reversals", "Submission Attempted", "Control Time", "Weight"]
structure_r = ["Name", "Date", "KO/TKO", "Submission", "Decision", "Finish score", "Weight"]

by_f = [{'label': s, 'value': s} for s in structure_f[2:]]
by_r = [{'label': s, 'value': s} for s in structure_r[2:]]

load_figure_template("sketchy")

style_button = {'border': 'none', 'display': 'block'}

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY, dbc_css])
server = app.server

app.title = "Tomato"

app.layout = dbc.Container(
    [
        # Header
        # dbc.Card(
        #     [
        #         dbc.CardBody(
        #             [
		#                 dbc.Row(
		#                     [
		#                         dbc.Col(
		#                             html.Img(src='assets/danatomato.png', width='50%', height='50%'),
		#                             width=2,
		#                         ),
		#                         dbc.Col(
		#                             [
		# 				                html.Div(
		# 				                    [
		# 				                        html.H3("Sam Alvey Fan Page")
		# 				                    ],
		# 				                    className="text-center"
		# 				                ),
		#                             ],
		#                             # Change width to 8 when adding images back.
		#                             width=12,
		#                             className="align-items-center justify-content-center"
		#                         ),
		#                         dbc.Col(
		#                             html.Img(src='assets/samciggie.png', width='40%', height='40%'),
		#                             width=2,
		#                         ),
		#                     ],
		#                     className="align-items-center",
		#                 )
        #             ]
        #         )
        #     ],
        # ),
        # Body
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dcc.Dropdown(id="filter_graph_chart", style=style_button, options=chart_options, placeholder='Select Graph', value='Line'),
                                        dcc.Dropdown(id="filter_graph_group", style=style_button, options=group_options, placeholder='Select Group', value='Fighters'),
                                        dcc.Dropdown(id="filter_graph_by", style=style_button, placeholder='Select Option', value='Finish Rate'),
                                        dcc.Dropdown(id="filter_graph_person", style=style_button, placeholder='Select Person(s)', value=['All'], multi=True),
                                        dcc.Dropdown(id="filter_graph_weight", style=style_button, options=weight_options, placeholder='Select Weight', value=['Lightweight'], multi=True),
                                        # dcc.Dropdown(id="filter_graph_percentage", style=style_button, options=yesno_options, value='No'),
                                    ]
                                ),
				                html.Div(
				                    [
				                        html.Ul(
				                        	[
					                        	html.Li("Winlose Score = Wins - Losses.", style={'padding-bottom': '10px'}),
					                        	html.Li("Finish Score = KO/TKOs + Submission - Decision. Only counting wins.", style={'padding-bottom': '10px'}),
					                        	html.Li("Finish Rate = KO/TKOs + Submission - Decision."),
				                        	],
				                        ),
				                    ],
				                    style={'padding-top': '10px'}
				                ),
                            ],
                            id="column-1",
                            width=2,
                        ),
                        dbc.Col(dbc.Card(dcc.Graph(id="graph_line", config={"displayModeBar": False}, className="container")), width=7),
						dbc.Col(dbc.Card(
						    dash_table.DataTable(
						        id="datatable1",
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
						    )),
						    width=3,
						    className="dbc dbc-row-selectable"
						),
                    ]
                ),
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
    style={'padding-top': '10px'}
)

@app.callback(
    Output("graph_line", "figure"), 
    [Input("filter_graph_group", "value"),
    Input("filter_graph_person", "value"),
	Input("filter_graph_by", "value"),
	Input("filter_graph_weight", "value")])
def update_line_chart(group, names, value, weight):
	if group == "Fighters":
		if 'All' in names:
			names = all_f_names

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
		df['Control Time'] = df['Control Time'].apply(lambda x: x.total_seconds())

	fig = px.line(df, x="Date", y=value, color="Name")
	fig.update_layout(showlegend=False)
	fig.update_traces(line_color='black', line_width=0.7)
	return fig

@app.callback(
    Output("datatable1", "data"),
    Output("datatable1", "columns"),
    [Input("filter_graph_group", "value"),
	Input("filter_graph_by", "value"),
	Input("filter_graph_weight", "value")])
def update_datatable(group, value, weight):
	if group == "Fighters":
		all_data = all_f_data
		structure = structure_f

	elif group == "Referees":
		all_data = all_r_data
		structure = structure_r

	if weight == None or weight == [] or group == "Referees":
		weight = weights

	df= pd.DataFrame(all_data, columns=structure)
	df = df[df['Weight'].isin(weight)]

	df = df.sort_values(by='Date', ascending=False)
	df = df.drop_duplicates(subset='Name', keep='first')
	df = df[["Name", value]]

	df = df.sort_values(value, ascending=False).reset_index(drop=True)
	df.index += 1
	df = df.reset_index(level=0)
	df.columns = ["#", "Name", value]
	columns =  [{"name": i, "id": i,} for i in (df.columns)]

	if value == "Control Time":
		df[value] = df[value].apply(lambda x: (datetime(1900, 1, 1) + x).strftime('%H:%M:%S'))

	return df[:250].to_dict('records'), columns

@app.callback(
    Output("filter_graph_person", "options"),
    Output("filter_graph_by", "options"),
    Output("filter_graph_by", "value"),
    [Input("filter_graph_group", "value"),
    Input("filter_graph_by", "value")])
def update_filter_graph(value, by_value):
	if value == "Fighters":
		names = all_f_names_options
		by = by_f
		if by_value not in structure_f[2:]:
			by_value = "Finish score"
	else:
		names = all_r_names_options
		by = by_r
		if by_value not in structure_r[2:]:
			by_value = "Finish score"

	return names, by, by_value


if __name__ == "__main__":
    app.run_server(debug=True)