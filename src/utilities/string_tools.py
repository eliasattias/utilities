# %%
import logging
import os
import pandas as pd

class StringUtils:
    """
    Class for string utility functions.
    """

    def __init__(self):
        """Initialize the logger for String_Utils"""
        StringUtils.logger = logging.getLogger(os.getenv('LOG_ENV'))
    
    @staticmethod
    def read_text_file_as_fstrings(file, **fstring_dictionary):
        """ Read the content of a text file and return it as an f-string.
        
        Args:
            file (str): The path to the text file.
            fstring_dictionary (dict, optional): Dictionary containing key-value pairs for f-string replacement.
                Defaults to {} (empty dictionary).
        
        Returns:
            str: The content of the text file as an f-string. """
        try:
            with open(file, 'r') as file_name:
                content = file_name.read()
                if fstring_dictionary:
                    # Replace placeholders in content with values from the dictionary
                    content = content.format(**fstring_dictionary)
                return content
        except Exception as e:
            StringUtils.logger.info(f"Error reading file {file}: {e}")
            return ""
