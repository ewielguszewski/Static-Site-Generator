import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_eq_props_to_html(self):
        node = HTMLNode("p", "content", None, {"href": "https://www.google.com","target": "_blank",})
        string = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), string)
        
    def test_eq_props_to_html2(self):
        node = HTMLNode("p", "content", None, {"href": "https://www.google.com"})
        string = ' href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), string)
        
    def test__not_eq_props_to_html(self):
        node = HTMLNode("p", "content", None, {"href": "https://www.google.pl","target": "_blank",})
        string = ' href="https://www.google.com" target="_blank"'
        self.assertNotEqual(node.props_to_html(), string)
    
    def test__not_eq_props_to_html2(self):
        node = HTMLNode("p", "content", None, {"href": "https://www.google.com","target": "_blank",})
        string = ' href="https://www.google.com"'
        self.assertNotEqual(node.props_to_html(), string)
        

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!")
        self.assertEqual(node.to_html(), "<a>Hello, world!</a>")
        
    def test_leaf_to_html_value(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
        
    def test_leaf_to_html__no_tag_props(self):
        node = LeafNode(None, "Hello, world!", {"key": "google.com"})
        self.assertEqual(node.to_html(), 'Hello, world!')

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Hello, world!", {"href": "google.com"})
        self.assertEqual(node.to_html(), '<a href="google.com">Hello, world!</a>')

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>",
    )
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>",
    )
    
    def test_to_html_with_nested_children(self):
        child_node1 = LeafNode("b", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><b>child1</b><span>child2</span></div>",
    )
        
    def test_to_html_with_nested_grandchildren_no_tag(self):
        grandgrandchild_node = LeafNode(None, "grandgrandchild")
        grandchild_node = ParentNode("b", [grandgrandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandgrandchild</b></span></div>",
    )
        
    
if __name__ == "__main__":
    unittest.main()
