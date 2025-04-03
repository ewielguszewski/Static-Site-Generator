from textnode import *
from md_parser import markdown_to_blocks
from text_parser import split_nodes_delimiter
import os, shutil

def main():
    from_path = "static/"
    to_path = "public/"
    
    from_path_exists = os.path.exists(from_path)
    to_path_exists = os.path.exists(to_path)
    
    if not to_path_exists:
        os.mkdir(to_path, mode = 0o755)
    
    public_list = os.listdir(to_path)
    
    if len(public_list) != 0:
        print(f"Directory '{to_path}' not empty: {public_list}\nDeleting files")
        shutil.rmtree(to_path)
        os.mkdir(to_path, mode = 0o755)
        public_list = os.listdir(to_path)
        print(f"Content after delete: {public_list}")
    
    recursiveCopy(from_path, to_path)
    
    generate_pages_recursive("content/", "template.html", "public/")
    
            

def recursiveCopy(src, dst):
    list_of_elements = os.listdir(src)
    print(f"LIST OF ELEMENTS : {list_of_elements}")
    for element in list_of_elements:
        pathDST = os.path.join(dst, element)
        pathSRC = os.path.join(src, element)
        if os.path.islink(pathSRC):
            print(f"Skipping symbolic link: {pathSRC}")
            continue
        if os.path.isfile(pathSRC):
            print(f"COPYING {pathSRC} to {pathDST}")
            try:
                shutil.copy(pathSRC, pathDST)
            except Exception as e:
                with open("error_log.txt", "a") as log_file:
                    log_file.write(f"Failed to copy {pathSRC} to {pathDST}: {e}\n")
                print(f"Failed to copy {pathSRC} to {pathDST}: {e}")
        else:
            print(f"MAKING DIR {pathDST}")
            os.mkdir(pathDST, mode = 0o755)
            print(f"RECURSIVE COPY {pathSRC}, {pathDST}")
            recursiveCopy(pathSRC, pathDST)
            
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("header not found")

from md_parser import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    content_markdown = ""
    content_template = ""
    with open(from_path, "r") as content:
        content_markdown = content.read()
    with open(template_path, "r") as content:
        content_template = content.read()
    HTMLString = markdown_to_html_node(content_markdown)
    title = extract_title(content_markdown)
    html = HTMLString.to_html()
    result = content_template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    with open(dest_path, "w") as content:
        content.write(result)    
    return

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    entries = os.listdir(dir_path_content)
    if len(entries) == 0:
        return
    for entry in entries:
        pathDIR = os.path.join(dir_path_content, entry)
        pathDEST = os.path.join(dest_dir_path, entry)
        if os.path.islink(pathDIR):
            continue
        if os.path.isfile(pathDIR) and pathDIR.endswith(".md"):
            base, _ = os.path.splitext(entry)
            dest = os.path.join(dest_dir_path, f"{base}.html")
            generate_page(pathDIR, template_path, dest)
        elif os.path.isdir(pathDIR):
            if not os.path.exists(pathDEST):
                os.mkdir(pathDEST, 0o755)
            print(f"RECURSIVE GENERATE FOR:\nPATH DIR: {pathDIR}\nTEMPLATE_PATH: {template_path}\nPATH DEST: {pathDEST}")
            generate_pages_recursive(pathDIR, template_path, pathDEST)
        else:
            continue
            
    


main()