from requests import post as http_post
from requests.exceptions import JSONDecodeError, InvalidJSONError
from random import choice as rand_select
import logging as log


class PorfirevichHttp:

    def __init__(self) -> None:
        self.host:    str = "pelevin.gpt.dobro.ai"
        self.path:    str = "generate"
        self.schema:  str = "https"
        self.headers: dict = {
            "Cache-Control": "no-cache"
        }

    def _build_request(self, body: dict) -> dict:
        return dict(
            url=f"{self.schema}://{self.host}/{self.path}/",
            json=body,
            headers=self.headers
        )

    def _make_request(self, body) -> http_post:
        return http_post(**self._build_request(body))

    @staticmethod
    def _validate_response(response: http_post) -> bool:
        try:
            response.json()
        except (JSONDecodeError, InvalidJSONError) as e:
            log.error("Error decode JSON response. %s: %s" % (
                e.__class__.__name__, e))
            return False
        except Exception as e:
            raise("Unknown error in step validation response. %s: %s" % (
                e.__class__.__name__, e))
            return False
        return True

    def get(self, body: dict) -> dict:
        response = self._make_request(body)
        return response.json() \
            if self._validate_response(response) \
            else {}


class Porfirevich:

    def __init__(self, text: str, prompt: str, length: int = 30) -> None:
        self.completion = PorfirevichHttp()
        self.stop_word = "Ты:"
        self.prompt: str = "%sТы: %s\nДруг:" % (prompt, text)
        self.length: int = length

    def _stopper(self, text: str) -> str:
        return "\x20".join([
            w for w in text.split()
            if w != self.stop_word
        ])

    def _request(self) -> list:
        # five repeats
        for _ in range(5):
            try:
                return self.completion.get({
                    "prompt": self.prompt,
                    "length": self.length
                })["replies"]
            except Exception as e:
                log.error("Error get response from Porfirevich. %s" % e)

    @staticmethod
    def _select(replies: list) -> str:
        return rand_select(replies).strip()

    @property
    def _order_result(self) -> str:
        org_array = self._request()
        resp_string = self._stopper(
            self._select(org_array))
        if not resp_string:
            raise ValueError("No response text")
        return resp_string

    def __str__(self) -> str:
        return self._order_result
