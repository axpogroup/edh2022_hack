import csv
import building_classifier
import gbr_interface
from dxf import dxf_metrics_computation
from merge import merge_functions

def main():
    north_west = (2655000.034938044, 1217999.989094743)
    south_east = (2663750.03735189, 1214999.975487134)

    output = gbr_interface.GBRDataFetcher().request_data(
        north_west_coords=north_west,
        south_east_coords=south_east,
        classifier=building_classifier.BuildingClassifier(),
    )

    with open("01_gbr_output.csv", "w", encoding="utf8", newline="") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=gbr_interface.GBRBuildingData.get_field_names()
        )
        writer.writeheader()
        writer.writerows([building_data.dict() for building_data in output])

    dxf_filenames = ["data/SWISSBUILDINGS3D_2_0_CHLV95LN02_1150-11.dxf",
                     "data/SWISSBUILDINGS3D_2_0_CHLV95LN02_1150-12.dxf"]
    dxf_metrics_computation.computeAll(dxf_filenames, "02_dxf_volume_and_locations.csv")

    merge_functions.merge("01_gbr_output.csv", "02_dxf_volume_and_locations.csv", "03_advanced_classes.csv")


if __name__ == "__main__":
    main()
