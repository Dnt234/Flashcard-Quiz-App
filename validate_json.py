import json

def validate_json(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            print("JSON is valid.")
            print(data)
    except json.JSONDecodeError as e:
        print(f"JSON is invalid: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")

# Call the function with a filename
validate_json("example.json")
