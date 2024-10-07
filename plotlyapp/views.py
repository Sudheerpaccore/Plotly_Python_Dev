import csv
from django.shortcuts import render
import plotly.express as px
import plotly.graph_objects as go
from .models import SalesData
import pandas as pd
from plotly.offline import plot
from plotly.subplots import make_subplots

#loading the csv data into models
def load_csv_data(file_path):
    """ Load data from CSV and insert into the SalesData model. """
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Create SalesData entries based on CSV rows
            SalesData.objects.create(
                product=row['product'],
                month=row['month'],
                sales=int(row['sales'])
            )


#line chart
def differentiated_chart(request):
    # Load CSV data into the model (only once, check if data exists)
    if not SalesData.objects.exists():
        file_path = 'plotlyapp/sales_data.csv'  # Adjust this path
        load_csv_data(file_path)

    # Query data from the database
    data = SalesData.objects.all().values('product', 'sales', 'month').order_by('id')
    print(type(data), data, "salesdata")
    # Convert data to a DataFrame for use with Plotly
    data_list = list(data)
    df = pd.DataFrame(data_list)
    print(df, "dataframe")
    # Differentiation logic: color-code based on sales
    df['color'] = df['sales'].apply(lambda x: 'blue' if x > 100 else 'red')
    print(df,"Dfffcolor")
    # Create a line chart using Plotly with color differentiation
    fig = px.line(
        df, 
        x='month', 
        y='sales', 
        color='color', 
        line_shape='linear',
        title="Monthly Sales with Differentiation",
        markers=True
    )
    # Customize the chart to disable zoom, pan, and other navigation tools
    config = {
        'displayModeBar': True,  # Show the toolbar
        'modeBarButtonsToRemove': [
            'zoom', 'pan', 'select2d', 'lasso2d', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale','toImage'
        ],
        'displaylogo': False  # Hide the Plotly logo
    }
    
    # Customize the layout (optional)
    fig.update_traces(marker=dict(size=12), line=dict(width=4))
    fig.update_layout(showlegend=True)

   
    # Convert the figure to HTML
    chart_html = fig.to_html(full_html=False, config=config)

    # Render the template with the chart
    return render(request, 'plotly_chart.html', {'chart': chart_html})


#BAR chart
def plotly_bar_view(request):
    data = SalesData.objects.all().values('product', 'sales', 'month').order_by('id')
    print(type(data), data, "salesdata")
    # Convert data to a DataFrame for use with Plotly
    data_list = list(data)
    df = pd.DataFrame(data_list)
    print(df, "dataframe")
    # Differentiation logic: color-code based on sales
    df['color'] = df['sales'].apply(lambda x: 'blue' if x > 100 else 'red')
    print(df,"Dfffcolor")
    
   
    # for displaying the bar chart
    fig = px.bar(
        df, 
        x='month', 
        y='sales', 
        color='color', 
        # line_shape='linear',
        title="Monthly Sales with Differentiation",
        # markers=True
        hover_data={'sales': True, 'month': True}
    )

    config = {
        'displayModeBar': True,  # Show the toolbar
        'modeBarButtonsToRemove': [
            'zoom', 'pan', 'select2d', 'lasso2d', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale','toImage'
        ],
        'displaylogo': False  # Hide the Plotly logo
    }
    # Convert the figure to HTML
    chart_html = fig.to_html(full_html=False, config=config)

    # Render the template with the chart
    return render(request, 'plotly_bar.html', {'bar_chart': chart_html})


#pie chart
def plotly_pie_view(request):
    # Query data from the database
    data = SalesData.objects.all().values('product', 'sales', 'month').order_by('id')
    print(type(data), data, "salesdata")
    # Convert data to a DataFrame for use with Plotly
    data_list = list(data)
    df = pd.DataFrame(data_list)
    print(df, "dataframe")
    # Differentiation logic: color-code based on sales
    df['color'] = df['sales'].apply(lambda x: 'blue' if x > 100 else 'red')
    print(df,"Dfffcolor")
    
    # fig.show(config={'staticPlot': True})
    #for displaying the pie chart
    fig = px.pie(
        df, 
        names='product',   # This is the label/category for each slice
        values='sales',    # This is the value that determines the size of each slice
        # line_shape='linear',
        title="Monthly Sales with Differentiation",
        # markers=True
    )
    config = {
        'displayModeBar': True,  # Show the toolbar
        'modeBarButtonsToRemove': [
            'zoom', 'pan', 'select2d', 'lasso2d', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale','toImage'
        ],
        'displaylogo': False  # Hide the Plotly logo
    } 
    # Convert the figure to HTML
    chart_html = fig.to_html(full_html=False, config=config)

    # Render the template with the chart
    return render(request, 'plotly_pie.html', {'pie_chart': chart_html})


