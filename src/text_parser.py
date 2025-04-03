import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_list.append(node)
            continue
        no_of_splits = node.text.split(delimiter)
        if len(no_of_splits) % 2 == 0:
            raise Exception("invalid Markdown syntax")
        
        for i in range(len(no_of_splits)):
            if i % 2 == 0:
                if no_of_splits[i]:
                    new_list.append(TextNode(no_of_splits[i], TextType.TEXT))
            else:
                new_list.append(TextNode(no_of_splits[i], text_type))
    return new_list

def split_nodes_image(old_nodes):
    text_type = TextType.IMAGE
    split_format = "!"
    func = extract_markdown_images
    return split_nodes_images_or_link(old_nodes, text_type, func, split_format)
    
def split_nodes_link(old_nodes):
    text_type = TextType.LINK
    func = extract_markdown_links
    return split_nodes_images_or_link(old_nodes, text_type, func)

def split_nodes_images_or_link(old_nodes, text_type, func, splitter_format = ""):
    new_list = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_list.append(node)
            continue
        matches = func(node.text)
        if len(matches) == 0:
            new_list.append(node)
            continue
        splits = []
        text = node.text
        for match in matches:
            if not match[1]:
                continue
            splitter = f"{splitter_format}[{match[0]}]({match[1]})"
            splits = text.split(splitter, 1)
            new_list.append(TextNode(splits[0], TextType.TEXT))
            new_list.append(TextNode(match[0], text_type, match[1]))
            if splits[1]:
                text = splits[1]
            else:
                text = ""
        if text.strip():
            new_list.append(TextNode(text, TextType.TEXT))
    return new_list

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes