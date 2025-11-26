import unittest
import os
import tempfile
import ctypes
from src.EnglishRussianDict import EnglishRussianDict

class TestEnglishRussianDictEdgeCases(unittest.TestCase):

    def setUp(self):
        self.dictionary = EnglishRussianDict()

    def testFileOperationsErrorConditions(self):
        result = self.dictionary.loadFromFile("nonExistentFile12345.txt")
        self.assertFalse(result)

        result = self.dictionary.loadFromFile("")
        self.assertFalse(result)

        result = self.dictionary.saveToFile("")
        self.assertFalse(result)

    def testFileWithOnlyCommentsAndWhitespace(self):
        fileContent = "# Comment line 1\n# Comment line 2\n   \n\t\n# Another comment"

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as tempFile:
            tempPath = tempFile.name
            tempFile.write(fileContent)

        try:
            result = self.dictionary.loadFromFile(tempPath)
            self.assertFalse(result)  # No actual words to load
            self.assertEqual(len(self.dictionary), 0)
        finally:
            os.unlink(tempPath)

    def testBoundaryWordLengths(self):
        # Exactly maximum length
        maxEnglish = "a" * 50
        maxRussian = "б" * 200

        result = self.dictionary.addWord(maxEnglish, maxRussian)
        self.assertTrue(result)
        self.assertEqual(self.dictionary.searchTranslation(maxEnglish), maxRussian)

        # One character over maximum length
        tooLongEnglish = "a" * 51
        tooLongRussian = "б" * 201

        result = self.dictionary.addWord(tooLongEnglish, "test")
        self.assertFalse(result)

        result = self.dictionary.addWord("test", tooLongRussian)
        self.assertFalse(result)

    def testSpecialCharactersInWords(self):
        # Valid cases with hyphens and spaces
        validCases = [
            ("hello-world", "привет-мир"),
            ("state of art", "состояние искусства"),
            ("well-known", "хорошо-известный"),
        ]

        for english, russian in validCases:
            result = self.dictionary.addWord(english, russian)
            self.assertTrue(result, f"Should accept: {english}")

        invalidCases = [
            ("hello!", "привет"),
            ("test123", "тест"),
            ("price$", "цена"),
            ("email@domain", "емейл"),
        ]

        for english, russian in invalidCases:
            result = self.dictionary.addWord(english, russian)
            self.assertFalse(result, f"Should reject: {english}")

    def testWhitespaceTrimming(self):
        result = self.dictionary.addWord("  hello  ", "  привет  ")
        self.assertTrue(result)
        self.assertEqual(self.dictionary.searchTranslation("hello"), "привет")

        # Search should work with trimmed version
        self.assertEqual(self.dictionary.searchTranslation("  hello  "), "привет")

    def testEmptyAndWhitespaceOnlyWords(self):
        emptyCases = [
            ("", "привет"),
            ("hello", ""),
            ("   ", "привет"),
            ("hello", "   "),
            ("\t\n", "привет"),
            ("hello", "\t\n"),
        ]

        for english, russian in emptyCases:
            result = self.dictionary.addWord(english, russian)
            self.assertFalse(result, f"Should reject: '{english}' -> '{russian}'")

    def testOperatorErrorHandling(self):
        # Test += with invalid inputs
        with self.assertRaises(ValueError):
            self.dictionary += ("single",)  # Not enough values

        with self.assertRaises(ValueError):
            self.dictionary += "notATuple"  # Wrong type

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

    def testCStyleStringsEdgeCases(self):
        noneString = ctypes.c_char_p(None)
        result = self.dictionary.addWord(noneString, "test")
        self.assertFalse(result)

        result = self.dictionary.addWord("test", noneString)
        self.assertFalse(result)

        emptyString = ctypes.c_char_p(b"")
        result = self.dictionary.addWord(emptyString, "test")
        self.assertFalse(result)

    def testDisplayMethodsEdgeCases(self):
        emptyList = self.dictionary.displayAllWords()
        self.assertEqual(emptyList, [])
        self.assertEqual(str(self.dictionary), "Dictionary is empty")

        self.dictionary.addWord("single", "один")
        singleList = self.dictionary.displayAllWords()
        self.assertEqual(len(singleList), 1)
        self.assertIn("single -> один", str(self.dictionary))

    def testBooleanRepresentation(self):
        # Empty dictionary should be falsy
        self.assertFalse(self.dictionary)
        self.assertFalse(bool(self.dictionary))

        self.dictionary.addWord("test", "тест")
        self.assertTrue(self.dictionary)
        self.assertTrue(bool(self.dictionary))

        self.dictionary.removeWord("test")
        self.assertFalse(self.dictionary)

    def testReprRepresentation(self):
        reprEmpty = repr(self.dictionary)
        self.assertIn("EnglishRussianDict", reprEmpty)
        self.assertIn("words=0", reprEmpty)

        self.dictionary.addWord("test", "тест")
        reprWithWords = repr(self.dictionary)
        self.assertIn("words=1", reprWithWords)

    def testContainsOperator(self):
        self.assertFalse("test" in self.dictionary)

        self.dictionary.addWord("test", "тест")
        self.assertTrue("test" in self.dictionary)
        self.assertFalse("nonexistent" in self.dictionary)

        self.dictionary.removeWord("test")
        self.assertFalse("test" in self.dictionary)

    def testGetWordCountMethod(self):
        self.assertEqual(self.dictionary.getWordCount(), 0)

        self.dictionary.addWord("test", "тест")
        self.assertEqual(self.dictionary.getWordCount(), 1)
        self.assertEqual(self.dictionary.getWordCount(), len(self.dictionary))

        self.dictionary.removeWord("test")
        self.assertEqual(self.dictionary.getWordCount(), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