def plotly_curve(request):
    fig = go.Figure()
 # # Create a custom legend below the chart using go.Figure
    fig.add_trace(go.Scatter(
        x=[1,2,3], y=[4,5,6],
        mode='markers',
        marker=dict(size=12, color='green'),
        legendgroup='Green',
        showlegend=True,
        name='Sales > 100'
    ))

    # fig.add_trace(go.Scatter(
    #     x=[None], y=[None],
    #     mode='markers',
    #     marker=dict(size=12, color='red'),
    #     legendgroup='Red',
    #     showlegend=True,
    #     name='Sales <= 100'
    # ))

    # # Position the custom legend below the chart
    fig.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",
            y=-0.25,  # Position the legend below x-axis
            xanchor="center",
            x=0.5
        )
    )
    graph_json = fig.to_html(full_html=False)

    # Pass to template
    context = {'pie_chart': graph_json}
    return render(request, 'plotly_pie.html', context)



def generate_charts():
    # Create subplots for your 3 different charts
    fig = make_subplots(rows=1, cols=1, subplot_titles=("Demand Curve"))
    
    # First graph (line chart - Demand Curve)
    fig.add_trace(go.Scatter(x=['2024-09-05', '2024-09-06', '2024-09-07','2024-09-08','2024-09-09','2024-09-10','2024-09-11'],
                             y=[1000, 1500, 2000, 2500, 3000, 3500, 4000],
                             mode='lines',
                            #  fill='tozeroy',
                             name='EPDS 1 Demand (gallons)',line=dict(shape='spline', color='red')),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=['2024-09-05', '2024-09-06', '2024-09-07','2024-09-08','2024-09-09','2024-09-10','2024-09-11'],
                             y=[1500, 2000, 2500, 3000, 3500, 4000, 4500],
                            #  mode='lines',
                             fill='tonexty',
                             name='EPDS 2 Demand (gallons)',line=dict(shape='spline', color='orange')),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=['2024-09-05', '2024-09-06', '2024-09-07','2024-09-08','2024-09-09','2024-09-10','2024-09-11'],
                             y=[1500, 2500, 3500, 1000, 4000, 4500, 5000],
                             mode='lines',
                             name='EPDS 3 Demand (gallons)',line=dict(shape='spline', color='blue')),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=['2024-09-05', '2024-09-06', '2024-09-07','2024-09-08','2024-09-09','2024-09-10','2024-09-11'],
                             y=[2000, 2500, 3000, 4500, 1000, 2000, 4000],
                             mode='lines',
                             name='EPDS 4 Demand (gallons)',line=dict(shape='spline', color='purple')),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=['2024-09-05', '2024-09-06', '2024-09-07','2024-09-08','2024-09-09','2024-09-10','2024-09-11'],
                             y=[3000, 3500, 4500, 5000, 2000, 2500, 3000],
                             mode='lines',
                             name='EPDS 5 Demand (gallons)',line=dict(shape='spline', color='black')),
                  row=1, col=1)
    
    # Second graph (stacked bar chart - Production Flow to RED)
    # fig.add_trace(go.Bar(x=['2024-09-05', '2024-09-06', '2024-09-07'],
    #                      y=[2000, 2000, 2000],
    #                      name='NN Added'),
    #               row=1, col=2)
    # fig.add_trace(go.Bar(x=['2024-09-05', '2024-09-06', '2024-09-07'],
    #                      y=[3000, 3000, 3000],
    #                      name='NE Added'),
    #               row=1, col=2)

    # # Third graph (stacked bar chart - Production Flow to RM)
    # fig.add_trace(go.Bar(x=['2024-09-05', '2024-09-06', '2024-09-07'],
    #                      y=[1500, 1500, 1500],
    #                      name='RM1 Added'),
    #               row=1, col=3)
    # fig.add_trace(go.Bar(x=['2024-09-05', '2024-09-06', '2024-09-07'],
    #                      y=[2500, 2500, 2500],
    #                      name='RM2 Added'),
    #               row=1, col=3)

    # Update layout for better appearance
    # fig.update_layout(height=600, width=1000, title_text="Your Multi-Graph Visualization")
    fig.update_layout(title_text="Your Multi-Graph Visualization")
    
    # Return Plotly figure
    return fig


