# callbacks.py
from dash import html, dcc, Output, Input
from data_fetching import fetch_data
from indicators import compute_zscore, add_credit_ratio, compute_stress_score
from figures import make_timeseries_panel, make_stress_gauge
from signal_guide import SIGNAL_GUIDE_TEXT

def register_callbacks(app, RISK_TICKERS):

    @app.callback(
        Output("panel-output", "children"),
        Input("tabs", "value"),
        Input("refresh", "n_intervals")
    )
    def update_panel(selected_group, n):

        # ---------- ALWAYS FETCH DATA FIRST ----------
        raw = fetch_data(RISK_TICKERS)

        # ---------- SIGNAL GUIDE ----------
        if selected_group == "Signal Guide":
            return html.Div([
                dcc.Markdown(SIGNAL_GUIDE_TEXT, style={
                    "padding": "20px",
                    "whiteSpace": "pre-wrap",
                    "overflowY": "scroll",
                    "height": "800px"
                })
            ])

        # ---------- STRESS SCORE PANEL ----------
        if selected_group == "Stress Score":

            raw = add_credit_ratio(raw)
            z = compute_zscore(raw)
            MSS = compute_stress_score(z)

            if MSS.empty:
                return html.Div([
                    html.H3("Stress Score unavailable"),
                    html.P(
                        "Data for required indicators could not be fetched. "
                        "If using Render, Yahoo may temporarily block rate-limited endpoints. "
                        "Please refresh or wait a few seconds.",
                        style={"color": "orange"}
                    )
                ])

            gauge = make_stress_gauge(
                MSS.iloc[-1]["Stress Score"],
                MSS["Stress Score"].mean()
            )
            line = make_timeseries_panel(MSS, "Stress Score Trend")

            return html.Div([dcc.Graph(figure=gauge), dcc.Graph(figure=line)])

        # ---------- REGULAR PANELS ----------
        raw = add_credit_ratio(raw)
        cols = (
            ["HYG", "JNK", "LQD", "HYG/LQD"]
            if selected_group == "Credit Risk"
            else RISK_TICKERS[selected_group]
        )

        # Keep only tickers that exist in yahooquery output
        existing_cols = [c for c in cols if c in raw.columns]

        if not existing_cols:
            return html.Div([
                html.H3(f"No data found for {selected_group}"),
                html.P("Yahooquery did not return any valid tickers.",
                       style={"color": "orange"})
            ])

        df = raw[existing_cols].dropna()
        z = compute_zscore(df)

        return html.Div([
            dcc.Graph(figure=make_timeseries_panel(df, f"{selected_group} — Levels")),
            dcc.Graph(figure=make_timeseries_panel(z, f"{selected_group} — Z-Scores"))
        ])
