import openai


class AiResponse:

    def __init__(self, text: str, prompt: str) -> None:
        self.completion = openai.Completion()
        self.prompt = "%sYou: %s\nFriend:" % (prompt, text)

    @property
    def _response(self) -> str:
        response = self.completion.create(
            prompt=self.prompt,
            engine="text-davinci-002",
            temperature=0.6,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            stop=["You:"])
        return response.choices[0].text.strip()

    def __str__(self) -> str:
        return self._response
