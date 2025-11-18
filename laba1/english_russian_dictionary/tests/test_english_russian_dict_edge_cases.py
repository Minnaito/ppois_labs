
import unittest
import os
import tempfile
import ctypes
from src.english_russian_dict import english_russian_dict

class test_english_russian_dict_edge_cases(unittest.TestCase):

    def setUp(self):
        self.dictionary = english_russian_dict()

    def test_file_operations_error_conditions(self):
        result = self.dictionary.load_from_file("non_existent_file_12345.txt")
        self.assertFalse(result)

        result = self.dictionary.load_from_file("")
        self.assertFalse(result)

        result = self.dictionary.save_to_file("")
        self.assertFalse(result)

    def test_file_with_only_comments_and_whitespace(self):
        file_content = "# Comment line 1\n# Comment line 2\n   \n\t\n# Another comment"

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as temp_file:
            temp_path = temp_file.name
            temp_file.write(file_content)

        try:
            result = self.dictionary.load_from_file(temp_path)
            self.assertFalse(result)  # No actual words to load
            self.assertEqual(len(self.dictionary), 0)
        finally:
            os.unlink(temp_path)

    def test_boundary_word_lengths(self):
        # Exactly maximum length
        max_english = "a" * 50
        max_russian = "б" * 200

        result = self.dictionary.add_word(max_english, max_russian)
        self.assertTrue(result)
        self.assertEqual(self.dictionary.search_translation(max_english), max_russian)

        # One character over maximum length
        too_long_english = "a" * 51
        too_long_russian = "б" * 201

        result = self.dictionary.add_word(too_long_english, "test")
        self.assertFalse(result)

        result = self.dictionary.add_word("test", too_long_russian)
        self.assertFalse(result)

    def test_special_characters_in_words(self):
        # Valid cases with hyphens and spaces
        valid_cases = [
            ("hello-world", "привет-мир"),
            ("state of art", "состояние искусства"),
            ("well-known", "хорошо-известный"),
        ]

        for english, russian in valid_cases:
            result = self.dictionary.add_word(english, russian)
            self.assertTrue(result, f"Should accept: {english}")

        invalid_cases = [
            ("hello!", "привет"),
            ("test123", "тест"),
            ("price$", "цена"),
            ("email@domain", "емейл"),
        ]

        for english, russian in invalid_cases:
            result = self.dictionary.add_word(english, russian)
            self.assertFalse(result, f"Should reject: {english}")

    def test_whitespace_trimming(self):
        result = self.dictionary.add_word("  hello  ", "  привет  ")
        self.assertTrue(result)
        self.assertEqual(self.dictionary.search_translation("hello"), "привет")

        # Search should work with trimmed version
        self.assertEqual(self.dictionary.search_translation("  hello  "), "привет")

    def test_empty_and_whitespace_only_words(self):
        empty_cases = [
            ("", "привет"),
            ("hello", ""),
            ("   ", "привет"),
            ("hello", "   "),
            ("\t\n", "привет"),
            ("hello", "\t\n"),
        ]

        for english, russian in empty_cases:
            result = self.dictionary.add_word(english, russian)
            self.assertFalse(result, f"Should reject: '{english}' -> '{russian}'")

    def test_operator_error_handling(self):
        # Test += with invalid inputs
        with self.assertRaises(ValueError):
            self.dictionary += ("single",)  # Not enough values

        with self.assertRaises(ValueError):
            self.dictionary += "not_a_tuple"  # Wrong type

        with self.assertRaises(ValueError):
            self.dictionary += ("a", "b", "c")  # Too many values

        # Test -= with invalid inputs
        with self.assertRaises(ValueError):
            self.dictionary -= 123  # Not a string

        with self.assertRaises(ValueError):
            self.dictionary -= None  # Wrong type

        # Test [] with invalid inputs
        with self.assertRaises(KeyError):
            _ = self.dictionary["nonexistent"]

        with self.assertRaises(KeyError):
            self.dictionary["nonexistent"] = "translation"

        with self.assertRaises(TypeError):
            self.dictionary[123] = "translation"

    def test_c_style_strings_edge_cases(self):
        none_string = ctypes.c_char_p(None)
        result = self.dictionary.add_word(none_string, "test")
        self.assertFalse(result)

        result = self.dictionary.add_word("test", none_string)
        self.assertFalse(result)

        empty_string = ctypes.c_char_p(b"")
        result = self.dictionary.add_word(empty_string, "test")
        self.assertFalse(result)

    def test_display_methods_edge_cases(self):
        empty_list = self.dictionary.display_all_words()
        self.assertEqual(empty_list, [])
        self.assertEqual(str(self.dictionary), "Dictionary is empty")

        self.dictionary.add_word("single", "один")
        single_list = self.dictionary.display_all_words()
        self.assertEqual(len(single_list), 1)
        self.assertIn("single -> один", str(self.dictionary))

    def test_boolean_representation(self):
        # Empty dictionary should be falsy
        self.assertFalse(self.dictionary)
        self.assertFalse(bool(self.dictionary))

        self.dictionary.add_word("test", "тест")
        self.assertTrue(self.dictionary)
        self.assertTrue(bool(self.dictionary))

        self.dictionary.remove_word("test")
        self.assertFalse(self.dictionary)

    def test_repr_representation(self):
        repr_empty = repr(self.dictionary)
        self.assertIn("english_russian_dict", repr_empty)
        self.assertIn("words=0", repr_empty)

        self.dictionary.add_word("test", "тест")
        repr_with_words = repr(self.dictionary)
        self.assertIn("words=1", repr_with_words)

    def test_contains_operator(self):
        self.assertFalse("test" in self.dictionary)

        self.dictionary.add_word("test", "тест")
        self.assertTrue("test" in self.dictionary)
        self.assertFalse("nonexistent" in self.dictionary)

        self.dictionary.remove_word("test")
        self.assertFalse("test" in self.dictionary)

    def test_get_word_count_method(self):
        self.assertEqual(self.dictionary.get_word_count(), 0)

        self.dictionary.add_word("test", "тест")
        self.assertEqual(self.dictionary.get_word_count(), 1)
        self.assertEqual(self.dictionary.get_word_count(), len(self.dictionary))

        self.dictionary.remove_word("test")
        self.assertEqual(self.dictionary.get_word_count(), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
