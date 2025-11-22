import unittest
from src.DictionaryNode import DictionaryNode

class TestDictionaryNode(unittest.TestCase):

    def test_node_creation(self):
        node = DictionaryNode("hello", "привет")

        self.assertEqual(node.english_word, "hello")
        self.assertEqual(node.russian_translation, "привет")
        self.assertIsNone(node.left_child)
        self.assertIsNone(node.right_child)

    def test_node_string_representation(self):
        node = DictionaryNode("test", "тест")
        expected_string = "test:тест"

        self.assertEqual(str(node), expected_string)

    def test_node_repr_representation(self):
        node = DictionaryNode("sample", "пример")
        expected_repr = "DictionaryNode('sample', 'пример')"

        self.assertEqual(repr(node), expected_repr)

    def test_node_with_children(self):
        parent = DictionaryNode("parent", "родитель")
        left_child = DictionaryNode("left", "левый")
        right_child = DictionaryNode("right", "правый")

        parent.left_child = left_child
        parent.right_child = right_child

        self.assertEqual(parent.left_child, left_child)
        self.assertEqual(parent.right_child, right_child)
        self.assertEqual(parent.left_child.english_word, "left")
        self.assertEqual(parent.right_child.english_word, "right")

    def test_node_comparison(self):
        node1 = DictionaryNode("apple", "яблоко")
        node2 = DictionaryNode("banana", "банан")
        node3 = DictionaryNode("apple", "другое_яблоко")  # Same English word

        self.assertEqual(node1.english_word, node3.english_word)
        self.assertNotEqual(node1.russian_translation, node3.russian_translation)
        self.assertNotEqual(node1.english_word, node2.english_word)


if __name__ == '__main__':
    unittest.main(verbosity=2)
