import os
import openai
from pathlib import Path
import json

directory = Path("C:/LLMCodingBenchmarkingFramework-main/prompt")
filename = "basic.txt"

full_path = directory / filename
print(full_path)
# Initialize OpenAI (you'll need to set this up locally with your API key)
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    raise ValueError("API key not set in environment variables")

def generate_json_from_txt(file_path):
    # Read problem statement from file
    with open(full_path, 'r') as f:
        concise_statement = f.readline().strip()

    # Extract details from concise statement
    details_split = concise_statement.split()
    function_name = details_split[0]
    param_type = details_split[-1]
    
    # Generate detailed problem statement using OpenAI
    response = openai.Completion.create(
      engine="davinci",  # or any other engine like "curie", "babbage", "ada"
      prompt=f"Given a concise problem statement: '{concise_statement}', provide a detailed problem statement, function prototype, and sample input/output.",
      max_tokens=150
    )
    detailed_statement = response.choices[0].text.strip()

    # Dummy parsing (you may need to refine this based on OpenAI's output)
    function_prototype = f"{function_name}({param_type}, {param_type}) -> {param_type}"
    
    # Construct JSON structure
    problem_json = {
        "identifier": f"problem_{function_name}",
        "description": detailed_statement,
        "function_prototype": {
            "function_name": function_name,
            "parameters": [{"name": f"param{i+1}", "type": param_type} for i in range(2)],
            "return_values": [{"type": param_type}]
        },
        "correctness_test_suite": [],
        "tags": [],
        "prompts": []
    }

    # Example prompts (this is just a dummy example, actual prompts may vary)
    problem_json["prompts"].append({
        "prompt_id": "brief_prompt",
        "prompt": f"Implement the {function_name} function as described.",
        "genericize": False,
        "sample_inputs_outputs": []
    })
    problem_json["prompts"].append({
        "prompt_id": "detailed_prompt",
        "prompt": detailed_statement,
        "genericize": True,
        "sample_inputs_outputs": []
    })
    output_file = f"{problem_json['identifier']}.json"
    with open(output_file, 'w') as outfile:
        json.dump(problem_json, outfile, indent=4)

    return problem_json

problem_json = generate_json_from_txt("path_to_your_txt_file.txt")
print(problem_json)

