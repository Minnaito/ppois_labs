import unittest
from src.dictionary_node import dictionary_node  # ← ИЗМЕНИЛ ИМПОРТ

class test_dictionary_node(unittest.TestCase):

    def test_node_creation(self):
        node = dictionary_node("hello", "привет")

        self.assertEqual(node.english_word, "hello")
        self.assertEqual(node.russian_translation, "привет")
        self.assertIsNone(node.left_child)
        self.assertIsNone(node.right_child)

    def test_node_string_representation(self):
        node = dictionary_node("test", "тест")
        expected_string = "test:тест"

        self.assertEqual(str(node), expected_string)

    def test_node_repr_representation(self):
        node = dictionary_node("sample", "пример")
        expected_repr = "dictionary_node('sample', 'пример')"

        self.assertEqual(repr(node), expected_repr)

    def test_node_with_children(self):
        parent = dictionary_node("parent", "родитель")
        left_child = dictionary_node("left", "левый")
        right_child = dictionary_node("right", "правый")

        parent.left_child = left_child
        parent.right_child = right_child

        self.assertEqual(parent.left_child, left_child)
        self.assertEqual(parent.right_child, right_child)
        self.assertEqual(parent.left_child.english_word, "left")
        self.assertEqual(parent.right_child.english_word, "right")

    def test_node_comparison(self):
        node1 = dictionary_node("apple", "яблоко")
        node2 = dictionary_node("banana", "банан")
        node3 = dictionary_node("apple", "другое_яблоко")  # Same English word

        self.assertEqual(node1.english_word, node3.english_word)
        self.assertNotEqual(node1.russian_translation, node3.russian_translation)
        self.assertNotEqual(node1.english_word, node2.english_word)


if __name__ == '__main__':
    unittest.main(verbosity=2)
