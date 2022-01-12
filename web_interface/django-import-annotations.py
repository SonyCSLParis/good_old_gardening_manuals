from manuals.models import *
import argparse
import json
import re

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    annotations = None
    with open(args.file) as f:
        annotations = json.load(f)
        f.close()

    for annotation in annotations:
        s = Statement(type=annotation['type'],
                      subject=annotation['subject'],
                      text=annotation['text'])
        s.save()

        a = Annotation(manual=annotation['index'][0],
                       section=annotation['index'][1],
                       paragraph=annotation['index'][2],
                       sentence=annotation['index'][3],
                       content_object=s)
        a.save()


