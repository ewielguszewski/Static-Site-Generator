import unittest
from md_parser import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_empty_input(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_markdown_to_blocks_single_block(self):
        md = "This is a single block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single block"])
    
    def test_markdown_to_blocks_multiple_blank_lines(self):
        md = "First block\n\n\n\nSecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])
        
    def test_markdown_to_blocks_only_whitespace(self):
        md = "First block\n\n    \n\nSecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])
        
class TestBlockToBlockType(unittest.TestCase):
    
    def test_paragraph(self):
        block = "This is a simple paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)
        
        self.assertEqual(block_to_block_type("#Not a heading"), BlockType.PARAGRAPH)
    
    def test_code(self):
        block = "```\ncode line 1\ncode line 2\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        
        block = "```python\ndef hello():\n    print('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        
        block = "```\ncode line 1\ncode line 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
    
        block = "> Line 1 of quote\n> Line 2 of quote\n> Line 3 of quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
        block = "> Line 1 of quote\nLine 2 not quoted\n> Line 3 of quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
    
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
        block = "- Item 1\nItem 2 not properly formatted\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Item 1"), BlockType.ORDERED_LIST)
    
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
        block = "1. Item 1\n3. Item 2\n4. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )