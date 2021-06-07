success = 200
fail = 400


def success_message(message: str, data=''):
    ctx = {
        'code': success,
        'message': message,
        'data': data
    }
    return ctx


def fail_message(message: str, data=''):
    ctx = {
        'code': fail,
        'message': message,
        'data': data
    }
    return ctx
