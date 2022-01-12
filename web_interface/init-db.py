from manuals.models import *

m = Manual(title="GPJF", authors='TODO', year=1800, label='gpjf')
m.save()


# section 1
s = Section(title="Salade", manual=m.label, section='1')
s.save()

s_node = TextNode(content_object=s, index=0)
s_node.save()


# p1

p = Paragraph(manual=m.label, section=s.section, paragraph="1")
p.save()

p_node = TextNode(content_object=p, index=0, parent=s_node)
p_node.save()

f = Sentence(text="Salades : Laitues de printemps, d'été, d'hiver, Laitues romaines, Chicorée, Scarole, Chicorée sauvage, Chicorée barbe-de-capucin, Mâche, Raiponce.", manual=m.label, section=s.section, paragraph=p.paragraph, index="1")
f.save()

f_node = TextNode(content_object=f, index=0, parent=p_node)
f_node.save()

# p2

p = Paragraph(manual=m.label, section=s.section, paragraph="2")
p.save()

p_node = TextNode(content_object=p, index=0, parent=s_node)
p_node.save()

#
f = Sentence(text="Laitues (Composées). -- D'Asie.", manual=m.label, section=s.section, paragraph=p.paragraph, index="1")
f.save()

f_node = TextNode(content_object=f, index=0, parent=p_node)
f_node.save()

#
f = Sentence(text="Toutes les nombreuses variétés de Laitues produites par la culture peuvent être rangées dans deux divisions générales : 1° Laitues pommées, 2° Laitues romaines ou chicons.", manual=m.label, section=s.section, paragraph=p.paragraph, index="2")
f.save()

f_node = TextNode(content_object=f, index=0, parent=p_node)
f_node.save()


#
f = Sentence(text="Parmi les Laitues de la première division on nomme les plus précoces de toutes, Laitues de printemps; les plus volumineuses et les moins sujettes à monter, Laitues d'été; enfin celles qu'on traite comme plantes bisannuelles à partir de l'automne pour être mangées au printemps de l'année suivante, s'appellent Laitues d'hiver; on comprend également dans cetle division les Laztues à couper non pommées.", manual=m.label, section=s.section, paragraph=p.paragraph, index="3")
f.save()

f_node = TextNode(content_object=f, index=0, parent=p_node)
f_node.save()

