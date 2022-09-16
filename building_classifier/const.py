import enum


class BuildingType(enum.Enum):
    UNKNOWN = 0
    NON_RESIDENTIAL = 1
    RESIDENTIAL = 2
    AGRICULTURAL = 3


class BuildingTypeExtended(enum.Enum):
    """
    This is the extension for the building type.
    It's not used yet.
    But it might be mapped to the GBRBuildingType
    later.
    """

    pass


class GBRBuildingClass(enum.Enum):
    TEMPORARY_SHELTERS = 1010
    RESIDENTIAL = 1020
    RESIDENTIAL_SECONDARY_USE = 1030
    RESIDENTIAL_PARTIAL_USE = 1040
    NON_RESIDENTIAL = 1060
    SPECIAL_CONSTRUCTIONS = 1080

    @classmethod
    def has_value(cls, value: int) -> bool:
        return value in cls._value2member_map_
