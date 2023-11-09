from django.db import models

# Create your models here.

class Fuski_Relation(models.Model):
    """
    Represents a single relationship between two attributes.
    """
    name = models.CharField(max_length=255, help_text="Name of the fuseki relationship.")
    description = models.TextField(blank=True, help_text="Description of the fuseki relationship.")
    
    attribute1 = models.CharField(max_length=255, help_text="First attribute in the relationship.")
    attribute2 = models.CharField(max_length=255, help_text="Second attribute in the relationship.")
    
    def __str__(self):
        return self.name
    
class Fuski_Relations_Group(models.Model):
    """
    Represents a list of relationships between attributes.
    """
    # Unique name
    name = models.CharField(max_length=255, db_index=True, unique=True, help_text="Name of the group of relationships.")
    description = models.TextField(blank=True, help_text="Description of the group of relationships.")
    relations = models.ManyToManyField('Fuski_Relation', help_text="Relationships between attributes.")
    
    def __str__(self):
        return self.name

class Mapping(models.Model):
    """
    Represents a single mapping from a fuseki query to a
    format for how excel should be specified.
    """
    title = models.CharField(max_length=255, db_index=True, unique=True)
    description = models.TextField(blank=True)
    fuseki_query = models.TextField()
    excel_format = models.JSONField()
    last_updated = models.DateTimeField(auto_now=True)
