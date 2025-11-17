# callbacks.py
import pandas as pd
from dash import html, dcc, Output, Input
import plotly.graph_objects as go
from data_fetching import fetch_data
from recession_model import compute_recession_probability
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
        # ---------- FRED Macro ----------
        if selected_group == "FRED Macro":
            fred_cols = ["HY_OAS", "NFCI", "TOTALSL", "DGS2", "DGS10", "DGS30"]
            existing = [c for c in fred_cols if c in raw.columns]

            # df = raw[existing].dropna()
            df = raw[existing].sort_index().asfreq("D").ffill()
            # Normalize by max value per series for raw display
            df_norm = df / df.abs().max()
            # calculate z score
            z = compute_zscore(df)
            
            return html.Div([
                dcc.Graph(figure=make_timeseries_panel(df_norm, "Macro Levels")),
                dcc.Graph(figure=make_timeseries_panel(z, "Macro Z-Scores"))
            ])
        # -----------------------------------------------------
        # RECESSION PANEL
        # -----------------------------------------------------
        if selected_group == "Recession Risk":

            p = compute_recession_probability()

            # --- unpack the recession model results ---
            prob = p["probability"]            # float
            z_dict = p["z"]                    # dict of floats
            raw_dict = p["raw"]                # dict of pd.Series

            # =====================================================
            # 1) PROBABILITY GAUGE
            # =====================================================
            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                gauge={
                    "axis": {"range": [0, 100]},
                    "steps": [
                        {"range": [0, 30], "color": "#2ca02c"},
                        {"range": [30, 50], "color": "#1f77b4"},
                        {"range": [50, 70], "color": "#ff7f0e"},
                        {"range": [70, 100], "color": "#d62728"},
                    ],
                    "bar": {"color": "white"},
                },
                title={"text": "Recession Probability (2026–27)"}
            ))
            gauge.update_layout(template="plotly_dark", height=300)

            # =====================================================
            # 2) RAW COMPONENT PANEL (time series)
            # =====================================================
            # Convert raw dict to DataFrame for plotting
            raw_df = pd.DataFrame(raw_dict)
            raw_df = raw_df.sort_index().asfreq("D").ffill()

            fig_raw = go.Figure()
            for col in raw_df.columns:
                fig_raw.add_trace(go.Scatter(
                    x=raw_df.index,
                    y=raw_df[col],
                    mode="lines",
                    name=col
                ))
            fig_raw.update_layout(
                title="Recession Model Inputs — Raw Levels",
                template="plotly_dark",
                height=400
            )

            # =====================================================
            # 3) Z-SCORE PANEL (bar chart)
            # =====================================================
            z_df = pd.DataFrame.from_dict(z_dict, orient="index", columns=["Z-Score"])

            fig_z = go.Figure()
            fig_z.add_trace(go.Bar(
                x=z_df.index,
                y=z_df["Z-Score"],
                name="Z-Scores"
            ))
            fig_z.update_layout(
                title="Component Z-Scores",
                template="plotly_dark",
                height=400
            )

            # Return three visual elements vertically stacked
            return html.Div([
                dcc.Graph(figure=gauge),
                dcc.Graph(figure=fig_raw),
                dcc.Graph(figure=fig_z),
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
