import requests
import json


class SwissBuildingsDownloader:
    url = "https://ogd.swisstopo.admin.ch/services/swiseld/services/assets/ch.swisstopo.swissbuildings3d_2/search"

    params = {"format": "application/x.dxf+zip", "srid": "2056", "state": "current"}
    headers = {"content-type": "application/x-www-form-urlencoded"}

    def download_tiles_by_polygon(self, polygon):
        geometry = {
            "type": "Polygon",
            "crs": {"type": "name", "properties": {"name": "EPSG:2056"}},
            "coordinates": [polygon],
        }

        payload = {"geometry": json.dumps(geometry)}

        response = requests.request(
            "POST", self.url, headers=self.headers, data=payload, params=self.params
        )

        return response.json()


class LasDownloader:
    url = (
        "https://ogd.swisstopo.admin.ch/services/swiseld/services/assets/ch.swisstopo.swisssurface3d/search"
        "?format=application/vnd.laszip&srid=2056&state=current"
    )
    headers = {"content-type": "application/x-www-form-urlencoded"}

    def download_by_polygon(self, polygon):
        geometry = {
            "type": "Polygon",
            "crs": {"type": "name", "properties": {"name": "EPSG:2056"}},
            "coordinates": [polygon],
        }

        payload = {"geometry": json.dumps(geometry)}

        response = requests.request(
            "POST", self.url, headers=self.headers, data=payload
        )

        resp_json = response.json()

        for item in resp_json["items"]:
            url = "http://i3.ytimg.com/vi/J---aiyznGQ/mqdefault.jpg"
            r = requests.get(item["ass_asset_href"])

            with open(f'data/las/{item["ass_asset_id"]}', "wb") as f:
                f.write(r.content)

            ...


if __name__ == "__main__":
    polygon = [
        [2653303.7617060556, 1220020.2855703058],
        [2653270.843540898, 1216529.351093326],
        [2662033.9766933974, 1216312.7842172906],
        [2661722.6120217186, 1219476.6534170236],
        [2653303.7617060556, 1220020.2855703058],
    ]

    sb_dl = SwissBuildingsDownloader()
    data = sb_dl.download_tiles_by_polygon(polygon)

    las_dl = LasDownloader()
    r = las_dl.download_by_polygon(polygon)
    files = []
    ...
