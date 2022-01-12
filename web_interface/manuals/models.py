from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Note(models.Model):
    author = models.CharField(max_length=200)
    text = models.CharField(max_length=200)

########################

class Statement(models.Model):
    
    class StatementType(models.TextChoices):
        ANY = 'Any', 'Any'
        STATEMENT = 'Statement', 'Statement'
        ADVICE = 'Advice', 'Advice'
        OPINION = 'Opinion', 'Opinion'
        DEFINITION = 'Definition', 'Definition'
        
    type = models.CharField(max_length=20,
                            choices=StatementType.choices,
                            default=StatementType.ANY)
    subject = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)

########################

class Name(models.Model):
    value = models.CharField(max_length=100)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['value'], name='unique value')
        ]
        
class Ontology(MPTTModel):
    names = models.ManyToManyField(Name)
    description = models.CharField(max_length=1000)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')

########################

class Annotation(models.Model):
    manual = models.CharField(max_length=20)
    section = models.CharField(max_length=20)
    paragraph = models.CharField(max_length=20)
    sentence = models.CharField(max_length=20)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        ordering = ['section', 'paragraph', 'sentence']

########################

class SectionManager(models.Manager):
    def get_by_natural_key(self, index):
        return self.get(index=index)
    
class Section(models.Model):
    title = models.CharField(max_length=2000)
    manual = models.CharField(max_length=200, default='m')
    section = models.CharField(max_length=200, default='x')
    level = models.PositiveIntegerField()
    objects = SectionManager()
    
    def natural_key(self):
        return (self.manual, self.section)
    
    class Meta:
        #indexes = [ models.Index(fields=['index']) ]
        unique_together = [['manual', 'section']]

class ParagraphManager(models.Manager):
    def get_by_natural_key(self, section, index):
        return self.get(section=section, index=index)
    
class Paragraph(models.Model):
    manual = models.CharField(max_length=200, default='m')
    section = models.CharField(max_length=200, default='x')
    paragraph = models.CharField(max_length=200, default='y')
    objects = ParagraphManager()
    
    def natural_key(self):
        return (self.manual, self.section, self.paragraph)
    
    class Meta:
        #indexes = [ models.Index(fields=['index']) ]
        unique_together = [['manual', 'section', 'paragraph']]
        #ordering = ('tree_id', 'lft')
        #order_insertion_by = 'title'
        
class SentenceManager(models.Manager):
    def get_by_natural_key(self, section, paragraph, index):
        return self.get(section=section, paragraph=paragraph, index=index)
    
class Sentence(models.Model):
    text = models.CharField(max_length=2000)
    manual = models.CharField(max_length=200, default='m')
    section = models.CharField(max_length=200, default='x')
    paragraph = models.CharField(max_length=200, default='y')
    index = models.CharField(max_length=200, default='z')
    objects = ParagraphManager()
    
    def natural_key(self):
        return (self.manual, self.section, self.paragraph, self.index)
    
    class Meta:
        #indexes = [ models.Index(fields=['index']) ]
        unique_together = [['manual', 'section', 'paragraph', 'index']]

        
class TextNode(MPTTModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')
    

        
class ManualManager(models.Manager):
    def get_by_natural_key(self, label):
        return self.get(label=label)
    
class Manual(models.Model):
    title = models.CharField(max_length=200, null=False)
    authors = models.CharField(max_length=100, null=True)
    year = models.IntegerField(null=True)
    label = models.CharField(max_length=100, default='?')
    text = models.ForeignKey(TextNode, on_delete=models.CASCADE)
    class Meta:
        #indexes = [ models.Index(fields=['index']) ]
        unique_together = ['label']
