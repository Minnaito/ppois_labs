import re
from typing import Optional, Tuple, List
import ctypes

from src.dictionary_node import dictionary_node


class english_russian_dict:

    MAX_WORD_LENGTH = 50
    MAX_TRANSLATION_LENGTH = 200
    ENGLISH_WORD_PATTERN = r'^[a-zA-Z\s\-]+$'
    RUSSIAN_TRANSLATION_PATTERN = r'^[а-яА-ЯёЁ\s\-]+$'
    FILE_DELIMITER = ':'
    FILE_ENCODING = 'utf-8'

    def __init__(self):
        self._root_node = None
        self._word_count = 0

    def _convert_to_string(self, text) -> str:
        if isinstance(text, ctypes.c_char_p):
            return text.value.decode('utf-8') if text.value else ""
        return str(text)

    def _validate_word_input(self, english_word, russian_translation) -> bool:
        english_str = self._convert_to_string(english_word).strip()
        russian_str = self._convert_to_string(russian_translation).strip()

        if not english_str or not russian_str:
            return False

        if len(english_str) > self.MAX_WORD_LENGTH:
            return False

        if len(russian_str) > self.MAX_TRANSLATION_LENGTH:
            return False

        if not re.match(self.ENGLISH_WORD_PATTERN, english_str):
            return False

        if not re.match(self.RUSSIAN_TRANSLATION_PATTERN, russian_str):
            return False

        return True

    def _compare_words(self, first_word: str, second_word: str) -> int:
        first_normalized = first_word.lower()
        second_normalized = second_word.lower()

        if first_normalized < second_normalized:
            return -1
        elif first_normalized > second_normalized:
            return 1
        return 0

    def add_word(self, english_word, russian_translation) -> bool:
        if not self._validate_word_input(english_word, russian_translation):
            return False

        english_str = self._convert_to_string(english_word).strip()
        russian_str = self._convert_to_string(russian_translation).strip()

        normalized_english = english_str.lower()

        new_node = dictionary_node(normalized_english, russian_str)

        if self._root_node is None:
            self._root_node = new_node
            self._word_count += 1
            return True

        return self._insert_node(self._root_node, new_node)

    def _insert_node(self, current_node: dictionary_node, new_node: dictionary_node) -> bool:
        comparison_result = self._compare_words(new_node.english_word, current_node.english_word)

        if comparison_result == 0:
            return False
        elif comparison_result < 0:
            if current_node.left_child is None:
                current_node.left_child = new_node
                self._word_count += 1
                return True
            return self._insert_node(current_node.left_child, new_node)
        else:
            if current_node.right_child is None:
                current_node.right_child = new_node
                self._word_count += 1
                return True
            return self._insert_node(current_node.right_child, new_node)

    def remove_word(self, english_word) -> bool:
        english_str = self._convert_to_string(english_word).lower().strip()
        if not english_str:
            return False

        initial_count = self._word_count
        self._root_node = self._remove_node(self._root_node, english_str)
        return self._word_count < initial_count

    def _remove_node(self, node: Optional[dictionary_node], english_word: str) -> Optional[dictionary_node]:
        if node is None:
            return None

        comparison_result = self._compare_words(english_word, node.english_word)

        if comparison_result < 0:
            node.left_child = self._remove_node(node.left_child, english_word)
        elif comparison_result > 0:
            node.right_child = self._remove_node(node.right_child, english_word)
        else:
            self._word_count -= 1

            if node.left_child is None:
                return node.right_child
            if node.right_child is None:
                return node.left_child

            min_node = self._find_min_node(node.right_child)

            node.english_word = min_node.english_word
            node.russian_translation = min_node.russian_translation

            node.right_child = self._remove_node(node.right_child, min_node.english_word)

        return node

    def _find_min_node(self, node: dictionary_node) -> dictionary_node:
        current = node
        while current.left_child is not None:
            current = current.left_child
        return current

    def search_translation(self, english_word) -> Optional[str]:
        english_str = self._convert_to_string(english_word).lower().strip()
        if not english_str:
            return None

        return self._search_node(self._root_node, english_str)

    def _search_node(self, node: Optional[dictionary_node], english_word: str) -> Optional[str]:
        if node is None:
            return None

        comparison_result = self._compare_words(english_word, node.english_word)

        if comparison_result == 0:
            return node.russian_translation
        elif comparison_result < 0:
            return self._search_node(node.left_child, english_word)
        else:
            return self._search_node(node.right_child, english_word)

    def update_translation(self, english_word, new_russian_translation) -> bool:
        if not self._validate_word_input(english_word, new_russian_translation):
            return False

        english_str = self._convert_to_string(english_word).lower().strip()
        new_russian_str = self._convert_to_string(new_russian_translation).strip()

        node = self._find_node(self._root_node, english_str)
        if node is None:
            return False

        node.russian_translation = new_russian_str
        return True

    def _find_node(self, node: Optional[dictionary_node], english_word: str) -> Optional[dictionary_node]:
        if node is None:
            return None

        comparison_result = self._compare_words(english_word, node.english_word)

        if comparison_result == 0:
            return node
        elif comparison_result < 0:
            return self._find_node(node.left_child, english_word)
        else:
            return self._find_node(node.right_child, english_word)

    def load_from_file(self, file_path: str) -> bool:
        try:
            with open(file_path, 'r', encoding=self.FILE_ENCODING) as file:
                success_count = 0
                for line_number, line in enumerate(file, 1):
                    if self._process_file_line(line.strip()):
                        success_count += 1
                return success_count > 0
        except (FileNotFoundError, PermissionError, UnicodeDecodeError):
            return False

    def _process_file_line(self, line: str) -> bool:
        if not line or line.startswith('#'):
            return False

        if self.FILE_DELIMITER not in line:
            return False

        parts = line.split(self.FILE_DELIMITER, 1)
        if len(parts) != 2:
            return False

        english_word, russian_translation = parts

        # Проверяем что обе части не пустые после strip
        english_clean = english_word.strip()
        russian_clean = russian_translation.strip()

        if not english_clean or not russian_clean:
            return False

        return self.add_word(english_clean, russian_clean)

    def save_to_file(self, file_path: str) -> bool:
        try:
            with open(file_path, 'w', encoding=self.FILE_ENCODING) as file:
                file.write("# English-Russian Dictionary\n")
                file.write(f"# Total words: {self._word_count}\n")
                file.write(f"# Format: english_word{self.FILE_DELIMITER}russian_translation\n\n")
                self._save_tree_to_file(self._root_node, file)
            return True
        except (PermissionError, OSError):
            return False

    def _save_tree_to_file(self, node: Optional[dictionary_node], file):
        if node is None:
            return

        self._save_tree_to_file(node.left_child, file)
        file.write(f"{node}\n")
        self._save_tree_to_file(node.right_child, file)

    def display_all_words(self) -> List[Tuple[str, str]]:
        word_list = []
        self._collect_words_in_order(self._root_node, word_list)
        return word_list

    def _collect_words_in_order(self, node: Optional[dictionary_node], word_list: List[Tuple[str, str]]):
        if node is None:
            return

        self._collect_words_in_order(node.left_child, word_list)
        word_list.append((node.english_word, node.russian_translation))
        self._collect_words_in_order(node.right_child, word_list)

    def get_word_count(self) -> int:
        return self._word_count

    def is_empty(self) -> bool:
        return self._root_node is None

    # Operator overloads
    def __iadd__(self, word_pair: Tuple[str, str]) -> 'english_russian_dict':
        if not isinstance(word_pair, (tuple, list)) or len(word_pair) != 2:
            raise ValueError("Expected tuple (english_word, russian_translation)")

        self.add_word(word_pair[0], word_pair[1])
        return self

    def __isub__(self, english_word: str) -> 'english_russian_dict':
        if not isinstance(english_word, str):
            raise ValueError("English word must be a string")

        self.remove_word(english_word)
        return self

    def __getitem__(self, english_word: str) -> str:
        if not isinstance(english_word, str):
            raise KeyError("English word must be a string")

        translation = self.search_translation(english_word)
        if translation is None:
            raise KeyError(f"Word '{english_word}' not found in dictionary")
        return translation

    def __setitem__(self, english_word: str, russian_translation: str):
        if not isinstance(english_word, str) or not isinstance(russian_translation, str):
            raise TypeError("Both arguments must be strings")

        if not self.update_translation(english_word, russian_translation):
            raise KeyError(f"Word '{english_word}' not found in dictionary")

    def __contains__(self, english_word: str) -> bool:
        return self.search_translation(english_word) is not None

    def __len__(self) -> int:
        return self._word_count

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __str__(self) -> str:
        words = self.display_all_words()
        if not words:
            return "Dictionary is empty"

        word_strings = [f"{eng} -> {rus}" for eng, rus in words]
        return "\n".join(word_strings)

    def __repr__(self) -> str:
        return f"english_russian_dict(words={self._word_count})"
