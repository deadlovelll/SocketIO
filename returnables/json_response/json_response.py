"""
This module provides a simple utility class for serializing data into a JSON-formatted string.
"""

import json


class JsonResponse:
    
    """
    Utility class for converting Python data structures into JSON strings.

    This class overrides the __new__ method to directly return the JSON string,
    allowing the class to be used as a callable wrapper around `json.dumps`.
    """

    def __new__(
        cls,
        data,
    ) -> str:
        
        """
        Converts the input data to a JSON-formatted string.

        Args:
            data (Any): A serializable Python object (e.g., dict, list).

        Returns:
            str: A JSON string representation of the input data.

        Raises:
            TypeError: If the data is not serializable by `json.dumps`.
        """
        
        return json.dumps(data)
