from dash import Dash, dcc, html, dash_table
from dash.dependencies import Output, Input

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

from functions import *

all_fight_data = open_data('all_fight_data')
all_f_data = open_data('all_f_data')
all_r_data = open_data('all_r_data')

all_f_names = all_fighter_names(all_fight_data)
all_r_names = all_referee_names(all_fight_data)

weight = ["Heavyweight", "Light Heavyweight", "Middleweight", "Welterweight", "Lightweight", "Featherweight", "Bantamweight", 
		  "Flyweight", "Women's Bantamweight", "Women's Strawweight", "Women's Flyweight", "Women's Featherweight", "Open Weight", "Super Heavyweight", "Catch Weight"]

weight_options = [{'label': s, 'value': s} for s in ['All'] + weight]
all_f_names_options = [{'label': s, 'value': s} for s in ['All'] + all_f_names]
all_r_names_options = [{'label': s, 'value': s} for s in ['All'] + all_r_names]

group_options = [{'label': s, 'value': s} for s in ["Fighters", "Referees"]]
chart_options = [{'label': s, 'value': s} for s in ["Line", "Bar"]]
yesno_options = [{'label': s, 'value': s} for s in ["Yes", "No"]]

structure_f = ["Name", "Date", "Winlose score", "KO/TKO", "Submission", "Decision", "Finish score", "Wins", "Losses", "Draws/NCs",
			   "Knockdowns", "Takedowns Landed", "Takedowns Attempted", "Reversals", "Submission Attempted", "Control Time"]
structure_r = ["Name", "Date", "KO/TKO", "Submission", "Decision", "Finish score"]

structure_t = ["KO/TKO", "Submission", "Decision", "Finish score"]

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
        html.Div(
            [
                dbc.CardBody(
                    [
		                dbc.Row(
		                    [
		                        dbc.Col(
		                            html.Img(src='assets/danatomato.png', width=180, height=150),
		                            width=2,
		                        ),
		                        dbc.Col(
		                            [
						                html.Div(
						                    [
						                        html.H1("Tomato Dashboard"),
						                        html.P("“I bet every single card, just about every fight” -  James “The James Krause” Krause"),
						                    ],
						                    className="text-center"
						                ),
		                            ],
		                            width=8,
		                            className="align-items-center justify-content-center"
		                        ),
		                        dbc.Col(
		                            html.Img(src='assets/samciggie.png', width=150, height=150),
		                            width=2,
		                        ),
		                    ],
		                    className="align-items-center",
		                )
                    ]
                )
            ],
        ),
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
                                        dcc.Dropdown(id="filter_graph_group", style=style_button, options=group_options, placeholder='Select Group', value='Referees'),
                                        dcc.Dropdown(id="filter_graph_person", style=style_button, placeholder='Select Person(s)', value=['Herb Dean', 'Keith Peterson'], multi=True),
                                        dcc.Dropdown(id="filter_graph_weight", style=style_button, options=weight_options, placeholder='Select Weight', multi=True),
                                        dcc.Dropdown(id="filter_graph_by", style=style_button, placeholder='Select Option', value='KO/TKO'),
                                        dcc.Dropdown(id="filter_graph_percentage", style=style_button, options=yesno_options, value='No'),
                                    ]
                                )
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
                dbc.Row(id="row-2"),
            ],
            # style={"padding": "20px"},
            fluid=True,
        ),
    ], 
    fluid=True,
    className="dbc"
)

@app.callback(
    Output("graph_line", "figure"), 
    [Input("filter_graph_group", "value"),
    Input("filter_graph_person", "value"),
	Input("filter_graph_by", "value")])
def update_line_chart(group, names, value):
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

	df= pd.DataFrame(all_data, columns=structure)
	df = df[df['Name'].isin(names)]

	fig = px.line(df, x="Date", y=value, color="Name")
	fig.update_layout(showlegend=False)
	return fig

@app.callback(
    Output("datatable1", "data"),
    Output("datatable1", "columns"),
    [Input("filter_graph_group", "value"),
	Input("filter_graph_by", "value")])
def update_datatable(group, value):
	if group == "Fighters":
		all_data = all_f_data
		structure = structure_f

	elif group == "Referees":
		all_data = all_r_data
		structure = structure_r

	df= pd.DataFrame(all_data, columns=structure)
	df = df.sort_values(by='Date', ascending=False)
	df = df.drop_duplicates(subset='Name', keep='first')
	df = df[["Name", value]]

	# print(df)
	df = df.sort_values(value, ascending=False).reset_index(drop=True)
	df.index += 1
	df = df.reset_index(level=0)
	df.columns = ["#", "Name", value]
	columns =  [{"name": i, "id": i,} for i in (df.columns)]

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