def index(request):
    chart = generate_charts()
    chart_div = plot(chart, output_type='div')  # Converts the graph to HTML div
    return render(request, 'plotly_pie.html', {'pie_chart': chart_div})

import plotly.io as pio
def demand_curve_view(request):
    x_data = ['2024-09-05 00:00', '2024-09-06 00:00', '2024-09-07 00:00', '2024-09-08 00:00', '2024-09-09 00:00']
    y_epds1 = [10000, 9500, 11000, 10500, 10000]  # Example data for EPDS 1
    y_epds2 = [6000, 5500, 6500, 6200, 6000]      # Example data for EPDS 2
    y_epds3 = [3000, 3500, 4000, 3800, 3600]      # Example data for EPDS 3
    y_epds4 = [3000, 3500, 2000, 3800, 1600]      # Example data for EPDS 3
    y_epds5 = [2000, 3500, 1000, 3800, 3600]      # Example data for EPDS 3
    y_epds6 = [3000, 3500, 1000, 3800, 2600]      # Example data for EPDS 3
    y_epds7 = [4000, 3500, 1000, 3800, 5600]      # Example data for EPDS 3
    y_epds8 = [5000, 3500, 2000, 3800, 4600]      # Example data for EPDS 3
    y_epds9 = [2000, 3500, 4000, 3800, 3600]      # Example data for EPDS 3
    y_epds10 = [3000, 3500, 4000, 3800, 3600]      # Example data for EPDS 3
    
    trace1 = go.Scatter(x=x_data, y=y_epds1, mode='lines', name='EPDS 1 Demand (gallons)', line=dict(shape='spline', color='black'))
    trace2 = go.Scatter(x=x_data, y=y_epds2, mode='lines', name='EPDS 2 Demand (gallons)', line=dict(shape='spline',color='green'))
    trace3 = go.Scatter(x=x_data, y=y_epds3, mode='lines', name='EPDS 3 Demand (gallons)', line=dict(shape='spline',color='blue'))
    trace4 = go.Scatter(x=x_data, y=y_epds4, mode='lines', name='EPDS 4 Demand (gallons)', line=dict(shape='spline',color='blue'))
    trace5 = go.Scatter(x=x_data, y=y_epds5, mode='lines', name='EPDS 5 Demand (gallons)', line=dict(shape='spline',color='blue'))
    trace6 = go.Scatter(x=x_data, y=y_epds6, mode='lines', name='EPDS 6 Demand (gallons)', line=dict(shape='spline',color='blue'))
    trace7 = go.Scatter(x=x_data, y=y_epds7, mode='lines', name='EPDS 7 Demand (gallons)', line=dict(shape='spline',color='blue'))
    trace8 = go.Scatter(x=x_data, y=y_epds8, mode='lines', name='EPDS 8 Demand (gallons)', line=dict(shape='spline',color='blue'))
    trace9 = go.Scatter(x=x_data, y=y_epds9, mode='lines', name='EPDS 9 Demand (gallons)', line=dict(shape='spline',color='blue'))
    trace10 = go.Scatter(x=x_data, y=y_epds10, mode='lines', name='EPDS 10 Demand (gallons)', line=dict(shape='spline',color='blue'))
    
    layout = go.Layout(title='Demand Curve - 05-Sep-24 to 11-Sep-24', xaxis=dict(title='Date'), yaxis=dict(title='Demand (Gallons)'))
    
    fig = go.Figure(data=[trace1, trace2, trace3,trace4,trace5,trace6,trace7,trace8,trace9,trace10], layout=layout)
    chart_html = pio.to_html(fig, full_html=False)
    
    return render(request, 'plotly_pie.html', {'pie_chart': chart_html})


