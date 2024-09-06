from re import match
from django.contrib.staticfiles import finders


def parse_country_file(file_path):
    """
    Reads a file containing country data and extracts country codes and names.

    The file should have each line formatted such that the country code is the last word on the line,
    and the country name is the preceding part of the line. Lines that do not follow this format or are
    empty will be skipped.

    Args:
        file_path (str): The path to the file containing country data. Each line in the file should
                         have a format like "Country Name CODE", where CODE is the country code.

    Returns:
        list of tuple: A list of tuples, where each tuple contains two strings:
                       - The country code (e.g., "US").
                       - The country name (e.g., "United States").
                       
                       For example: [("US", "United States"), ("CA", "Canada")]

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    country_choices = []
    
    file_path = _get_file_path(file_path)
    try:
        with open(file_path) as file:
            for line in file:
                code, country = extract_country_and_code_from_string(line)
                if code and country:
                    country_choices.append((code, country))
    except FileNotFoundError:
        raise FileNotFoundError("The file was not found")
    
    return country_choices


def extract_country_and_code_from_string(country_line):
    """
    Extracts the country code and name from a string formatted as "Country Name CODE".

    Args:
        country_line (str): A string containing the country name and code, separated by whitespace.

    Returns:
        tuple: A tuple containing two strings:
               - The country code (e.g., "US").
               - The country name (e.g., "United States").
               
               Returns ("", "") if the format is incorrect.
    """
    matcher = match(r'^(.*)\s+(\S+)$', country_line.strip())
    if matcher:
        country = matcher.group(1).strip()
        code = matcher.group(2).strip()
        return code, country
    return "", ""


def _get_file_path(file_path):
    
    file_path = finders.find(file_path)
    if file_path is None:
        raise FileNotFoundError("The file was not found")
    return file_path
        