import os
import json

from src.sardinas_patterson.sp import SPChecker,Codex


def parse_input(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def main(raw_codes):
    checker = SPChecker()
    for code in raw_codes:
        # Create Codex instances
        codex = Codex(raw_codes[code])
        # Check if the code is uniquely decodable
        is_ud, factorization = checker.is_ud(codex)
        print("Code:", codex)
        print("Is UD:", is_ud)
        if not is_ud:
            print("Not uniquely decodable. Factorization:", factorization)

        print("-" * 30)


if __name__ == "__main__":
    PATH = "../src/sardinas_patterson/test/sp_tests.json"
    try:
        input_data = parse_input(PATH)
        main(input_data)
    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the input file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
