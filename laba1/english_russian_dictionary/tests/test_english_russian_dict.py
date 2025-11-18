import unittest
import os
import tempfile
import ctypes
from src.english_russian_dict import english_russian_dict  # ← ИЗМЕНИЛ ИМПОРТ


class test_english_russian_dict(unittest.TestCase):

    def setUp(self):
        self.dictionary = english_russian_dict()

    def test_initial_dictionary_is_empty(self):
        self.assertEqual(len(self.dictionary), 0)
        self.assertTrue(self.dictionary.is_empty())

    def test_add_word_successfully(self):
        result = self.dictionary.add_word("hello", "привет")
        self.assertTrue(result)
        self.assertEqual(len(self.dictionary), 1)
        self.assertFalse(self.dictionary.is_empty())

    def test_add_duplicate_word_fails(self):
        self.dictionary.add_word("hello", "привет")
        result = self.dictionary.add_word("hello", "здравствуйте")
        self.assertFalse(result)
        self.assertEqual(len(self.dictionary), 1)

    def test_search_existing_word(self):
        self.dictionary.add_word("hello", "привет")
        translation = self.dictionary.search_translation("hello")
        self.assertEqual(translation, "привет")

    def test_search_nonexistent_word(self):
        translation = self.dictionary.search_translation("nonexistent")
        self.assertIsNone(translation)

    def test_remove_existing_word(self):
        self.dictionary.add_word("hello", "привет")
        result = self.dictionary.remove_word("hello")
        self.assertTrue(result)
        self.assertEqual(len(self.dictionary), 0)

    def test_remove_nonexistent_word(self):
        result = self.dictionary.remove_word("nonexistent")
        self.assertFalse(result)

    def test_update_existing_translation(self):
        self.dictionary.add_word("hello", "привет")
        result = self.dictionary.update_translation("hello", "здравствуйте")
        self.assertTrue(result)
        self.assertEqual(self.dictionary.search_translation("hello"), "здравствуйте")

    def test_update_nonexistent_word(self):
        result = self.dictionary.update_translation("nonexistent", "перевод")
        self.assertFalse(result)

    def test_case_insensitive_operations(self):
        self.dictionary.add_word("Hello", "привет")
        self.assertEqual(self.dictionary.search_translation("HELLO"), "привет")
        self.assertTrue(self.dictionary.remove_word("hello"))

    def test_operator_overloads(self):
        # Test += operator
        self.dictionary += ("hello", "привет")
        self.assertEqual(self.dictionary["hello"], "привет")

        # Test -= operator
        self.dictionary -= "hello"
        with self.assertRaises(KeyError):
            _ = self.dictionary["hello"]

        # Test [] operator for update
        self.dictionary.add_word("test", "тест")
        self.dictionary["test"] = "проверка"
        self.assertEqual(self.dictionary["test"], "проверка")

        # Test in operator
        self.dictionary.add_word("word", "слово")
        self.assertTrue("word" in self.dictionary)
        self.assertFalse("nonexistent" in self.dictionary)

    def test_c_style_strings_support(self):
        c_english = ctypes.c_char_p(b"hello")
        c_russian = ctypes.c_char_p("привет".encode('utf-8'))

        result = self.dictionary.add_word(c_english, c_russian)
        self.assertTrue(result)
        self.assertEqual(self.dictionary.search_translation(c_english), "привет")

    def test_file_operations(self):
        test_words = [
            ("apple", "яблоко"),
            ("book", "книга"),
            ("cat", "кот")
        ]

        for english, russian in test_words:
            self.dictionary.add_word(english, russian)

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_path = temp_file.name

        try:
            # Test save
            save_result = self.dictionary.save_to_file(temp_path)
            self.assertTrue(save_result)

            # Test load
            new_dict = english_russian_dict()
            load_result = new_dict.load_from_file(temp_path)
            self.assertTrue(load_result)

            self.assertEqual(len(new_dict), len(test_words))
            for english, russian in test_words:
                self.assertEqual(new_dict.search_translation(english), russian)

        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_validation_empty_words(self):
        result = self.dictionary.add_word("", "привет")
        self.assertFalse(result)

        result = self.dictionary.add_word("hello", "")
        self.assertFalse(result)

    def test_validation_invalid_characters(self):
        result = self.dictionary.add_word("hello123", "привет")
        self.assertFalse(result)

        result = self.dictionary.add_word("hello", "privet")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
