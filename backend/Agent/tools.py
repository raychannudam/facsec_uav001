
import json
from langchain.tools import tool
from sqlalchemy.orm import Session
from Models import get_db
from Services.Station import StationService
from Services.Controller import ControllerService
from fastapi.encoders import jsonable_encoder
from Services.Influx import InfluxService

@tool
def get_station_data() -> str:
    """Get station data from the database.
    """
    db: Session = next(get_db())
    stations = StationService.get_stations(db)
    if not stations:
        return "No stations found."

    stations_data = jsonable_encoder(stations)
    
    return f"Found {len(stations)} stations:\n{json.dumps(stations_data, indent=2)}"


@tool
def query_influxdb(flux_query: str) -> str:
    """Query InfluxDB using a Flux query.
    """
    influx_service = InfluxService()
    return influx_service.query(flux_query)

@tool
def get_s1_data() -> str:
    """Get data for drsys/ESP32/s1 topic from InfluxDB.
    """
    influx_service = InfluxService()
    flux_query = f'''
        from(bucket: "{influx_service.bucket}")
            |> range(start: -30d)
            |> filter(fn: (r) => r["topic"] == "drsys/ESP32/s1")
    '''
    return influx_service.query(flux_query)

@tool
def get_altitude_data() -> str:
    """Get data for drsys/ESP32/altitude topic from InfluxDB.
    """
    influx_service = InfluxService()
    flux_query = f'''
        from(bucket: "{influx_service.bucket}")
            |> range(start: -30d)
            |> filter(fn: (r) => r["topic"] == "drsys/ESP32/altitude")
    '''
    return influx_service.query(flux_query)

@tool
def get_b1_data() -> str:
    """Get data for drsys/ESP32/b1 topic from InfluxDB.
    """
    influx_service = InfluxService()
    flux_query = f'''
        from(bucket: "{influx_service.bucket}")
            |> range(start: -30d)
            |> filter(fn: (r) => r["topic"] == "drsys/ESP32/b1")
    '''
    return influx_service.query(flux_query)

@tool
def get_gps_latlng_data() -> str:
    """Get data for drsys/ESP32/gps_latlng topic from InfluxDB.
    """
    influx_service = InfluxService()
    flux_query = f'''
        from(bucket: "{influx_service.bucket}")
            |> range(start: -30d)
            |> filter(fn: (r) => r["topic"] == "drsys/ESP32/gps_latlng")
    '''
    return influx_service.query(flux_query)

@tool
def get_s2_data() -> str:
    """Get data for drsys/ESP32/s2 topic from InfluxDB.
    """
    influx_service = InfluxService()
    flux_query = f'''
        from(bucket: "{influx_service.bucket}")
            |> range(start: -30d)
            |> filter(fn: (r) => r["topic"] == "drsys/ESP32/s2")
    '''
    return influx_service.query(flux_query)

@tool
def get_s3_data() -> str:
    """Get data for drsys/ESP32/s3 topic from InfluxDB.
    """
    influx_service = InfluxService()
    flux_query = f'''
        from(bucket: "{influx_service.bucket}")
            |> range(start: -30d)
            |> filter(fn: (r) => r["topic"] == "drsys/ESP32/s3")
    '''
    return influx_service.query(flux_query)

@tool
def get_slide1_data() -> str:
    """Get data for drsys/ESP32/slide1 topic from InfluxDB.
    """
    influx_service = InfluxService()
    flux_query = f'''
        from(bucket: "{influx_service.bucket}")
            |> range(start: -30d)
            |> filter(fn: (r) => r["topic"] == "drsys/ESP32/slide1")
    '''
    return influx_service.query(flux_query)

@tool
def get_slide2_data() -> str:
    """Get data for drsys/ESP32/slide2 topic from InfluxDB.
    """
    influx_service = InfluxService()
    flux_query = f'''
        from(bucket: "{influx_service.bucket}")
            |> range(start: -30d)
            |> filter(fn: (r) => r["topic"] == "drsys/ESP32/slide2")
    '''
    return influx_service.query(flux_query)

@tool
def get_speed_data() -> str:
    """Get data for drsys/ESP32/speed topic from InfluxDB.
    """
    influx_service = InfluxService()
    flux_query = f'''
        from(bucket: "{influx_service.bucket}")
            |> range(start: -30d)
            |> filter(fn: (r) => r["topic"] == "drsys/ESP32/speed")
    '''
    print("Sokleap: ", influx_service.query(flux_query))
    return influx_service.query(flux_query)
