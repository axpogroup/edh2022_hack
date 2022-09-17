from typing import Optional, Any

import requests
import pydantic
import building_classifier


class GBRBuildingData(pydantic.BaseModel):
    egid: Optional[str]
    gkat: Optional[int]
    gklas: Optional[int]
    street: Optional[str]
    zip: Optional[str]
    city: Optional[str]
    description: Optional[str]
    building_type: building_classifier.BuildingType
    gkat: Optional[int]
    gklas: Optional[int]
    coordinate_lat: Optional[float]
    coordinate_lon: Optional[float]
    area: Optional[int]
    volume: Optional[int]
    url: Optional[str]

    @classmethod
    def get_field_names(cls, alias=False):
        return list(cls.schema(alias).get("properties").keys())

    def dict(self, *args, **kwargs) -> dict[str, Any]:
        result = super(GBRBuildingData, self).dict(*args, **kwargs)
        result["building_type"] = self.building_type.name
        return result


class GBRDataFetcher:
    @staticmethod
    def _get_buildings_list_url(
        north_west_coords: tuple[int, int], south_east_coords: tuple[int, int]
    ) -> str:
        url = (
            f"https://api3.geo.admin.ch/rest/services/api/MapServer/identify?"
            f"geometryType=esriGeometryEnvelope&"
            f"geometry={north_west_coords[0]},{north_west_coords[1]},"
            f"{south_east_coords[0]},{south_east_coords[1]}&"
            f"tolerance=0&"
            f"sr=2056&"
            f"layers=all:ch.bfs.gebaeude_wohnungs_register&returnGeometry=false"
        )
        return url

    @staticmethod
    def _get_building_url(egid: int) -> str:
        url = f"https://map.geo.admin.ch/?ch.bfs.gebaeude_wohnungs_register={egid}_0&time=None&lang=de&topic=ech"
        return url

    def request_data(
        self,
        north_west_coords: tuple[int, int],
        south_east_coords: tuple[int, int],
        classifier: building_classifier.AbstractBuildingClassifier,
    ) -> list[GBRBuildingData]:
        building_list_data = requests.get(
            self._get_buildings_list_url(
                north_west_coords=north_west_coords, south_east_coords=south_east_coords
            )
        ).json()
        output = []
        for building in building_list_data["results"]:
            attr = building["attributes"]
            building_type = classifier.classify(
                gbr_category=attr["gkat"], gbr_class=attr["gklas"]
            )

            building_data = GBRBuildingData(
                egid=attr["egid"],
                street=attr["strname_deinr"],
                zip=attr["dplz4"],
                city=attr["ggdename"],
                description=attr["gbez"],
                building_type=building_type,
                gkat=attr["gkat"],
                gklas=attr["gklas"],
                coordinate_lat=attr["gkode"],
                coordinate_lon=attr["gkodn"],
                area=attr["garea"],
                volume=attr["gvol"],
                url=self._get_building_url(egid=attr["egid"]),
            )
            output.append(building_data)
        return output
