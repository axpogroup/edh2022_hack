import csv
import building_classifier
import gbr_interface


def main():
    north_west = (655000, 218235)
    south_east = (663400, 214855)

    output = gbr_interface.GBRDataFetcher().request_data(
        north_west_coords=north_west,
        south_east_coords=south_east,
        classifier=building_classifier.BuildingClassifier(),
    )

    with open("output.csv", "w", encoding="utf8", newline="") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=gbr_interface.GBRBuildingData.get_field_names()
        )
        writer.writeheader()
        writer.writerows([building_data.dict() for building_data in output])


if __name__ == "__main__":
    main()
