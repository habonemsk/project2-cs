
import json
import os
import argparse

TEMPLATE_JSON = {
    "identifier": "Valid Parentheses",
    "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. An input string is valid if: Open brackets must be closed by the same type of brackets. Open brackets must be closed in the correct order.",
    "function_prototype": {
        "function_name": "isValid",
        "parameters": [
            {
                "name": "s",
                "type": "str"
            }
        ],
        "return_values": [
            {
                "type": "bool"
            }
        ]
    },
    "correctness_test_suite": [
        {
            "input": {
                "s": "()[]"
            },
            "expected_output": [
                True
            ]
        },
        {
            "input": {
                "s": "([)]"
            },
            "expected_output": [
                False
            ]
        }
    ],
    "tags": [
        "String",
        "Stack",
        "Easy"
    ],
    "prompts": [
        {
            "prompt_id": "brief_prompt",
            "prompt": "Implement the isValid function to determine if the input string s has valid parentheses.",
            "genericize": False,
            "sample_inputs_outputs": [
                {
                    "input": {
                        "s": "()[]"
                    },
                    "expected_output": [
                        True
                    ]
                },
                {
                    "input": {
                        "s": "(]"
                    },
                    "expected_output": [
                        False
                    ]
                }
            ]
        },
        {
            "prompt_id": "detailed_prompt",
            "prompt": "Write a function named 'isValid' that takes a string s containing just the characters '(', ')', '{', '}', '[' and ']', and returns a boolean representing whether the input string has valid parentheses.",
            "genericize": True,
            "sample_inputs_outputs": [
                {
                    "input": {
                        "s": "()"
                    },
                    "expected_output": [
                        True
                    ]
                },
                {
                    "input": {
                        "s": "([)]"
                    },
                    "expected_output": [
                        False
                    ]
                }
            ]
        }
    ],
    "title": "Valid Parentheses",
    "function_signature": "def isValid(s: str) -> bool:",
    "example": "Input: s = \"()[]{}\"\nOutput: True"
}

def convert_txt_to_json(base_path: str, mode: str):
    # Use the hard-coded template JSON
    template_json = TEMPLATE_JSON

    # Define the txt file path based on the mode
    txt_file_path = os.path.join(base_path, f"{mode}.txt")
    if not os.path.exists(txt_file_path):
        raise FileNotFoundError(f"The txt file {txt_file_path} does not exist.")

    # Define the JSON output directory based on the mode
    json_output_dir = os.path.join(base_path, 'problem_sets', mode, 'problems')
    os.makedirs(json_output_dir, exist_ok=True)

    # Read the txt file
    with open(txt_file_path, 'r') as txt_file:
        titles = [title.strip() for title in txt_file.readlines() if title.strip()]

    for title in titles:
        # Use the template JSON and update the title
        json_obj = template_json.copy()
        json_obj['title'] = title
        json_obj['identifier'] = title

        # Define the JSON file path based on the title
        formatted_title = title.replace(" ", "_")
        json_file_path = os.path.join(json_output_dir, f"{formatted_title}.json")
        with open(json_file_path, 'w') as json_file:
            json.dump(json_obj, json_file, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Convert txt to JSON.')
    parser.add_argument('--base_path', required=True, help='The base path of the txt file.')
    parser.add_argument('--mode', required=True, help='The mode, e.g., basic or bugfixing.')
    args = parser.parse_args()
    convert_txt_to_json(args.base_path, args.mode)

if __name__ == "__main__":
    main()
