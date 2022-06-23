from translatepy.translators.google import GoogleTranslate


class Translate:

    def __init__(self, from_: str, to_: str, text: str) -> None:
        self.gtranslate = GoogleTranslate()
        self.from_ = from_
        self.to_ = to_
        self.text = text

    @property
    def _translate(self) -> str:
        return self.gtranslate.translate(
            text=self.text, source_language=self.from_,
            destination_language=self.to_).result

    def __str__(self) -> str:
        return self._translate
