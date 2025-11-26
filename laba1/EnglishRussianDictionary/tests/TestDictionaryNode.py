import unittest
from src.DictionaryNode import DictionaryNode

class TestDictionaryNode(unittest.TestCase):

    def testNodeCreation(self):
        node = DictionaryNode("hello", "привет")

        self.assertEqual(node.englishWord, "hello")
        self.assertEqual(node.russianTranslation, "привет")
        self.assertIsNone(node.leftChild)
        self.assertIsNone(node.rightChild)

    def testNodeStringRepresentation(self):
        node = DictionaryNode("test", "тест")
        expectedString = "test:тест"

        self.assertEqual(str(node), expectedString)

    def testNodeReprRepresentation(self):
        node = DictionaryNode("sample", "пример")
        expectedRepr = "DictionaryNode('sample', 'пример')"

        self.assertEqual(repr(node), expectedRepr)

    def testNodeWithChildren(self):
        parent = DictionaryNode("parent", "родитель")
        leftChild = DictionaryNode("left", "левый")
        rightChild = DictionaryNode("right", "правый")

        parent.leftChild = leftChild
        parent.rightChild = rightChild

        self.assertEqual(parent.leftChild, leftChild)
        self.assertEqual(parent.rightChild, rightChild)
        self.assertEqual(parent.leftChild.englishWord, "left")
        self.assertEqual(parent.rightChild.englishWord, "right")

    def testNodeComparison(self):
        node1 = DictionaryNode("apple", "яблоко")
        node2 = DictionaryNode("banana", "банан")
        node3 = DictionaryNode("apple", "другое_яблоко")  # Same English word

        self.assertEqual(node1.englishWord, node3.englishWord)
        self.assertNotEqual(node1.russianTranslation, node3.russianTranslation)
        self.assertNotEqual(node1.englishWord, node2.englishWord)


if __name__ == '__main__':
    unittest.main(verbosity=2)
