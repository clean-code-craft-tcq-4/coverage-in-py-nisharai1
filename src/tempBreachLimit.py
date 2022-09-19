temperature = {"PASSIVE_COOLING": (0, 35),
               "HI_ACTIVE_COOLING": (0, 45),
               "NORMAL_ACTIVE_COOLING": (0, 40), }

coolingTypes = "PASSIVE_COOLING", "HI_ACTIVE_COOLING", "NORMAL_ACTIVE_COOLING"


def get_temperature(coolingType):
    if coolingType in coolingTypes:
        return temperature[coolingType]
    else:
        return None
