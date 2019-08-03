import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from plots.show_funds import fund_data_layout
from plots.efficirnt_frontier import efficient_frontier_data_layout

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
# Create global chart template
mapbox_access_token = "pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w"

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-78.05, lat=42.54),
        zoom=7,
    ),
)

config = {
    'risk_range': range(0, 7)
}

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dash-logo.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "AI-Investment Advisor",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Deecamp 36", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Learn More", id="learn-more-button"),
                            href="https://plot.ly/dash/pricing/",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Choose your risk:",
                            className="control_label",
                        ),
                        dcc.Slider(
                            id="risk_slider",
                            min=min(config['risk_range']),
                            max=max(config['risk_range']),
                            value=min(config['risk_range']),
                            marks={i: '{}'.format(i) for i in config['risk_range']},
                            className="dcc_control",
                        ),
                        html.P("Filter by well status:", className="control_label"),
                        dcc.RadioItems(
                            id="well_status_selector",
                            options=[
                                {"label": "All ", "value": "all"},
                                {"label": "Active only ", "value": "active"},
                                {"label": "Customize ", "value": "custom"},
                            ],
                            value="active",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="well_statuses",
                            options=[
                                {'label': 1, 'value': 1}
                            ],
                            multi=True,
                            value=[1],
                            className="dcc_control",
                        ),
                        dcc.Checklist(
                            id="lock_selector",
                            options=[{"label": "Lock camera", "value": "locked"}],
                            className="dcc_control",
                        ),
                        html.P("Filter by well type:", className="control_label"),
                        dcc.RadioItems(
                            id="well_type_selector",
                            options=[
                                {"label": "All ", "value": "all"},
                                {"label": "Productive only ", "value": "productive"},
                                {"label": "Customize ", "value": "custom"},
                            ],
                            value="productive",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="well_types",
                            options=[
                                {'label': 1, 'value': 1}
                            ],
                            multi=True,
                            value=[1],
                            className="dcc_control",
                        ),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="fund_text"), html.P("No. of Funds")],
                                    id="funds",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="return_text"), html.P("Return")],
                                    id="return",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="volatility_text"), html.P("Volatility")],
                                    id="oil",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="sharp_text"), html.P("Sharp Ratio")],
                                    id="sharp",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="count_graph")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="main_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="individual_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="pie_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="aggregate_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

# @app.callback(
#     [Output('show-funds', 'figure'),
#      Output('risk-text', 'children')],
#     [Input('risk-slider', 'value')]
# )
# def update_risk(risk_val):
#     return fund_data_layout(risk_val), '您选择的风险值为: {}'.format(risk_val)
#
#
# @app.callback(
#     Output('efficient-frontier', 'figure'),
#     [Input('show-funds', 'selectedData'),
#      Input('show-funds', 'clickData')]
# )
# def update_select(selectedData, clickData):
#     if selectedData is None and clickData is None:
#         return efficient_frontier_data_layout('all')
#     selected_points = set(selectedData['points']) if selectedData is not None else set()
#     click_points = set(clickData['points']) if clickData is not None else set()
#     points = selected_points | click_points
#     selected_fund_code = [p['code'] for p in points]
#     return efficient_frontier_data_layout(selected_fund_code)


if __name__ == '__main__':
    app.run_server(debug=True)
