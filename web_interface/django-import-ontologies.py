from manuals.models import *
import argparse
import json
import re

def create_name(name):
    n, created = Name.objects.get_or_create(value=name)
    if created:
        print(f"created {name}")
    else:
        print(f"skipped duplicate {name}")
    n.save()
    return n

def add_name(ontology, name):
    n = create_name(name)
    ontology.names.add(n)
    
def add_names(ontology, names):
    if type(names) is str:
        add_name(ontology, names)
    else:
        for name in names:
            add_name(ontology, name)


def create_ontology(names, description, parent):
    o = Ontology(description=description, parent=parent)
    o.save()
    add_names(o, names)
    o.save()
    return o

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    ontologies = None
    with open(args.file) as f:
        ontologies = json.load(f)
        f.close()

    for ontology in ontologies:
        description = ontology.get('description', "")
        names = ontology['name']
        o = create_ontology(names, description, None)

        for e in ontology['children']:
            description = e.get('description', "")
            names = e['name']
            create_ontology(names, description, o)
        
        a = Annotation(manual=ontology['index'][0],
                       section=ontology['index'][1],
                       paragraph=ontology['index'][2],
                       sentence=ontology['index'][3],
                       content_object=o)
        a.save()


