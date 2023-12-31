from django.db import models

# Create your models here.

class Mapping(models.Model):
    """
    Represents a single mapping from a fuseki query to a
    format for how excel should be specified.
    """
    title = models.CharField(max_length=255, db_index=True, unique=True)
    graph_name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    fuseki_relations = models.JSONField() # Each relation is a list of 3 elements: [attribute1, relation, attribute2]; this is a JSON list of lists
    excel_format = models.JSONField()
    last_updated = models.DateTimeField(auto_now=True)

class GeneratedExcelFile(models.Model):
    """
    Represents a single generated excel file.
    """
    excel_file = models.FileField(upload_to='data/excel_files/')
    last_updated = models.DateTimeField(auto_now=True)
