import src.tempBreachLimit as definition
import src.typewiseAlertStep as step


def infer_breach(value, lowerLimit, upperLimit):
    if value < lowerLimit:
        return 'TOO_LOW'
    if value > upperLimit:
        return 'TOO_HIGH'
    return 'NORMAL'


def classify_temperature_breach(coolingType, temperatureInC):
    if coolingType in definition.coolingTypes:
        lowerLimit, upperLimit = definition.get_temperature(coolingType)
        return infer_breach(temperatureInC, lowerLimit, upperLimit)
    else:
        return None


def check_and_alert(alertTarget, coolingType, temperatureInC):
    if coolingType in definition.coolingTypes:
        breachType = \
            classify_temperature_breach(coolingType, temperatureInC)
        Action = step.get_step(alertTarget, breachType)
        return Action
    else:
        return None
