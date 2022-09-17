import zipfile

import requests
import json
import os
import logging
import shapely.geometry as shgeo
from shapely.geometry import Polygon, LineString
import pdal

import matplotlib.pyplot as plt


class SwissTopoDownloader:
    url: str
    params: dict
    headers = {"content-type": "application/x-www-form-urlencoded"}
    data_dir = "data"

    def download_tiles_by_polygon(self, polygon: Polygon):
        geometry = {
            "type": "Polygon",
            "crs": {"type": "name", "properties": {"name": "EPSG:2056"}},
            "coordinates": [list(polygon.exterior.coords)],
        }

        payload = {"geometry": json.dumps(geometry)}

        response = requests.post(
            self.url, headers=self.headers, data=payload, params=self.params
        )

        return response.json()

    @staticmethod
    def download_file(url, file_path):
        resp = requests.get(url)
        with open(file_path, "wb") as f:
            f.write(resp.content)

    def unzip_single_file(self, zip_file_path: str):
        tmp_dir = f"{self.data_dir}/tmp"
        destination_file = zip_file_path.removesuffix(".zip")
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(tmp_dir)
            unziped_file = zip_ref.namelist()[0]
            os.rename(f"{tmp_dir}/{unziped_file}", destination_file)
            os.remove(zip_file_path)
            os.rmdir(tmp_dir)

    def update_file_meta(self, items: list):
        os.makedirs(self.data_dir, exist_ok=True)
        meta_file = f"{self.data_dir}/files.json"
        try:
            with open(meta_file) as f:
                existing_files = json.load(f)
        except FileNotFoundError:
            existing_files = {}

        new_files = {}
        for f in items:
            zip_file = f["ass_asset_id"]
            final_file = zip_file.removesuffix(".zip")
            new_files[final_file] = {**f, "zip_file": zip_file, "file": final_file}

        all_files = {**existing_files, **new_files}

        with open(meta_file, "w") as f:
            json.dump(all_files, f)

        return new_files

    def download_files_by_polygon(self, polygon: Polygon):
        resp_json = self.download_tiles_by_polygon(polygon)
        new_files = self.update_file_meta(resp_json["items"])

        for id, item in new_files.items():
            zip_file_path = f'{self.data_dir}/{item["zip_file"]}'
            las_file_path = f'{self.data_dir}/{item["file"]}'
            if not os.path.exists(las_file_path):
                self.download_file(item["ass_asset_href"], zip_file_path)
                self.unzip_single_file(zip_file_path)

            else:
                logging.warning(f"file already exists: {las_file_path}")

        return new_files


class SwissBuildings3dDownloader(SwissTopoDownloader):
    url = "https://ogd.swisstopo.admin.ch/services/swiseld/services/assets/ch.swisstopo.swissbuildings3d_2/search"
    params = {"format": "application/x.dxf+zip", "srid": "2056", "state": "current"}
    data_dir = "data/buildings"


class SwissSurface3dDownloader(SwissTopoDownloader):
    url = "https://ogd.swisstopo.admin.ch/services/swiseld/services/assets/ch.swisstopo.swisssurface3d/search"
    params = {"format": "application/vnd.laszip", "srid": "2056", "state": "current"}
    data_dir = "data/surfaces"


class Controller:
    def __init__(self, power_line):
        self.power_line = power_line
        self.building_dl = SwissBuildings3dDownloader()
        self.surface_dl = SwissSurface3dDownloader()
        self.building_files: dict = {}
        self.surface_files: dict = {}

    def download_building_files(self):
        self.building_files = self.building_dl.download_files_by_polygon(
            self.line_buffer_polygon
        )

    def download_surface_files(self):
        self.surface_files = self.surface_dl.download_files_by_polygon(
            self.line_buffer_polygon
        )

    def merge_surface_files(self):
        for f in self.surface_files.items():
            pl = [
                        "1.2-with-color.las",
                        {
                            "type": "filters.sort",
                            "dimension": "X"
                        },
                        "1.2-with-color.las",
                    ]
            pipeline = pdal.Pipeline(json.dumps(pl))
            count = pipeline.execute()

    @property
    def line_buffer_polygon(self) -> Polygon:
        line = LineString(self.power_line)
        surrounding_polygon = line.buffer(4, cap_style=3, join_style=3)
        return surrounding_polygon

    def plot_line_buffer(self):
        line = shgeo.LineString(self.power_line)
        buffer = self.line_buffer_polygon
        plt.plot(*buffer.exterior.xy)
        plt.plot(*line.xy)
        plt.axis("equal")
        plt.show()


if __name__ == "__main__":
    line = [
        (2655011.0, 1217198.5),
        (2655986.0, 1217333.5),
        (2655996.0, 1217338.5),
        (2656521.0, 1217473.5),
        (2657006.0, 1217523.5),
        (2657976.0, 1217373.5),
    ]

    c = Controller(line)
    c.plot_line_buffer()
    c.download_building_files()
    c.download_surface_files()

    c.merge_surface_files()
