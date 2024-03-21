import re


class RegexUtils:
    @staticmethod
    def extract_digits(input_string):
        match = re.search(r'\d+', input_string)
        return match.group() if match else None
