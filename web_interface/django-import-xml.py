import xml.etree.ElementTree as ET
import re
from manuals.models import *
import argparse


class ManualConverter():
    path = ""
    title = "?"
    authors = "?"
    year = 0
    body = None
    label = "?"
    level = 0
    section = [ 0 ]
    paragraph_index = 0
    sentence_index = 0
    section_stack = []

    def __init__(self, path):
        self.path = path
        
    def convert(self):
        node = self.load(self.path)
        print(f"Importing '{self.title}', {self.authors} ({self.year})")
        
        m = Manual(title=self.title, authors=self.authors,
                   year=self.year, label=self.label, text=node)
        m.save()
        
        
    def load(self, path):
        tree = ET.parse(args.file)
        manual = tree.getroot()
        if not manual.tag == 'manual':
            raise ValueError("Not a manual")
        self.title = manual.find('title').text
        self.authors = manual.find('authors').text
        self.year = manual.find('year').text
        self.label = manual.find('label').text
        body = manual.find('body')

        section = Section(title=self.title, manual=self.label, section='root', level=0)
        section.save()

        node = self.create_node(section, None)
        
        self.enter_section(node)
        self.create_recursive(body)
        self.leave_section(node)

        return node

        
    def create_recursive(self, body):
        for element in body:
            self.create_element(element)
            
    def create_element(self, element):
        if element.tag == 'section':
            self.create_section(element)
        elif element.tag == 'p':
            self.create_paragraph(element)
        elif element.tag == 's':
            self.create_sentence(element)
        else:
            raise ValueError(f"Unknown element: {element.tag}")

    def get_current_section(self):
        if len(self.section_stack) > 0:
            return self.section_stack[-1]
        else:
            return None
        
    def create_section(self, element):
        self.increment_section()
        s = self.get_section_string()
        title = element.find('title').text
        section = Section(title=title, manual=self.label, section=s, level=self.level)
        section.save()

        node = self.create_node(section, self.get_current_section())
        
        print(f"Section {self.label}:{s}: {title}")
        print("-------")
        body = element.find('body')
        self.enter_section(node)
        self.create_recursive(body)
        self.leave_section(node)
        print("-------")

        return node

    def create_node(self, content, parent):
        node = TextNode(content_object=content, parent=parent)
        node.save()
        return node
    
    def increment_section(self):
        if len(self.section) < self.level:
            self.section.append(1)
            #self.section[self.level] = 1
        else:
            self.section[-1] = self.section[-1] + 1
        
    def enter_section(self, node):
        self.section_stack.append(node)
        self.reset_paragraph()
        self.level += 1
    
    def leave_section(self, node):
        self.section_stack.pop()
        self.level -= 1
        if len(self.section) > self.level:
            self.section.pop()

    def enter_paragraph(self, node):
        self.reset_sentence()
        self.current_paragraph = node
        
    def leave_paragraph(self, node):
        pass

    def reset_paragraph(self):
        self.paragraph_index = 0

    def increment_paragraph(self):
        self.paragraph_index += 1

    def create_paragraph(self, element):
        self.increment_paragraph()
        s = self.get_section_string()
        print(f"Paragraph({self.label}:{s}:{self.paragraph_index}):")
        
        p = Paragraph(manual=self.label, section=s, paragraph=self.paragraph_index)
        p.save()

        node = self.create_node(p, self.get_current_section())
        
        self.enter_paragraph(node)
        self.create_recursive(element)
        self.leave_paragraph(node)
        print("--")

        return node
        
    def reset_sentence(self):
        self.sentence_index = 0

    def increment_sentence(self):
        self.sentence_index += 1

    def get_section_string(self):
        string_list = [str(i) for i in self.section]
        return ".".join(string_list)
        
    def create_sentence(self, element):
        self.increment_sentence()
        s = self.get_section_string()
        text = self.cleanup_whitespaces(element.text)
        print(f"* Sentence({self.label}:{s}:{self.paragraph_index}:{self.sentence_index}):")
        print(f"  {text}")

        f = Sentence(text=text,
                     manual=self.label,
                     section=s,
                     paragraph=self.paragraph_index,
                     index=self.sentence_index)
        f.save()
        node = self.create_node(f, self.current_paragraph)
        return node
        
    def cleanup_whitespaces(self, text):
        text = re.sub('\r', ' ', text)
        text = re.sub('\n', ' ', text)
        text = re.sub('\t', ' ', text)
        text = re.sub(' +', ' ', text)
        return text

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    converter = ManualConverter(args.file)
    converter.convert()



