import src.typewiseAlertConfig as Config


def get_step(alertTarget, breachType):
    alertAction = None
    if alertTarget == 'TO_CONTROLLER':
        send_to_controller(breachType)
        alertAction = Config.targetType[alertTarget]
    elif alertTarget == 'TO_EMAIL':
        send_to_email(breachType)
        alertAction = Config.targetType[alertTarget]
    return alertAction


def send_to_controller(breachType):
    if breachType in Config.breachType:
        message = f'{Config.header}, {breachType}'
        print(message)
        return Config.header, message
    else:
        return None


def send_to_email(breachType):
    if breachType in Config.breachType:
        EmailMessage = f'To: {Config.recepient}' + '\t' + Config.alertMessage[breachType]
        print(EmailMessage)
        return Config.recepient, EmailMessage
    else:
        return None
