"""
This module contains helper functions that are used across the application.
"""


def create_response(detail: str, status_code: int):
    """
    Creates a response object with the given detail and status code.
    """
    return {
        'detail': detail,
        'status_code': status_code,
    }
