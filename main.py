import os
import json

from dotenv import load_dotenv

from metrolinx_api.general_data_fetcher import GeneralDataFetcher
from metrolinx_api.gtfs_vehicle_position import GtfsVehiclePosition

def main():
    data = GtfsVehiclePosition()
    print(data.get_timestamp())
    # print(data.get_vehicle_info())
    print(json.dumps(data.data, indent=4))


if __name__ == "__main__":
    main()