def production_flow_red_view(request):
    x_data = ['2024-09-05 00:00', '2024-09-06 00:00', '2024-09-07 00:00']  # Example time values
    y_rmtp = [3000, 3200, 3100]  # Example data for RMTP
    y_nn = [1000, 1200, 1100]    # Example data for NN
    y_ne = [500, 600, 700]       # Example data for NE

    trace2 = go.Bar(x=x_data, y=y_rmtp, name='RMTP added', marker=dict(color='orange'))
    trace3 = go.Bar(x=x_data, y=y_nn, name='NN added',marker=dict(color='blue'))
    trace4 = go.Bar(x=x_data, y=y_ne, name='NE added', marker=dict(color='red'))
    trace1 = go.Scatter(x=x_data, y=y_rmtp, name='NE added', fill='tonexty', marker=dict(color='gray'))   
    
    layout = go.Layout(barmode='stack', title='Production Flow to RED - 05-Sep-24 to 11-Sep-24', xaxis=dict(title='Time'), yaxis=dict(title='Flow (Gallons)'))
    
    fig = go.Figure(data=[trace1, trace2, trace3,trace4], layout=layout)

   
    chart_html = pio.to_html(fig, full_html=False)
    
    return render(request, 'plotly_pie.html', {'pie_chart': chart_html})


def production_flow_rm_view(request):
    x_data = ['2024-09-05 00:00', '2024-09-06 00:00', '2024-09-07 00:00']  # Example time values
    y_sorrells_east = [1500, 1600, 1550]  # Example data for Sorrells East
    y_rm1 = [2000, 2100, 2050]            # Example data for RM1
    y_rm2 = [1000, 1100, 1050]            # Example data for RM2
    
    trace1 = go.Bar(x=x_data, y=y_sorrells_east, name='Sorrells East added', marker=dict(color='blue'))
    trace2 = go.Bar(x=x_data, y=y_rm1, name='RM1 added', marker=dict(color='orange'))
    trace3 = go.Bar(x=x_data, y=y_rm2, name='RM2 added', marker=dict(color='red'))
    
    layout = go.Layout(barmode='stack', title='Production Flow to RM - 05-Sep-24 to 11-Sep-24', xaxis=dict(title='Time'), yaxis=dict(title='Flow (Gallons)'))
    
    fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)


    chart_html = pio.to_html(fig, full_html=False)
    
    return render(request, 'plotly_pie.html', {'pie_chart': chart_html})



def production_flow_chart():
    # X-axis data
    x_data = ['00:00', '00:15', '00:30', '00:45', '01:00', '01:15', '01:30', 
              '01:45', '02:00', '02:15', '02:30', '02:45', '03:00', '03:15', '03:30']

    # Y-axis data for area chart
    area_data = [1500, 1600, 1550, 1650, 1700, 1600, 1550, 1700, 1750, 1600, 1650, 1700, 1800, 1750, 1700]

    # Y-axis data for bar charts
    bar_data_rm1 = [2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400]
    bar_data_rm2 = [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400]

    # Create figure
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add area chart trace
    fig.add_trace(go.Scatter(x=x_data, y=area_data, 
                             mode='none', 
                             fill='tozeroy', 
                             name='Sorrento East added',
                             fillcolor='blue'), secondary_y=False)

    # Add bar chart trace for RM1
    fig.add_trace(go.Bar(x=x_data, y=bar_data_rm1, 
                         name='RM1 added', 
                         marker_color='orange', 
                         opacity=0.8))

    # Add bar chart trace for RM2
    fig.add_trace(go.Bar(x=x_data, y=bar_data_rm2, 
                         name='RM2 added', 
                         marker_color='red', 
                         opacity=0.8))

    # Update layout
    fig.update_layout(barmode='stack', title='Production Flow to RM - 05-Sep-24 to 11-Sep-24', 
                      xaxis_title='Time', yaxis_title='Units', showlegend=True)

    # Return the figure
    return fig

def production_flow_view(request):
    chart = production_flow_chart()
    graph_json = pio.to_html(chart)
    return render(request, 'production_flow.html', {'production_flow_chart': graph_json})