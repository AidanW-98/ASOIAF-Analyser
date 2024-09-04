import openai


class PromptToSQL:
    def __init__(self):
        api_key_path = "./src/resources/openai_apikey.txt"
        base_prompt_path = "src/resources/query_engine_prompt.txt"

        with open(api_key_path, "r") as f:
            openai.api_key = f.readline()

        with open(base_prompt_path, "r") as f:
            prompt_list = f.readlines()
            combined_string = "\n".join(
                line.strip() for line in prompt_list if line.strip()
            )
            self.base_prompt = f"""{combined_string}"""

        self.conversation_history = [{"role": "system", "content": self.base_prompt}]

    def get_sql(self, user_query: str) -> str:
        # the conversation history should be sent at each call
        self.conversation_history.append({"role": "user", "content": user_query})

        response = openai.chat.completions.create(
            model="gpt-4o-mini", messages=self.conversation_history, temperature=0.2
        )

        response_text = response.choices[0].message.content.strip('"')
        self.conversation_history.append(
            {"role": "assistant", "content": response_text}
        )

        return response_text
