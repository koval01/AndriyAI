from translatepy.translators.google import GoogleTranslate
import logging as log


class Translate:

    def __init__(self, from_: str, to_: str, text: str) -> None:
        self.gtranslate = GoogleTranslate()
        self.from_ = from_
        self.to_ = to_
        self.text = text
        log.debug("Translate from %s to %s" % (from_, to_))

    @staticmethod
    def _fix_result(text: str) -> str:
        end_chars = [".", "!", "?"]
        for i in end_chars:
            text = f"{i}\x20".join(text.split(i))
        return text

    @property
    def _translate(self) -> str:
        return self.gtranslate.translate(
            text=self.text, source_language=self.from_,
            destination_language=self.to_).result

    def __str__(self) -> str:
        return self._fix_result(self._translate)
