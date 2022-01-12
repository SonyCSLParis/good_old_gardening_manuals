import xml.etree.ElementTree as ET
import re
from manuals.models import *
import argparse
    
if __name__ == "__main__":
    
    s0 = Statement(type="Statement",
                   text="Les laitues montent vite.")
    s0.save()
    a0 = Annotation(manual="gpjf",
                    section="1.1",
                    paragraph="2",
                    sentence="1",
                    content_object=s0)
    a0.save()

    s1 = Statement(type="Statement",
                   text="Les laitues prennent difficilement dans les terrains trop légers.")
    s1.save()
    a1 = Annotation(manual="gpjf",
                    section="1.1",
                    paragraph="2",
                    sentence="1",
                    content_object=s1)
    a1.save()

    s2 = Statement(type="Statement",
                    text="Les laitues prennent difficilement dans les terrains trop chauds.")
    s2.save()
    a2 = Annotation(manual="gpjf",
                    section="1.1",
                    paragraph="2",
                    sentence="1",
                    content_object=s2)
    a2.save()

    s3 = Statement(type="Statement",
                    text="Les laitues prennent difficilement dans les terrains trop secs.")
    s3.save()
    a3 = Annotation(manual="gpjf",
                    section="1.1",
                    paragraph="2",
                    sentence="1",
                    content_object=s3)
    a3.save()

    s4 = Statement(type="Statement",
                    text="Les laitues poussent avec une extrême lenteur dans les terrains forts et froids.")
    s4.save()
    a4 = Annotation(manual="gpjf",
                    section="1.1",
                    paragraph="2",
                    sentence="1",
                    content_object=s4)
    a4.save()


    s4 = Statement(type="Statement",
                    text="Les laitues poussent avec une extrême lenteur dans les terrains forts et froids.")
    s4.save()
    a4 = Annotation(manual="gpjf",
                    section="1.1",
                    paragraph="2",
                    sentence="1",
                    content_object=s4)
    a4.save()
    
