import numpy


def haversine_km(lat_o: float, lon_o: float, lat_f: float, lon_f: float):
    """
    Returns the great circle distance between two points on the Earth, defined by args :

    Args :
    - lat_o : Latitude of origin, or first point
    - lon_o : Longitude of origin, or first point
    - lat_f : Latitude of final point, or destination
    - lon_f : Longitude of final point, or destination

    Returns :
    - Haverside_distance : The estimated distance, in Km, between point o and point f
    """

    earth_radius = 6371  # In Km
    float_list = [lat_o, lon_o, lat_f, lon_f]
    r_lat_o, r_lon_o, r_lat_f, r_lon_f = map(numpy.radians, float_list)  # Convert lat/lon to radians

    delta_lat = r_lat_f - r_lat_o
    delta_lon = r_lon_f - r_lon_o

    # meaning of both "a" and "c" can be found in sources :
    # - "c" is the angular distance between two points (in radians)
    # - "a" is the square of half the chord length between two points.
    a = numpy.sin(delta_lat/2.0) ** 2 + numpy.cos(r_lat_o) * numpy.cos(r_lat_f) * numpy.sin(delta_lon/2.0) ** 2
    c = 2 * numpy.arcsin(numpy.sqrt(a))

    return round(c * earth_radius, ndigits=4)  # Precision to meter
