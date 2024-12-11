from rest_framework.response import Response

def custom_response(message, status_code, data=None, success=True):
    """
    Utility function for consistent API responses.

    Args:
        message (str): Message to include in the response.
        status_code (int): HTTP status code.
        data (dict, optional): Response data. Defaults to None.
        success (bool): Whether the response indicates success or failure.

    Returns:
        Response: DRF Response object.
    """
    response_data = {
        'message': message,
        'status': 'success' if success else 'error',
        'data': data
    }
    return Response(response_data, status=status_code)