import re
from typing import Optional, Tuple, List
import ctypes
from src.DictionaryNode import DictionaryNode

class EnglishRussianDict:
    MAX_WORD_LENGTH = 50
    MAX_TRANSLATION_LENGTH = 200
    ENGLISH_WORD_PATTERN = r'^[a-zA-Z\s\-]+$'
    RUSSIAN_TRANSLATION_PATTERN = r'^[а-яА-ЯёЁ\s\-]+$'
    FILE_DELIMITER = ':'
    FILE_ENCODING = 'utf-8'

    def __init__(self):
        self._rootNode = None
        self._wordCount = 0

    def _convertToString(self, text) -> str:
        if isinstance(text, ctypes.c_char_p):
            return text.value.decode('utf-8') if text.value else ""
        return str(text)

    def _validateWordInput(self, englishWord, russianTranslation) -> bool:
        englishStr = self._convertToString(englishWord).strip()
        russianStr = self._convertToString(russianTranslation).strip()

        if not englishStr or not russianStr:
            return False
        if len(englishStr) > self.MAX_WORD_LENGTH:
            return False
        if len(russianStr) > self.MAX_TRANSLATION_LENGTH:
            return False
        if not re.match(self.ENGLISH_WORD_PATTERN, englishStr):
            return False
        if not re.match(self.RUSSIAN_TRANSLATION_PATTERN, russianStr):
            return False
        return True

    def _compareWords(self, firstWord: str, secondWord: str) -> int:
        firstNormalized = firstWord.lower()
        secondNormalized = secondWord.lower()
        if firstNormalized < secondNormalized:
            return -1
        elif firstNormalized > secondNormalized:
            return 1
        return 0

    def addWord(self, englishWord, russianTranslation) -> bool:
        if not self._validateWordInput(englishWord, russianTranslation):
            return False

        englishStr = self._convertToString(englishWord).strip()
        russianStr = self._convertToString(russianTranslation).strip()
        normalizedEnglish = englishStr.lower()

        newNode = DictionaryNode(normalizedEnglish, russianStr)

        if self._rootNode is None:
            self._rootNode = newNode
            self._wordCount += 1
            return True

        return self._insertNode(self._rootNode, newNode)

    def _insertNode(self, currentNode: DictionaryNode, newNode: DictionaryNode) -> bool:
        comparisonResult = self._compareWords(newNode.englishWord, currentNode.englishWord)

        if comparisonResult == 0:
            return False
        elif comparisonResult < 0:
            if currentNode.leftChild is None:
                currentNode.leftChild = newNode
                self._wordCount += 1
                return True
            return self._insertNode(currentNode.leftChild, newNode)
        else:
            if currentNode.rightChild is None:
                currentNode.rightChild = newNode
                self._wordCount += 1
                return True
            return self._insertNode(currentNode.rightChild, newNode)

    def removeWord(self, englishWord) -> bool:
        englishStr = self._convertToString(englishWord).lower().strip()
        if not englishStr:
            return False

        initialCount = self._wordCount
        self._rootNode = self._removeNode(self._rootNode, englishStr)
        return self._wordCount < initialCount

    def _removeNode(self, node: Optional[DictionaryNode], englishWord: str) -> Optional[DictionaryNode]:
        if node is None:
            return None

        comparisonResult = self._compareWords(englishWord, node.englishWord)

        if comparisonResult < 0:
            node.leftChild = self._removeNode(node.leftChild, englishWord)
        elif comparisonResult > 0:
            node.rightChild = self._removeNode(node.rightChild, englishWord)
        else:
            self._wordCount -= 1

            if node.leftChild is None:
                return node.rightChild
            elif node.rightChild is None:
                return node.leftChild

            minNode = self._findMinNode(node.rightChild)
            node.englishWord = minNode.englishWord
            node.russianTranslation = minNode.russianTranslation
            node.rightChild = self._removeMinNode(node.rightChild)

        return node

    def _removeMinNode(self, node: DictionaryNode) -> Optional[DictionaryNode]:
        if node.leftChild is None:
            return node.rightChild
        node.leftChild = self._removeMinNode(node.leftChild)
        return node

    def _findMinNode(self, node: DictionaryNode) -> DictionaryNode:
        current = node
        while current.leftChild is not None:
            current = current.leftChild
        return current

    def searchTranslation(self, englishWord) -> Optional[str]:
        englishStr = self._convertToString(englishWord).lower().strip()
        if not englishStr:
            return None
        return self._searchNode(self._rootNode, englishStr)

    def _searchNode(self, node: Optional[DictionaryNode], englishWord: str) -> Optional[str]:
        if node is None:
            return None

        comparisonResult = self._compareWords(englishWord, node.englishWord)

        if comparisonResult == 0:
            return node.russianTranslation
        elif comparisonResult < 0:
            return self._searchNode(node.leftChild, englishWord)
        else:
            return self._searchNode(node.rightChild, englishWord)

    def updateTranslation(self, englishWord, newRussianTranslation) -> bool:
        if not self._validateWordInput(englishWord, newRussianTranslation):
            return False

        englishStr = self._convertToString(englishWord).lower().strip()
        newRussianStr = self._convertToString(newRussianTranslation).strip()

        node = self._findNode(self._rootNode, englishStr)
        if node is None:
            return False

        node.russianTranslation = newRussianStr
        return True

    def _findNode(self, node: Optional[DictionaryNode], englishWord: str) -> Optional[DictionaryNode]:
        if node is None:
            return None

        comparisonResult = self._compareWords(englishWord, node.englishWord)

        if comparisonResult == 0:
            return node
        elif comparisonResult < 0:
            return self._findNode(node.leftChild, englishWord)
        else:
            return self._findNode(node.rightChild, englishWord)

    def loadFromFile(self, filePath: str) -> bool:
        try:
            with open(filePath, 'r', encoding=self.FILE_ENCODING) as file:
                successCount = 0
                for lineNumber, line in enumerate(file, 1):
                    if self._processFileLine(line.strip()):
                        successCount += 1
                return successCount > 0
        except (FileNotFoundError, PermissionError, UnicodeDecodeError):
            return False

    def _processFileLine(self, line: str) -> bool:
        if not line or line.startswith('#'):
            return False
        if self.FILE_DELIMITER not in line:
            return False

        parts = line.split(self.FILE_DELIMITER, 1)
        if len(parts) != 2:
            return False

        englishWord, russianTranslation = parts
        englishClean = englishWord.strip()
        russianClean = russianTranslation.strip()

        if not englishClean or not russianClean:
            return False

        return self.addWord(englishClean, russianClean)

    def saveToFile(self, filePath: str) -> bool:
        try:
            with open(filePath, 'w', encoding=self.FILE_ENCODING) as file:
                file.write("# English-Russian Dictionary\n")
                file.write(f"# Total words: {self._wordCount}\n")
                file.write(f"# Format: english_word{self.FILE_DELIMITER}russian_translation\n\n")
                self._saveTreeToFile(self._rootNode, file)
            return True
        except (PermissionError, OSError):
            return False

    def _saveTreeToFile(self, node: Optional[DictionaryNode], file):
        if node is None:
            return
        self._saveTreeToFile(node.leftChild, file)
        file.write(f"{node}\n")
        self._saveTreeToFile(node.rightChild, file)

    def displayAllWords(self) -> List[Tuple[str, str]]:
        wordList = []
        self._collectWordsInOrder(self._rootNode, wordList)
        return wordList

    def _collectWordsInOrder(self, node: Optional[DictionaryNode], wordList: List[Tuple[str, str]]):
        if node is None:
            return
        self._collectWordsInOrder(node.leftChild, wordList)
        wordList.append((node.englishWord, node.russianTranslation))
        self._collectWordsInOrder(node.rightChild, wordList)

    def getWordCount(self) -> int:
        return self._wordCount

    def isEmpty(self) -> bool:
        return self._rootNode is None

    def __iadd__(self, wordPair: Tuple[str, str]) -> 'EnglishRussianDict':
        if not isinstance(wordPair, (tuple, list)) or len(wordPair) != 2:
            raise ValueError("Expected tuple (englishWord, russianTranslation)")
        self.addWord(wordPair[0], wordPair[1])
        return self

    def __isub__(self, englishWord: str) -> 'EnglishRussianDict':
        if not isinstance(englishWord, str):
            raise ValueError("English word must be a string")
        self.removeWord(englishWord)
        return self

    def __getitem__(self, englishWord: str) -> str:
        if not isinstance(englishWord, str):
            raise KeyError("English word must be a string")
        translation = self.searchTranslation(englishWord)
        if translation is None:
            raise KeyError(f"Word '{englishWord}' not found in dictionary")
        return translation

    def __setitem__(self, englishWord: str, russianTranslation: str):
        if not isinstance(englishWord, str) or not isinstance(russianTranslation, str):
            raise TypeError("Both arguments must be strings")
        if not self.updateTranslation(englishWord, russianTranslation):
            raise KeyError(f"Word '{englishWord}' not found in dictionary")

    def __contains__(self, englishWord: str) -> bool:
        return self.searchTranslation(englishWord) is not None

    def __len__(self) -> int:
        return self._wordCount

    def __bool__(self) -> bool:
        return not self.isEmpty()

    def __str__(self) -> str:
        words = self.displayAllWords()
        if not words:
            return "Dictionary is empty"
        wordStrings = [f"{eng} -> {rus}" for eng, rus in words]
        return "\n".join(wordStrings)

    def __repr__(self) -> str:
        return f"EnglishRussianDict(words={self._wordCount})"
