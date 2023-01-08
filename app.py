from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from functions import *

import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

all_fight_data = open_data('all_fight_data')

all_f_n = all_fighter_names(all_fight_data)
all_f_n_options = ['All'] + all_f_n
all_f_names = [{'label': s, 'value': s} for s in all_f_n_options]

all_r_n = all_referee_names(all_fight_data)
all_r_n_options = ['All'] + all_r_n
all_r_names = [{'label': s, 'value': s} for s in all_r_n_options]

group_names = [{'label': s, 'value': s} for s in ["Fighters", "Referees"]]
chart_names = [{'label': s, 'value': s} for s in ["Line", "Bar"]]

weight = ["Heavyweight", "Light Heavyweight", "Middleweight",
          "Welterweight", "Lightweight", "Featherweight", "Bantamweight", 
          "Flyweight", "Women's Bantamweight", "Women's Strawweight", 
          "Women's Flyweight", "Women's Featherweight", "Open Weight", 
         "Super Heavyweight", "Catch Weight"]
weight_names = [{'label': s, 'value': s} for s in ['All'] + weight]

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
        	[	
        		html.Img(src=r'assets/danatomato.png', style={'height':'6%', 'width':'6%'}, alt='image'),
        		"Tomato Dashboard",
        		html.Img(src=r'assets/samciggie.png', style={'height':'5%', 'width':'5%'}, alt='image')
        	], className="header-title"),
        html.P("“I bet every single card, just about every fight” -  James “The James Krause” Krause", className="header-description"),

        dbc.Row(
            [
                dbc.Col(
                	[
        				"Select Chart (doesnt work)",
	                	dcc.Dropdown(id="filter_graph5", options=chart_names, value="Line"),
        				"Select Group",
	                	dcc.Dropdown(id="filter_graph1", options=group_names, value="Fighters"),
	                	"Select person(s)",
			            dcc.Dropdown(id="filter_graph2", value=["Sam Alvey ", "Francisco Trinaldo ", "Jon Jones "], multi=True),
	                	"Select Weight class (doesnt work)",
	                	dcc.Dropdown(id="filter_graph6", options=weight_names, value="Lightweight", multi=True),
	                	"By",
	                	dcc.Dropdown(id="filter_graph3", value="Finish score"),
	                	"Percentage (doesnt work)",
			            dcc.Dropdown(id="filter_graph4", options=[{'label': s, 'value': s} for s in ["Yes", "No"]], value="No"),
                	], md=2, className=["wrapper", "card"]),
                dbc.Col(
                	dbc.Row([
                		dbc.Col(dcc.Graph(id="graph_line", config={"displayModeBar": False}), md=8, className=["wrapper", "card"]),
						dbc.Col(dash_table.DataTable(id="datatable1", style_table={'overflowY': 'scroll', 'height': '400px'},
							style_cell_conditional=[
				    			{	
						            'if': {'column_id': 'Name'},
						            'textAlign': 'left',
						            'padding-left': '30px'
						        },
					        ],
						    style_as_list_view=True,
						), md=4, className=["wrapper", "card"]), 
                	]), md=10),

            ],
        ),
        dbc.Row(
            [
                html.Ul(
                	[
                		html.Li("Winlose score: Win - Lose"),
                		html.Li("Finish score: KO/TKO + Submission - Decision. Wins only. "),
                	])

            ], className=["wrapper-text", "card"]),
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
	df = df[[0, structure.index(value)]]
	df = df.sort_values(structure.index(value))
	df = df[::-1].reset_index(drop=True)
	df.index += 1
	df = df.reset_index(level=0)
	df.columns = ["#", "Name", value]
	columns =  [{"name": i, "id": i,} for i in (df.columns)]

	return df[:100].to_dict('records'), columns

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
		if 'All' in names:
			names = all_f_n

		all_n = all_f_n
		all_data = all_f_data
		structure = structure_f

	elif group == "Referees":
		if "All" in names:
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
	fig.update_layout(showlegend=False)
	return fig


if __name__ == "__main__":
    app.run_server(debug=True)