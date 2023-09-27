from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    handlers = {"ValidationError": _handle_generic_error}

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        response.data["status_code"] = response.status_code
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):
    response.data = {"errors": response.data}

    return response


# -----------------------------------------------------------------------------------

# if response is not None:
#     response.data['status_code'] = response.status_code


# from rest_framework.views import exception_handler

# def status_code_handler(exc, context):
#     response = exception_handler(exc, context)

#     if response is not None and response.status_code == 403:
#         response.status_code == 401

#     return response

# REST_FRAMEWORK = {
#     'EXCEPTION_HANDLER': 'accounts.exceptions.status_code_handler',
# }
