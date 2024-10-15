import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots
from django.shortcuts import render
from plotlyapp.gwr_chart_data import (
    epds_demand_chart_data,
    treatment_additions_chart_data,
    modelled_demand_chart_data,
    production_flow_RM_chart_data,
    epds1_constituents_chart_data,
)


def gwr_chart(request):
    ######################epds demand chart end#################################
    x_data_time, y_data_g, y_data_h, y_data_i, y_data_bd, y_data_bt = (
        epds_demand_chart_data()
    )
    # Create a DataFrame to handle large data and aggregation
    df = pd.DataFrame(
        {
            "Time": pd.to_datetime(x_data_time, format="%H:%M:%S"),
            "EPDS 1 Demand": y_data_g,
            "EPDS 2 Demand": y_data_h,
            "EPDS 3 Demand": y_data_i,
            "Production Rate To Red": y_data_bd,
            "Production Rate To RM": y_data_bt,
        }
    )

    # Resample the DataFrame to adjust intervals (if needed)
    df.set_index("Time", inplace=True)
    df_resampled = df.resample("1T").mean()  # Resample every 1 minute and take the mean

    # Create traces for the demand curves
    trace_g = go.Scatter(
        x=df_resampled.index,
        y=df_resampled["EPDS 1 Demand"],
        mode="lines+markers",
        name="EPDS 1 Demand (Gallons)",
        line=dict(shape="spline", width=2),
    )
    trace_h = go.Scatter(
        x=df_resampled.index,
        y=df_resampled["EPDS 2 Demand"],
        mode="lines+markers",
        name="EPDS 2 Demand (Gallons)",
        line=dict(shape="spline", width=2),
    )
    trace_i = go.Scatter(
        x=df_resampled.index,
        y=df_resampled["EPDS 3 Demand"],
        mode="lines+markers",
        name="EPDS 3 Demand (Gallons)",
        line=dict(shape="spline", width=2),
    )
    # trace_bd = go.Scatter(
    #     x=df_resampled.index,
    #     y=df_resampled["Production Rate To Red"],
    #     mode="lines+markers",
    #     name="Production Rate To Red",
    #     line=dict(shape="spline", width=2),
    # )
    # trace_bt = go.Scatter(
    #     x=df_resampled.index,
    #     y=df_resampled["Production Rate To RM"],
    #     mode="lines+markers",
    #     name="Production Rate To RM",
    #     line=dict(shape="spline", width=2),
    # )

    # Layout for the chart
    layout = go.Layout(
        title="Demand Curve for EPDS and Production Rate",
        xaxis=dict(title="Time"),
        yaxis=dict(title="Demand, GPM", range=[0, 12000]),
        autosize=False,
        width=800,  # Adjust the chart width
        height=500,  # Adjust the chart height
    )

    # Create the figure
    # fig = go.Figure(data=[trace_g, trace_h, trace_i, trace_bd, trace_bt], layout=layout)

    fig = go.Figure(
        data=[
            trace_g,
            trace_h,
            trace_i,
        ],
        layout=layout,
    )

    # Convert the figure to HTML
    epds_demand_chart_html = pio.to_html(fig, full_html=False)

    ######################epds demand chart end#################################
    #######################treatment addition stack chart start#################################
    (
        x_data_time,
        y_data_rm_tp_added,
        y_data_nn_added,
        y_data_ne_added,
        y_data_nw_added,
        y_data_v_added,
        y_data_ne_treatment_added,
        y_data_s_added,
        y_data_ne_nn_treatment_added,
        y_data_glennwilde_added,
    ) = treatment_additions_chart_data()
    # Create a DataFrame to handle the data
    df = pd.DataFrame(
        {
            "Time": pd.to_datetime(x_data_time, format="%H:%M:%S"),
            "RM TP added": y_data_rm_tp_added,
            "NN added": y_data_nn_added,
            "NE added": y_data_ne_added,
            "NW added": y_data_nw_added,
            "V added": y_data_v_added,
            "NE TREATMENT ADDED": y_data_ne_treatment_added,
            "s added": y_data_s_added,
            "NE + NN TREATMENT ADDED": y_data_ne_nn_treatment_added,
            "Glennwilde added": y_data_glennwilde_added,
        }
    )

    # Set the index for the DataFrame
    df.set_index("Time", inplace=True)

    colors = [
        "#FF6347",  # Tomato
        "#8B008B",  # Dark Magenta
        "#008080",  # Teal
        "#4682B4",  # Steel Blue
        "#2E8B57",  # Sea Green
        "#A52A2A",  # Brown
        "#FFFF00",  # Yellow
        "#00008B",  # Dark Blue
        "#808080",  # Grey
    ]

    # Create traces for the stacked area chart with custom colors
    traces = []
    for i, column in enumerate(df.columns):
        traces.append(
            go.Scatter(
                x=df.index,
                y=df[column],
                mode="none",  # Use 'none' for area traces
                name=column,
                stackgroup="one",  # Group the areas together
                opacity=0.6,
                fillcolor=colors[i % len(colors)],  # Cycle through the color list
            )
        )

    # Adjust x-axis to reduce the time interval and improve readability
    layout = go.Layout(
        title="Production Flow To Red Chart",
        xaxis=dict(
            title="Time",
            # dtick=3600000,  # Set x-axis tick interval to 1 hour (3600000 milliseconds)
            # tickformat="%H:%M",  # Format as hour and minute
        ),
        yaxis=dict(title="Amount Added", range=[0, 7000]),
        autosize=False,
        width=800,  # Adjust the chart width
        height=500,  # Adjust the chart height
    )

    # Create the figure
    fig = go.Figure(data=traces, layout=layout)

    # Convert the figure to HTML
    treatment_addition_chart_html = pio.to_html(fig, full_html=False)

    #######################treatment addition stack chart end#################################
    #######################production flow RM stack chart start#################################
    (
        x_data_time,
        y_data_sorrento_east_added,
        y_data_rm1_added,
        y_data_rm2_added,
    ) = production_flow_RM_chart_data()
    # Create a DataFrame to handle the data
    df = pd.DataFrame(
        {
            "Time": pd.to_datetime(x_data_time, format="%H:%M:%S"),
            "Sorrento East added": y_data_sorrento_east_added,
            "RM 1 added": y_data_rm1_added,
            "RM 2 added": y_data_rm2_added,
        }
    )

    # Set the index for the DataFrame
    df.set_index("Time", inplace=True)

    colors = [
        "#008080",  # Teal
        "#4682B4",  # Steel Blue
        "#2E8B57",  # Sea Green
    ]

    # Create traces for the stacked area chart with custom colors
    traces = []
    for i, column in enumerate(df.columns):
        traces.append(
            go.Scatter(
                x=df.index,
                y=df[column],
                mode="none",  # Use 'none' for area traces
                name=column,
                stackgroup="one",  # Group the areas together
                opacity=0.6,
                fillcolor=colors[i % len(colors)],  # Cycle through the color list
            )
        )

    # Adjust x-axis to reduce the time interval and improve readability
    layout = go.Layout(
        title="Production Flow To RM Chart",
        xaxis=dict(
            title="Time",
            # dtick=3600000,  # Set x-axis tick interval to 1 hour (3600000 milliseconds)
            # tickformat="%H:%M",  # Format as hour and minute
        ),
        yaxis=dict(title="Amount Added", range=[0, 4000]),
        autosize=False,
        width=800,  # Adjust the chart width
        height=500,  # Adjust the chart height
    )

    # Create the figure
    fig = go.Figure(data=traces, layout=layout)

    # Convert the figure to HTML
    production_flow_RM_chart_html = pio.to_html(fig, full_html=False)

    #######################production flow RM stack chart end#################################

    #######################modelled demand stack chart start#################################

    (x_data, y_total, y_red, y_rm, y_groves) = modelled_demand_chart_data()
    # Create a DataFrame to handle the data
    df = pd.DataFrame(
        {
            "Time": x_data,
            # "Total": y_total,
            "RED": y_red,
            "RM": y_rm,
            "Groves": y_groves,
        }
    )

    # Set the index for the DataFrame
    df.set_index("Time", inplace=True)

    colors = [
        "#008080",  # Teal
        # "#4682B4",  # Steel Blue
        "#8B008B",  # Dark Magenta
        "#2E8B57",  # Sea Green
    ]

    # Create traces for the stacked area chart with custom colors
    traces = []
    for i, column in enumerate(df.columns):
        traces.append(
            go.Scatter(
                x=df.index,
                y=df[column],
                mode="none",  # Use 'none' for area traces
                name=column,
                stackgroup="one",  # Group the areas together
                opacity=0.6,
                fillcolor=colors[i % len(colors)],  # Cycle through the color list
            )
        )

    # Adjust x-axis to reduce the time interval and improve readability
    layout = go.Layout(
        title="Modelled demand Chart",
        xaxis=dict(
            title="Model Day",
            # dtick=3600000,  # Set x-axis tick interval to 1 hour (3600000 milliseconds)
            # tickformat="%H:%M",  # Format as hour and minute
        ),
        yaxis=dict(title="Demand (GPD)"),
        autosize=False,
        width=800,  # Adjust the chart width
        height=500,  # Adjust the chart height
    )

    # Create the figure
    fig = go.Figure(data=traces, layout=layout)

    # Convert the figure to HTML
    modelled_demand_chart_html = pio.to_html(fig, full_html=False)

    #######################modelled demand stack chart end#################################

    #######################epds1 constituents chart start#################################
    x_data_time, y_data_as, y_data_no3, y_data_f, y_data_u, y_data_tds = (
        epds1_constituents_chart_data()
    )

    # Create a DataFrame to handle large data and aggregation
    df = pd.DataFrame(
        {
            "Time": pd.to_datetime(x_data_time, format="%H:%M:%S"),
            "Resultant As (mg/L)": y_data_as,
            "Resultant NO3 (mg/L)": y_data_no3,
            "Resultant F (mg/L)": y_data_f,
            "Resultant U (mg/L)": y_data_u,
            "Resultant TDS (mg/L)": y_data_tds,
        }
    )

    # Resample the DataFrame to adjust intervals (if needed)
    df.set_index("Time", inplace=True)
    df_resampled = df.resample("1T").mean()  # Resample every 1 minute and take the mean

    # Create a subplot with two y-axes
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces for the constituents on the primary y-axis
    fig.add_trace(
        go.Scatter(
            x=df_resampled.index,
            y=df_resampled["Resultant As (mg/L)"],
            mode="lines+markers",
            name="Resultant As (mg/L)",
            line=dict(shape="spline", width=2),
        ),
        secondary_y=False,  # Primary y-axis
    )

    fig.add_trace(
        go.Scatter(
            x=df_resampled.index,
            y=df_resampled["Resultant NO3 (mg/L)"],
            mode="lines+markers",
            name="Resultant NO3 (mg/L)",
            line=dict(shape="spline", width=2),
        ),
        secondary_y=False,  # Primary y-axis
    )

    fig.add_trace(
        go.Scatter(
            x=df_resampled.index,
            y=df_resampled["Resultant F (mg/L)"],
            mode="lines+markers",
            name="Resultant F (mg/L)",
            line=dict(shape="spline", width=2),
        ),
        secondary_y=False,  # Primary y-axis
    )

    fig.add_trace(
        go.Scatter(
            x=df_resampled.index,
            y=df_resampled["Resultant U (mg/L)"],
            mode="lines+markers",
            name="Resultant U (mg/L)",
            line=dict(shape="spline", width=2),
        ),
        secondary_y=False,  # Primary y-axis
    )

    # Add trace for TDS on the secondary y-axis
    fig.add_trace(
        go.Scatter(
            x=df_resampled.index,
            y=df_resampled["Resultant TDS (mg/L)"],
            mode="lines+markers",
            name="Resultant TDS (mg/L)",
            line=dict(shape="spline", width=2),
        ),
        secondary_y=True,  # Secondary y-axis
    )

    # Update layout with titles and axis properties
    fig.update_layout(
        title="EPDS1 constituents chart",
        xaxis=dict(title="Time"),
        yaxis=dict(
            title="Constituents Concentration (mg/L)", range=[0, 40]
        ),  # Primary y-axis
        yaxis2=dict(
            title="Resultant TDS (mg/L)", overlaying="y", side="right", range=[0, 1400]
        ),  # Secondary y-axis
        autosize=False,
        width=800,  # Adjust the chart width
        height=500,  # Adjust the chart height
    )

    # Convert the figure to HTML
    epds1_constituents_chart_html = pio.to_html(fig, full_html=False)

    #######################epds1 constituents chart end#################################

    # Render the template with the chart HTML
    return render(
        request,
        "gwr_chart.html",
        {
            "gwr_epds_demand_chart": epds_demand_chart_html,
            "gwr_treatment_addition_chart": treatment_addition_chart_html,
            "gwr_production_flow_RM_chart": production_flow_RM_chart_html,
            "gwr_modelled_demand_chart": modelled_demand_chart_html,
            "gwr_epds1_constituents_chart": epds1_constituents_chart_html,
        },
    )
