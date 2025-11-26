import unittest
import os
import tempfile
import ctypes
from src.EnglishRussianDict import EnglishRussianDict


class TestEnglishRussianDict(unittest.TestCase):

    def setUp(self):
        self.dictionary = EnglishRussianDict()

    def testInitialDictionaryIsEmpty(self):
        self.assertEqual(len(self.dictionary), 0)
        self.assertTrue(self.dictionary.isEmpty())

    def testAddWordSuccessfully(self):
        result = self.dictionary.addWord("hello", "привет")
        self.assertTrue(result)
        self.assertEqual(len(self.dictionary), 1)
        self.assertFalse(self.dictionary.isEmpty())

    def testAddDuplicateWordFails(self):
        self.dictionary.addWord("hello", "привет")
        result = self.dictionary.addWord("hello", "здравствуйте")
        self.assertFalse(result)
        self.assertEqual(len(self.dictionary), 1)

    def testSearchExistingWord(self):
        self.dictionary.addWord("hello", "привет")
        translation = self.dictionary.searchTranslation("hello")
        self.assertEqual(translation, "привет")

    def testSearchNonexistentWord(self):
        translation = self.dictionary.searchTranslation("nonexistent")
        self.assertIsNone(translation)

    def testRemoveExistingWord(self):
        self.dictionary.addWord("hello", "привет")
        result = self.dictionary.removeWord("hello")
        self.assertTrue(result)
        self.assertEqual(len(self.dictionary), 0)

    def testRemoveNonexistentWord(self):
        result = self.dictionary.removeWord("nonexistent")
        self.assertFalse(result)

    def testUpdateExistingTranslation(self):
        self.dictionary.addWord("hello", "привет")
        result = self.dictionary.updateTranslation("hello", "здравствуйте")
        self.assertTrue(result)
        self.assertEqual(self.dictionary.searchTranslation("hello"), "здравствуйте")

    def testUpdateNonexistentWord(self):
        result = self.dictionary.updateTranslation("nonexistent", "перевод")
        self.assertFalse(result)

    def testCaseInsensitiveOperations(self):
        self.dictionary.addWord("Hello", "привет")
        self.assertEqual(self.dictionary.searchTranslation("HELLO"), "привет")
        self.assertTrue(self.dictionary.removeWord("hello"))

    def testOperatorOverloads(self):
        # Test += operator
        self.dictionary += ("hello", "привет")
        self.assertEqual(self.dictionary["hello"], "привет")

        # Test -= operator
        self.dictionary -= "hello"
        with self.assertRaises(KeyError):
            _ = self.dictionary["hello"]

        # Test [] operator for update
        self.dictionary.addWord("test", "тест")
        self.dictionary["test"] = "проверка"
        self.assertEqual(self.dictionary["test"], "проверка")

        # Test in operator
        self.dictionary.addWord("word", "слово")
        self.assertTrue("word" in self.dictionary)
        self.assertFalse("nonexistent" in self.dictionary)

    def testCStyleStringsSupport(self):
        cEnglish = ctypes.c_char_p(b"hello")
        cRussian = ctypes.c_char_p("привет".encode('utf-8'))

        result = self.dictionary.addWord(cEnglish, cRussian)
        self.assertTrue(result)
        self.assertEqual(self.dictionary.searchTranslation(cEnglish), "привет")

    def testFileOperations(self):
        testWords = [
            ("apple", "яблоко"),
            ("book", "книга"),
            ("cat", "кот")
        ]

        for english, russian in testWords:
            self.dictionary.addWord(english, russian)

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tempFile:
            tempPath = tempFile.name

        try:
            # Test save
            saveResult = self.dictionary.saveToFile(tempPath)
            self.assertTrue(saveResult)

            # Test load
            newDict = EnglishRussianDict()
            loadResult = newDict.loadFromFile(tempPath)
            self.assertTrue(loadResult)

            self.assertEqual(len(newDict), len(testWords))
            for english, russian in testWords:
                self.assertEqual(newDict.searchTranslation(english), russian)

        finally:
            if os.path.exists(tempPath):
                os.unlink(tempPath)

    def testValidationEmptyWords(self):
        result = self.dictionary.addWord("", "привет")
        self.assertFalse(result)

        result = self.dictionary.addWord("hello", "")
        self.assertFalse(result)

    def testValidationInvalidCharacters(self):
        result = self.dictionary.addWord("hello123", "привет")
        self.assertFalse(result)

        result = self.dictionary.addWord("hello", "privet")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
