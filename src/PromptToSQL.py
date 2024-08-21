import openai

class PromptToSQL():
    def __init__(self):
        api_key_path = "./src/resources/openai_apikey.txt"
        base_prompt_path = "src/resources/query_engine_prompt.txt"

        with open(api_key_path, 'r') as f: openai.api_key = f.readline()

        with open(base_prompt_path, 'r') as f: 
            prompt_list = f.readlines()
            combined_string = '\n'.join(line.strip() for line in prompt_list if line.strip())
            self.base_prompt = f"""{combined_string}"""
    
    def get_sql(self, user_query: str) -> str:
        prompt = self.base_prompt + user_query

        response = openai.completions.create(
            model="davinci-002",
            prompt=prompt,
            max_tokens=150
        )