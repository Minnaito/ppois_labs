class DictionaryNode:

    __slots__ = ('english_word', 'russian_translation', 'left_child', 'right_child')

    def __init__(self, english_word: str, russian_translation: str):
        self.english_word = english_word
        self.russian_translation = russian_translation
        self.left_child = None
        self.right_child = None

    def __str__(self) -> str:
        return f"{self.english_word}:{self.russian_translation}"

    def __repr__(self) -> str:
        return f"dictionary_node('{self.english_word}', '{self.russian_translation}')"
