from influxdb_client import InfluxDBClient
from datetime import datetime
import os
import json

class InfluxService:
    def __init__(self):
        url = os.getenv("INFLUXDB_URL")
        org = os.getenv("DOCKER_INFLUXDB_INIT_ORG")
        bucket = os.getenv("DOCKER_INFLUXDB_INIT_BUCKET")
        user = os.getenv("INFLUXDB_USER")
        password = os.getenv("INFLUXDB_PASSWORD")

        self.client = InfluxDBClient(url=url, org=org, username=user, password=password)
        self.query_api = self.client.query_api()
        self.bucket = bucket
        self.org = org

    def query(self, flux_query: str):
        """
        Executes a raw Flux query and returns structured results.
        Returns "no data" if the bucket (or query range) contains no data.
        """
        tables = self.query_api.query(query=flux_query, org=self.org)
        
        results = []
        for table in tables:
            for record in table.records:
                results.append(record.values)

        if not results:
            return "no data"

        # Convert datetime objects to string
        for row in results:
            for key, value in row.items():
                if isinstance(value, datetime):
                    row[key] = value.isoformat()
                    
        return json.dumps(results, indent=2)


    def get_latest_value(self, measurement: str, field: str):
        """
        Fetch the latest value for a specific measurement/field.
        Optionally filter by drone ID tag.
        """
        flux_query = f'''
            from(bucket: "{self.bucket}")
                |> range(start: -1h)
                |> filter(fn: (r) => r["_measurement"] == "{measurement}" and r["_field"] == "{field}")
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
                |> filter(fn: (r) => r["_measurement"] == "{measurement}" and r["_field"] == "{field}")
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
