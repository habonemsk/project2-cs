import argparse
import json
import os

def parse_problem(problem_str):
    problem_dict = {
        "function_prototype": {
            "parameters": [],
            "return_values": []
        },
        "correctness_test_suite": [],
        "prompts": [],
    }
    
    lines = [line.strip() for line in problem_str.split('\n') if line.strip()]
    for line in lines:
        if ':' not in line:
            print(f"Skipping line '{line}' as it does not contain a colon.")
            continue
        
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()

        if key == 'Title':
            problem_dict['identifier'] = value
            problem_dict['title'] = value
        elif key == 'Description':
            problem_dict['description'] = value
        elif key == 'Function Prototype':
            try:
                func_name, params_return = value.split('(', 1)
                params, return_type = params_return.split(') -> ', 1)
            except ValueError as e:
                print(f"Error parsing Function Prototype on line '{line}': {e}")
                continue

            problem_dict['function_prototype']['function_name'] = func_name.strip()
            problem_dict['function_prototype']['parameters'] = [{'name': p.split(':')[0].strip(), 'type': p.split(':')[1].strip()} for p in params.split(', ') if p]
            problem_dict['function_prototype']['return_values'].append({'type': return_type.strip()})
        elif key == 'Tags':
            problem_dict['tags'] = [tag.strip() for tag in value.strip('[]').split(',')]
        elif key == 'Prompt':
            problem_dict['prompts'].append({
                "prompt_id": "brief_prompt",
                "prompt": value,
                "genericize": False,
                "sample_inputs_outputs": []
            })

    # Before creating the function signature, check if the necessary keys are present
    if 'function_name' not in problem_dict['function_prototype'] or \
       not problem_dict['function_prototype']['parameters'] or \
       not problem_dict['function_prototype']['return_values']:
        print(f"Error: Missing necessary keys in problem_dict for problem {problem_dict.get('title', 'Unknown')}")
        return None

    problem_dict["function_signature"] = f"def {problem_dict['function_prototype']['function_name']}({', '.join([p['name'] for p in problem_dict['function_prototype']['parameters']])}) -> {problem_dict['function_prototype']['return_values'][0]['type']}:"
    return problem_dict


def convert_txt_to_json(base_path, mode):
    txt_file_path = os.path.join(base_path, f"{mode}.txt")
    if not os.path.exists(txt_file_path):
        raise FileNotFoundError(f"The txt file {txt_file_path} does not exist.")

    json_directory = os.path.join('problem_sets', mode, 'problems')
    os.makedirs(json_directory, exist_ok=True)

    with open(txt_file_path, 'r') as file:
        content = file.read()

    problems_str = content.split('---')
    converted_count = 0
    for problem_str in problems_str:
        problem_str = problem_str.strip()
        if not problem_str:
            continue

        problem_dict = parse_problem(problem_str)
        
        # If problem_dict is None, skip this problem
        if problem_dict is None:
            print("Skipping current problem due to errors in parsing.")
            continue
        
        # If problem_dict does not have the key 'identifier', skip this problem
        if 'identifier' not in problem_dict:
            print(f"Skipping problem due to missing 'identifier': {problem_str[:60]}...")
            continue
        
        json_file_path = os.path.join(json_directory, f"{problem_dict['identifier']}.json")
        with open(json_file_path, 'w') as json_file:
            json.dump(problem_dict, json_file, indent=4)
        
        converted_count += 1  # Increment the count of successfully converted problems

    print(f"Converted {converted_count} problems from {txt_file_path} to JSON files in {json_directory}.")

def main():
    parser = argparse.ArgumentParser(description='Convert txt to JSON.')
    parser.add_argument('--base_path', type=str, required=True, help='The base path of the txt file.')
    parser.add_argument('--mode', type=str, required=True, choices=['basic', 'bugfixing'], help='The mode to use for conversion.')
    args = parser.parse_args()

    convert_txt_to_json(args.base_path, args.mode)


if __name__ == "__main__":
    main()
