import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from text_parser import text_to_textnodes, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "url")
        node2 = TextNode("This is a text node", TextType.BOLD, "url")
        self.assertEqual(node, node2)
        
    def test_not_eq_diff_TextType(self):
        node = TextNode("This is a text node", TextType.LINK, "url")
        node2 = TextNode("This is a text node", TextType.BOLD, "url")
        self.assertNotEqual(node, node2)
    def test_not_eq_diff_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "url")
        node2 = TextNode("This is a text node", TextType.BOLD, "url2")
        self.assertNotEqual(node, node2)
    def test_not_eq_oneNodeWithNoUrl(self):
        node = TextNode("This is a text node", TextType.BOLD, "url")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

class Test_Split_Node_Delimiters(unittest.TestCase):
    def test_eq_split_node_delimiters_with_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [ TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),])
        
    def test_eq_split_node_delimiters_with_double_code(self):
        node = TextNode("`This` is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [ TextNode("This", TextType.CODE), TextNode(" is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),])
        
    def test_eq_split_node_delimiters_with__just_code(self):
        node = TextNode("`This is text with a `", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [ TextNode("This is text with a ", TextType.CODE)])
        
    def test_not_eq_split_node_delimiters_with_code(self):
        node = TextNode("This is text with a `code` `block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertNotEqual(new_nodes, [ TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),])
        
    def test_not_eq_split_node_delimiters_odd_delimiters_no(self):
        node = TextNode("This is text with a `code `block` word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)
            
    def test_eq_split_node_delimiters_with_bold(self):
        node = TextNode("This is text with a **code block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [ TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.BOLD),
    TextNode(" word", TextType.TEXT),])
        
    def test_eq_split_node_delimiters_with_italic(self):
        node = TextNode("This is _text_ with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [ TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.ITALIC),
    TextNode(" with a `code block` word", TextType.TEXT),])
        
    def test_eq_split_node_delimiters_clear_text(self):
        node = TextNode("This is text with a code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a code block word", TextType.TEXT)])
        
    def test_eq_split_node_delimiters_check_code_on_bold_textType(self):
        node = TextNode("**code block**", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [ TextNode("**code block**", TextType.BOLD)])
        
    def test_eq_split_node_delimiters_check_bold_on_bold_textType(self):
        node = TextNode("**code block**", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "", TextType.BOLD)
        self.assertEqual(new_nodes, [ TextNode("**code block**", TextType.BOLD)])
        
    def test_eq_split_node_delimiters_with_spaces(self):
        node = TextNode(" _test_ ", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode(" _test_ ", TextType.ITALIC)])
        
class Test_Extract_Markdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown__multiple_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://google.com)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [image](https://google.com)"
        )
        self.assertListEqual([("image", "https://google.com")], matches)  
        
    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with an [link1](https://google.com) and [link1][some link]"
        )
        self.assertListEqual([("link1", "https://google.com")], matches)
        
    def test_extract_markdown_multiple_links_return_both(self):
        matches = extract_markdown_links(
            "This is text with an [link1](https://google.com) and [link1](some link)"
        )
        self.assertListEqual([("link1", "https://google.com"), ("link1", "some link")], matches)
        
    def test_extract_markdown_adjacent_links(self):
        matches = extract_markdown_links(
            "[One](https://one.com)[Two](https://two.com)"
        )
        self.assertListEqual([("One", "https://one.com"), ("Two", "https://two.com")], matches) 
        
    def test_extract_markdown_query_links(self):
        matches = extract_markdown_links(
            "Here is some link [One](https://one.com/page?name=value#section)"
        )
        self.assertListEqual([("One", "https://one.com/page?name=value#section")], matches)   
    
    def test_extract_markdown_no_links(self):
        matches = extract_markdown_links(
            "Here is no link"
        )
        self.assertListEqual([], matches) 
    
class Test_Split_Images(unittest.TestCase):
    def test_split_nodes_image_without_link(self):
        node = TextNode(
            "This is text with no link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no link", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_split_nodes_image_single_with_text_after(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) ...",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" ...", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_split_nodes_image_single_with_no_text_after(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    
    def test_split_nodes_image_single_with_backspace_after(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )    
        
    def test_split_nodes_image_two_images_without_text_after(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
        
    def test_split_nodes_image_two_images_with_text_after(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" image", TextType.TEXT)
            ],
            new_nodes,
        )
        
    def test_split_nodes_image_two_images_and_link_without_text_after(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) [link](google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" [link](google.com)", TextType.TEXT),
            ],
            new_nodes,
        )
        
class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link_multiple_links(self):
        node = TextNode(
            "This is text with an [link](https://sth.com) and another [second link](https://site.com) and [link](google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://sth.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://site.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "google.com"),
            ],
            new_nodes,
        )
    
    def test_split_nodes_link_no_links(self):
        node = TextNode("This text has no links at all.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This text has no links at all.", TextType.TEXT)
            ],
            new_nodes,
        )
        
    def test_split_nodes_link_invalid_link(self):
        node = TextNode("This text contains an incomplete [link without URL]().", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This text contains an incomplete [link without URL]().", TextType.TEXT)
            ],
            new_nodes
        )
        
    def test_split_nodes_link_same_links(self):
        node = TextNode("Check the [repeated link](https://same.com) and again [repeated link](https://same.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check the ", TextType.TEXT),
                TextNode("repeated link", TextType.LINK, "https://same.com"),
                TextNode(" and again ", TextType.TEXT),
                TextNode("repeated link", TextType.LINK, "https://same.com")
            ],
            new_nodes
        )
        

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textNodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = [TextNode(text, TextType.TEXT)]
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        nodes = split_nodes_image(nodes)
        nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )
        
    def test_text_to_textnodes_empty_text(self):
        nodes = text_to_textnodes("")
        assert len(nodes) == 0
        
    def test_text_to_textnodes_with_mixed_formats(self):
        text = "This has **bold and _italic_** mixed formats"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 3
        assert nodes[0].text == "This has "
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[1].text == "bold and _italic_"
        assert nodes[1].text_type == TextType.BOLD
        assert nodes[2].text == " mixed formats"
        assert nodes[2].text_type == TextType.TEXT

    def test_text_to_textnodes_with_code_and_links(self):
        text = "Check this `code` and [this link](https://example.com)"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 4
        assert nodes[0].text == "Check this "
        assert nodes[1].text == "code"
        assert nodes[1].text_type == TextType.CODE
        assert nodes[2].text == " and "
        assert nodes[3].text == "this link"
        assert nodes[3].text_type == TextType.LINK
        assert nodes[3].url == "https://example.com"
    
    
if __name__ == "__main__":
    unittest.main()


   