from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from functions import *

import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

all_fight_data = open_data('all_fight_data')

all_f_n = all_fighter_names(all_fight_data)
all_f_names = [{'label': s, 'value': s} for s in all_f_n]

all_r_names = all_referee_names(all_fight_data)
all_r_names = [{'label': s, 'value': s} for s in all_r_names]

group_names = [{'label': s, 'value': s} for s in ["Fighters", "Referees"]]

structure = ["Fighter", "Date", "KO/TKO", "Submission", "Decision", "Winlose score", "Finish score"]
structure_t = ["KO/TKO", "Submission", "Decision", "Finish score"]
structure_r = ["Ref", "Date", "Method"]
by = [{'label': s, 'value': s} for s in structure[2:]]
by_t = [{'label': s, 'value': s} for s in structure_t]
by_r = [{'label': s, 'value': s} for s in structure_r[2:]]


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.title = "Dojo"

app.layout = dbc.Container(
    [
        html.H1("Dojo Dashboard", className="header-title"),
        html.P("Dashboard for mma analytics", className="header-description"),
        dbc.Row(
            [
                dbc.Col(
                		dbc.Row(
		                	[
			                	"Select Group",
			                	dcc.Dropdown(id="filter_table1", options=group_names, value="Referees"),
			                	"By",
			                	dcc.Dropdown(id="filter_table2", options=by_t, value="Finish score"),
			                	dash_table.DataTable(id="datatable1"),
			                ],
                		),  md=3),
                dbc.Col(
                	[
		                dbc.Row(
		                	[
			                	dbc.Col(dcc.Graph(id="graph_line", config={"displayModeBar": False}), md=9),
			                	dbc.Col(
			                		[
			                			"Select Group",
			                			dcc.Dropdown(id="filter_line1", options=group_names, value="Fighters"),
			                			"Select person(s)",
			                			dcc.Dropdown(id="filter_line2", options=all_f_names, value=["Francisco Trinaldo ", "Michael Bisping ", "Jon Jones "], multi=True),
			                			"By",
			                			dcc.Dropdown(id="filter_line3", options=by, value="Finish score"),
			                		], md=3),
			                ],
		                ),
		                dbc.Row(
		                	[
			                	dbc.Col(dcc.Graph(id="graph_bar", config={"displayModeBar": False}), md=9),
			                	dbc.Col(
			                		[
			                			"Select Group",
			                			dcc.Dropdown(id="filter_bar1", options=group_names, value="Referees"),
			                			"Subject",
			                			dcc.Dropdown(id="filter_bar2", options=by_r, value="Method"),
			                			"Percentage",
			                			dcc.Dropdown(id="filter_bar3", options=[{'label': s, 'value': s} for s in ["Yes", "No"]], value="No"),
			                		], md=3),
			                	
			                ],
		                ),
                	], md=9),

            ],
            align="center",
        ),
    ],
    fluid=True,
)

@app.callback(
    Output("graph_line", "figure"), 
    [Input("filter_line1", "value"),
    Input("filter_line2", "value"),
	Input("filter_line3", "value")])
def update_line_chart(group, names, value):
	data = []
	for name in names:
		data += fighter_data(all_fight_data, name, structure.index(value))

	df = pd.DataFrame(data, columns=["Fighter", "Date", value])
	fig = px.line(df, x="Date", y=value, color='Fighter')
	return fig

@app.callback(
    Output("graph_bar", "figure"), 
    [Input("filter_bar1", "value"),
	Input("filter_bar2", "value"),
	Input("filter_bar3", "value")])
def update_bar_chart(group, by_value, percentage):

	b_data = bar_data(all_fight_data, group)
	data = []
	for row in b_data:
		numbers = [row[1], row[2], row[3]]
		total = sum(numbers)

		if group == 'Fighters' or total > 100:
			if percentage == "Yes":
				numbers = [int(x/total*100) for x in numbers]

			data.append(go.Bar(name=row[0], x=["KO/TKO", "Submission", "Decision"], y=numbers))

	fig = go.Figure(data=data)
	return fig

@app.callback(
    Output("datatable1", "data"),
    Output("datatable1", "columns"), 
    [Input("filter_table1", "value"),
	Input("filter_table2", "value")])
def update_datatable(group, by_value):

	if group == "Referees":

		b_data = bar_data(all_fight_data, 'Referees')
		df = pd.DataFrame(b_data)

		index = structure_t.index(by_value) + 1
		df = df[[0,index]].sort_values(index)[::-1].reset_index(drop=True)

	else:
		data = []
		for name in all_f_n:
			data.append(fighter_data(all_fight_data, name, structure.index(by_value)))

		table_data = []
		for i, fighter in enumerate(data):
			count = fighter[-1][2]
			table_data.append([fighter[0][0], count])
			index = 2
		
		df = pd.DataFrame(table_data).sort_values(1)
		df = df[::-1].reset_index(drop=True)
	
	df.index += 1
	df = df.reset_index(level=0)

	df.columns = ["#", "Name", by_value]
	columns =  [{"name": i, "id": i,} for i in (df.columns)]
	
	return df[:30].to_dict('records'), columns


if __name__ == "__main__":
    app.run_server(debug=True)