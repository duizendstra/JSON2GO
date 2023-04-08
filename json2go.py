import json
import random
import string
from datetime import datetime

class JSON2Go:
    def __init__(self, json_data):
        self.json_data = json_data

    def anonymize_datetime(self, dt_str):
        """Anonymizes datetime string by keeping the format unchanged."""
        return datetime.strftime(datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%fZ'), '%Y-%m-%dT%H:%M:%S.%fZ')

    def anonymize_value(self, value):
        """
        Anonymizes the value based on its data type.
        """
        if isinstance(value, str):
            try:
                dt = datetime.fromisoformat(value.rstrip("Z"))
                return self.anonymize_datetime(value)
            except ValueError:
                return ''.join(random.choices(string.ascii_letters + string.digits, k=len(value)))
        elif isinstance(value, int):
            return random.randint(0, 100)
        elif isinstance(value, float):
            return round(random.uniform(0, 100), 2)
        elif isinstance(value, bool):
            return random.choice([True, False])
        elif isinstance(value, list):
            return [self.anonymize_value(item) for item in value]
        elif isinstance(value, dict):
            return self.anonymize_json(value)
        else:
            return None

    def anonymize_json(self, json_obj):
        """
        Anonymizes the input JSON object by anonymizing its values.
        """
        anonymized_json = {}
        for key, value in json_obj.items():
            anonymized_json[key] = self.anonymize_value(value)
        return anonymized_json

    def anonymize_data(self):
        """
        Anonymizes the JSON data by calling anonymize_json() on each JSON object.
        """
        anonymized_data = []
        for json_obj in self.json_data:
            anonymized_data.append(self.anonymize_json(json_obj))
        return anonymized_data

    def combine_jsons(self):
        """
        Combines all JSON objects into one JSON object with all unique keys.
        """
        combined_json = {}
        for json_obj in self.json_data:
            for key, value in json_obj.items():
                if key not in combined_json:
                    combined_json[key] = value
        return combined_json

    def generate_go_struct(self, struct_name, json_obj, indent_level=0):
        """
        Generates a Go struct from the input JSON object.
        """
        indent = '    ' * indent_level
        go_struct = f'{indent}type {struct_name} struct {{\n'

        for key, value in json_obj.items():
            field_type = ''
            if isinstance(value, str):
                try:
                    dt = datetime.fromisoformat(value.rstrip("Z"))
                    field_type = 'time.Time'
                except ValueError:
                    field_type = 'string'
            elif isinstance(value, int):
                field_type = 'int'
            elif isinstance(value, float):
                field_type = 'float64'
            elif isinstance(value, bool):
                field_type = 'bool'
            elif isinstance(value, list):
                if value and isinstance(value[0], dict):
                    nested_struct_name = key.capitalize()
                    field_type = f'[]{nested_struct_name}'
                    go_struct += self.generate_go_struct(nested_struct_name, value[0], indent_level + 1)
                else:
                    field_type = '[]interface{}'
            elif isinstance(value, dict):
                nested_struct_name = key.capitalize()
                go_struct += self.generate_go_struct(nested_struct_name, value, indent_level + 1)
            else:
                field_type = 'interface{}'

            field_name = ''.join([part.capitalize() for part in key.split('_')])
            go_struct += f'{indent}    {field_name} {field_type}\n'

        go_struct += f'{indent}}}\n'
        return go_struct
