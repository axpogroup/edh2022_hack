from typing import Callable, Optional, Union, Any

import building_classifier.const as const


class BuildingClassifier:
    GBR_TYPE_TO_TYPE_MAP: dict[const.GBRBuildingClass, Union[const.BuildingType, dict[Any, const.BuildingType]]] = {
        const.GBRBuildingClass.TEMPORARY_SHELTERS: const.BuildingType.UNKNOWN,
        const.GBRBuildingClass.SPECIAL_CONSTRUCTIONS: const.BuildingType.NON_RESIDENTIAL,
        const.GBRBuildingClass.NON_RESIDENTIAL: {
            "_DEFAULT": const.BuildingType.NON_RESIDENTIAL,
            1271: const.BuildingType.AGRICULTURAL,
            1276: const.BuildingType.AGRICULTURAL,
            1277: const.BuildingType.AGRICULTURAL,
            1278: const.BuildingType.AGRICULTURAL,
        },
        const.GBRBuildingClass.RESIDENTIAL: const.BuildingType.RESIDENTIAL,
        const.GBRBuildingClass.RESIDENTIAL_SECONDARY_USE: const.BuildingType.RESIDENTIAL,
        const.GBRBuildingClass.RESIDENTIAL_PARTIAL_USE: const.BuildingType.RESIDENTIAL,
    }

    def classify(self, gbr_category: int, gbr_class: Optional[int]) -> const.BuildingType:
        if not const.GBRBuildingClass.has_value(gbr_category):
            return const.BuildingType.UNKNOWN

        gbr_category = const.GBRBuildingClass(gbr_category)
        result_type: Union[const.BuildingType, dict[Any, const.BuildingType]] = self.GBR_TYPE_TO_TYPE_MAP[gbr_category]
        if isinstance(result_type, dict):
            return result_type.get(gbr_class, result_type["_DEFAULT"])

        return result_type
