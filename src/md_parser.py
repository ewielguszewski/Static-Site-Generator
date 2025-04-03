from enum import Enum
import re
from htmlnode import HTMLNode, ParentNode
from text_parser import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(md_block):
    lines = md_block.split("\n")
    if re.match(r"^#{1,6} ", lines[0]):
        return BlockType.HEADING
    if lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    isQuote = True
    isUnorderedList = True
    isOrderedList = True
    for i in range(len(lines)):
        if not lines[i]:
            continue
        if not lines[i].startswith(">"):
            isQuote = False
        if not lines[i].startswith("- "):
            isUnorderedList = False
        if not lines[i].startswith(f"{i + 1}. "):
            isOrderedList = False
    if isQuote:
        return BlockType.QUOTE
    if isUnorderedList:
        return BlockType.UNORDERED_LIST
    if isOrderedList:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def block_type_to_html_tag(block_type, block = None):
    if block_type == BlockType.PARAGRAPH:
        return "p"
    elif block_type == BlockType.HEADING:
        counter = 0
        for char in block:
            if char == "#":
                counter += 1
            else:
                break
        return f"h{counter}"  
    elif block_type == BlockType.CODE:
        
        return "code"
    elif block_type == BlockType.QUOTE:
        return "blockquote"
    elif block_type == BlockType.UNORDERED_LIST:
        return "ul"
    elif block_type == BlockType.ORDERED_LIST:
        return "ol"
    else:
        raise ValueError(f"Invalid block type: {block_type}")

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    
    result = []
    for block in blocks:
        cleaned_block = block.strip()
        if cleaned_block:
            lines = cleaned_block.split("\n")
            cleaned_lines = [line for line in lines]
            cleaned_block = '\n'.join(cleaned_lines)
            result.append(cleaned_block)
    return result

from htmlnode import LeafNode

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.CODE:
                code_content = block.strip().split("\n")
                code_content = code_content[1:-1]
                code_content = "\n".join(code_content)
                text_node = TextNode(code_content, TextType.CODE)
                code_node = text_node_to_html_node(text_node)
                block_node = ParentNode("pre", [code_node])
                
            case BlockType.HEADING:
                html_tag = block_type_to_html_tag(block_type, block)
                heading_content = block.lstrip("#").strip()
                children = text_to_children(heading_content)
                block_node = ParentNode(html_tag, children)
                
            case BlockType.QUOTE:
                html_tag = block_type_to_html_tag(block_type)
                lines = block.split("\n")
                children = []
                for line in lines:
                    line = line.lstrip(">").strip()
                    node = LeafNode(None, line)
                    children.append(node)
                block_node = ParentNode(html_tag, children)
                
            case BlockType.UNORDERED_LIST:
                html_tag = block_type_to_html_tag(block_type)
                lines = block.split("\n")
                children = []
                for line in lines:
                    line = line.lstrip("- ").strip()
                    line_children = text_to_children(line)
                    line_node = ParentNode("li", line_children)
                    children.append(line_node)
                block_node = ParentNode(html_tag, children)
                
            case BlockType.ORDERED_LIST:
                html_tag = block_type_to_html_tag(block_type)
                lines = block.split("\n")
                children = []
                for line in lines:
                    line_children = text_to_children(line[3:])
                    line_node = ParentNode("li", line_children)
                    children.append(line_node)
                block_node = ParentNode(html_tag, children)
                
            case _:
                html_tag = block_type_to_html_tag(block_type, block)
                children = text_to_children(block, block_type)
                block_node = ParentNode(html_tag, children)
                
        html_children.append(block_node)        
    return ParentNode("div", html_children)

def text_to_children(text, block_type = None):
    if block_type == BlockType.PARAGRAPH:
        text = text.replace("\n", " ")
    nodes = text_to_textnodes(text)
    leafs = []
    for node in nodes:
        leaf = text_node_to_html_node(node)
        leafs.append(leaf)
    return leafs
