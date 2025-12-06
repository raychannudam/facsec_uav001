from influxdb_client import InfluxDBClient
from datetime import datetime
import os

class InfluxService:
    def __init__(self):
        url = os.getenv("INFLUXDB_URL", "http://influxdb_facsec:8086")
        token = os.getenv("DOCKER_INFLUXDB_INIT_TOKEN", "your_influx_token")
        org = os.getenv("DOCKER_INFLUXDB_INIT_ORG", "drtech")
        bucket = os.getenv("DOCKER_INFLUXDB_INIT_BUCKET", "drsys")
        
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.query_api = self.client.query_api()
        self.bucket = bucket
        self.org = org

    def query(self, flux_query: str):
        """
        Executes a raw Flux query and returns structured results.
        Returns "no data" if the bucket (or query range) contains no data.
        """
        # return "hello"
        tables = self.query_api.query(query=flux_query, org=self.org)
        return tables

        results = []
        for table in tables:
            for record in table.records:
                results.append({
                    "measurement": record.get_measurement(),
                    "field": record.get_field(),
                    "value": record.get_value(),
                    "time": record.get_time().isoformat(),
                    "tags": record.values
                })

        if not results:
            return {}

        return results


    def get_latest_value(self, measurement: str, field: str):
        """
        Fetch the latest value for a specific measurement/field.
        Optionally filter by drone ID tag.
        """
        flux_query = f'''
            from(bucket: "{self.bucket}")
                |> range(start: -1h)
                |> last()
        '''

        return self.query(flux_query)

    def get_measurement_history(self, measurement: str, field: str, range_str: str = "30m"):
        """
        Get historical data for a measurement/field.
        """
        flux_query = f'''
            from(bucket: "{self.bucket}")
                |> range(start: -{range_str})
                |> sort(columns: ["_time"])
        '''

        return self.query(flux_query)

    def get_drone_telemetry(self, drone_username: str, range_str: str = "10m"):
        """
        Example helper:
        Fetch common telemetry fields (altitude, speed, battery, gps, temperature)
        for one drone.
        """
        fields = ["altitude", "speed", "battery", "gps_latlng", "temperature"]

        results = {}
        for field in fields:
            results[field] = self.get_measurement_history(
                measurement="telemetry",
                field=field,
                range_str=range_str
            )

        return results
