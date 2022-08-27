class CoolingType:
    breach_type = 'Default'

    def __init__(self, val, ul, ll):
        self.infer_breach(val, ul, ll)

    def infer_breach(self, value, upperLimit, lowerLimit):
        if value < lowerLimit:
            self.breach_type = 'TOO_LOW'
        elif value > upperLimit:
            self.breach_type = 'TOO_HIGH'
        else:
            self.breach_type = 'NORMAL'


def classify_temperature_breach(coolingType, temperatureInC):
    if coolingType == 'PASSIVE_COOLING':
        return CoolingType(temperatureInC, 35, 0).breach_type
    elif coolingType == 'HI_ACTIVE_COOLING':
        return CoolingType(temperatureInC, 45, 0).breach_type
    else:
        return CoolingType(temperatureInC, 40, 0).breach_type


def controller_message(header, breachType):
    string = f'{hex(header)}, {breachType}'
    return string


def recepient(recepient):
    string = f'To: {recepient}'
    return string


def message_on_console(message):
    print(message)


def send_to_controller(breachType, print_message_on_console, header):
    message = controller_message(header, breachType)
    message_on_console(message)
    return controller_message


def send_to_email(breachType, message, recepient):
    global breach_message
    recepient_message = recepient(recepient)
    message(recepient_message)
    if breachType == 'TOO_LOW':
        breach_message = 'Hi, the temperature is too low'
    elif breachType == 'TOO_HIGH':
        breach_message = 'Hi, the temperature is too high'
    message(breach_message)
    return breachType, breach_message


def check_and_alert(coolingType, temperatureInC, classify_temperature_breach, send_to_controller_or_email,
                    print_message_on_console, recepient_or_header):
    breachType = \
        classify_temperature_breach(coolingType, temperatureInC)
    send_to_controller_or_email(breachType, print_message_on_console, recepient_or_header)
