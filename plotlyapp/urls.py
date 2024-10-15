from django.urls import path
from . import views, chart_views

app_name = "plotlyapp"

urlpatterns = [
    path("", views.differentiated_chart, name="differentiated-chart"),
    path("plotlybarview/", views.plotly_bar_view, name="plotlybarview"),
    path("plotlypieview/", views.plotly_pie_view, name="plotlypieview"),
    path("plotlycurveview/", views.plotly_curve, name="plotlycurveview"),
    path("index/", views.index, name="index"),
    path("demand_curve_view/", views.demand_curve_view, name="demand_curve_view"),
    path(
        "production_flow_red_view/",
        views.production_flow_red_view,
        name="production_flow_red_view",
    ),
    path(
        "production_flow_rm_view/",
        views.production_flow_rm_view,
        name="production_flow_rm_view",
    ),
    path(
        "production_flow_view/", views.production_flow_view, name="production_flow_view"
    ),
    path("testchart/", views.test_chart, name="test_chart"),
    path("gwrchart/", chart_views.gwr_chart, name="gwr_chart"),
]
