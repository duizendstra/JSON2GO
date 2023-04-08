# JSON2Go

JSON2Go is a Python library that allows you to process an array of JSON objects and generate a Go struct based on the combined JSON data. It also provides functionality to anonymize the JSON data, keeping the data types intact.

## Features

- Anonymize JSON data
- Combine multiple JSON objects into one with all unique keys
- Generate a Go struct from the combined JSON object

## Installation

Clone the repository or download the `JSON2GO.py` file and place it in your project directory.

```
git clone https://github.com/duizendstra/JSON2GO.git
```

## Usage

Import the JSON2Go class:

```python
from JSON2GO import JSON2Go
```

Create a JSON2Go object with your JSON data:

```python
data = [...]  # Your JSON data
json2go = JSON2Go(data)
```

Anonymize the JSON data:

```python
anonymized_data = json2go.anonymize_data()
```

Combine multiple JSON objects:

```python
combined_json = json2go.combine_jsons()
```

Generate a Go struct:

```python
go_struct = json2go.generate_go_struct("YourStructName", combined_json)
print(go_struct)
```

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository on GitHub.
2. Create a branch with your changes.
3. Commit your changes and push to your fork.
4. Create a pull request with your changes.
