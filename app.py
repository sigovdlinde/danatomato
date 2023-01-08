from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from functions import *

import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

all_fight_data = open_data('all_fight_data')

all_f_n = all_fighter_names(all_fight_data)
all_f_n_options = ['Everyone'] + all_f_n
all_f_names = [{'label': s, 'value': s} for s in all_f_n_options]

all_r_n = all_referee_names(all_fight_data)
all_r_n_options = ['Everyone'] + all_r_n
all_r_names = [{'label': s, 'value': s} for s in all_r_n_options]

group_names = [{'label': s, 'value': s} for s in ["Fighters", "Referees"]]
chart_names = [{'label': s, 'value': s} for s in ["Line", "Bar"]]

structure_f = ["Name", "Date", "KO/TKO", "Submission", "Decision", "Winlose score", "Finish score"]
structure_r_new = ["Name", "Date", "KO/TKO", "Submission", "Decision", "Finish score"]

structure_t = ["KO/TKO", "Submission", "Decision", "Finish score"]
structure_r = ["Ref", "Date", "Method"]

by_f = [{'label': s, 'value': s} for s in structure_f[2:]]
by_t = [{'label': s, 'value': s} for s in structure_t]
by_r = [{'label': s, 'value': s} for s in structure_r[2:]]

all_f_data = []
for name in all_f_n:
	all_f_data.append(fighter_data(all_fight_data, name))

all_r_data = []
for name in all_r_n:
	all_r_data.append(referee_data(all_fight_data, name))


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.title = "Tomato"

app.layout = dbc.Container(
    [
        html.H1(
        	[	html.Img(src=r'assets/danatomato.png', style={'height':'6%', 'width':'6%'}, alt='image'),
        		"Tomato Dashboard",
        		html.Img(src=r'assets/samciggie.png', style={'height':'5%', 'width':'5%'}, alt='image')
        	], className="header-title"),
        html.P("“I bet every single card, just about every fight” -  James “The James Krause” Krause", className="header-description"),

        dbc.Row(
            [
                dbc.Col(
                	[
        				"Select Chart",
	                	dcc.Dropdown(id="filter_graph5", options=chart_names, value="Line"),
        				"Select Group",
	                	dcc.Dropdown(id="filter_graph1", options=group_names, value="Fighters"),
	                	"Select person(s)",
			            dcc.Dropdown(id="filter_graph2", value=["Sam Alvey ", "Francisco Trinaldo ", "Jon Jones "], multi=True),
	                	"By",
	                	dcc.Dropdown(id="filter_graph3", value="Finish score"),
	                	"Percentage",
			            dcc.Dropdown(id="filter_graph4", options=[{'label': s, 'value': s} for s in ["Yes", "No"]], value="No"),
                	],  md=2),
                dbc.Col(
                	dbc.Row([
                		dbc.Col(dcc.Graph(id="graph_line", config={"displayModeBar": False}), md=9),
                		dbc.Col(dash_table.DataTable(id="datatable1"), md=3),
                	]), md=10),

            ],
        ),
    ],
    fluid=True,
)

@app.callback(
    Output("datatable1", "data"),
    Output("datatable1", "columns"), 
    [Input("filter_graph1", "value"),
	Input("filter_graph3", "value")])
def update_datatable(group, value):

	if group == "Fighters":
		all_n = all_f_n
		all_data = all_f_data
		structure = structure_f

	elif group == "Referees":
		all_n = all_r_n
		all_data = all_r_data
		structure = structure_r_new

	data = []
	for i, name in enumerate(all_n):
		data.append([name] + all_data[i][1][-1])
	
	df = pd.DataFrame(data)
	# print(structure.index(value))
	# print(df)
	# print(df[[0, structure.index(value)]].sort_values(1))
	df = df[[0, structure.index(value)]]
	df = df.sort_values(structure.index(value))
	df = df[::-1].reset_index(drop=True)
	df.index += 1
	df = df.reset_index(level=0)
	df.columns = ["#", "Name", value]
	columns =  [{"name": i, "id": i,} for i in (df.columns)]

	return df[:15].to_dict('records'), columns

@app.callback(
    Output("filter_graph2", "options"),
    Output("filter_graph3", "options"),
    Output("filter_graph3", "value"),
    [Input("filter_graph1", "value"),
    Input("filter_graph3", "value")])
def update_filter_graph(value, by_value):
	if value == "Fighters":
		names = all_f_names
		by = by_f
		if by_value not in structure_f[2:]:
			by_value = "Finish score"
	else:
		names = all_r_names
		by = by_t
		if by_value not in structure_r_new[2:]:
			by_value = "Finish score"

	return names, by, by_value

@app.callback(
    Output("graph_line", "figure"), 
    [Input("filter_graph1", "value"),
    Input("filter_graph2", "value"),
	Input("filter_graph3", "value")])
def update_line_chart(group, names, value):
	if group == "Fighters":
		if 'Everyone' in names:
			names = all_f_n

		all_n = all_f_n
		all_data = all_f_data
		structure = structure_f

	elif group == "Referees":
		if "Everyone" in names:
			names = all_r_n

		all_n = all_r_n
		all_data = all_r_data
		structure = structure_r_new

	data = []
	for name in names:
		index = all_n.index(name)
		for fight in all_data[index][1]:
			data.append([name] + fight)
	
	if data != []:
		df = pd.DataFrame(data)
		df = df[[0, 1, structure.index(value)]]
		df.columns = ["Name", "Date", value]
	else:
		df = pd.DataFrame(data, columns=["Name", "Date", value])

	fig = px.line(df, x="Date", y=value, color="Name")
	return fig


if __name__ == "__main__":
    app.run_server(debug=True)