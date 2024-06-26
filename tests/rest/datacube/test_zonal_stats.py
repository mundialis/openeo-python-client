import pytest
import shapely.geometry

import openeo.processes
from openeo.api.process import Parameter

from .. import get_execute_graph


def test_polygon_timeseries_polygon(connection, api_version, test_data):
    polygon = shapely.geometry.shape(test_data.load_json("polygon.json"))
    res = connection.load_collection("S2").filter_bbox(3, 6, 52, 50).polygonal_mean_timeseries(polygon)
    assert get_execute_graph(res) == test_data.load_json("%s/aggregate_zonal_polygon.json" % api_version)


@pytest.mark.parametrize("reducer", ["mean", openeo.processes.mean, lambda x: x.mean()])
def test_aggregate_spatial(connection, api_version, reducer, test_data):
    polygon = shapely.geometry.shape(test_data.load_json("polygon.json"))
    res = (
        connection.load_collection("S2")
            .filter_bbox(3, 6, 52, 50)
            .aggregate_spatial(geometries=polygon, reducer=reducer)
    )
    assert get_execute_graph(res) == test_data.load_json("%s/aggregate_zonal_polygon.json" % api_version)


def test_polygon_timeseries_path(connection, api_version, test_data):
    res = (
        connection.load_collection('S2')
            .filter_bbox(west=3, east=6, north=52, south=50)
            .polygonal_mean_timeseries(polygon="/some/path/to/GeometryCollection.geojson")
    )
    assert get_execute_graph(res) == test_data.load_json("%s/aggregate_zonal_path.json" % api_version)


@pytest.mark.parametrize("reducer", ["mean", openeo.processes.mean, lambda x: x.mean()])
def test_aggregate_spatial_read_vector(connection, api_version, reducer, test_data):
    res = (
        connection.load_collection("S2")
            .filter_bbox(3, 6, 52, 50)
            .aggregate_spatial(geometries="/some/path/to/GeometryCollection.geojson", reducer=reducer)
    )
    assert get_execute_graph(res) == test_data.load_json("%s/aggregate_zonal_path.json" % api_version)


def test_aggregate_spatial_parameter_polygon(connection, api_version, test_data):
    geometries = Parameter("polygon")
    res = (
        connection.load_collection("S2")
            .filter_bbox(3, 6, 52, 50)
            .aggregate_spatial(geometries=geometries, reducer="mean")
    )
    assert get_execute_graph(res) == test_data.load_json("%s/aggregate_zonal_parameter.json" % api_version)
