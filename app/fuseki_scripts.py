from SPARQLWrapper import SPARQLWrapper, JSON, POST
from app.models import Fuski_Relation, Fuski_Relations_Group
import pandas as pd
from os import environ

fuseki_username = environ.get('FUSEKI_ADMIN_USER')
fuseki_password = environ.get('FUSEKI_ADMIN_PASSWORD')

"""
List of relations:
attribute - relation - attribute
attribute - relation - attribute
attribute - relation - attribute
...
attribute - relation - attribute
"""

def create_sparql_graph(graph_name: str):
    """
    Creates a sparql graph which adheres to the relations in the schema
    """
    sparql = SPARQLWrapper("http://host.docker.internal:3030/mydataset/update")
    sparql.setCredentials(fuseki_username, fuseki_password)
    sparql.setMethod(POST)
    
    sparql.setQuery("""
        PREFIX : <http://example/>
        CREATE GRAPH :""" + graph_name + """
    """)
    _ = sparql.query()
    
def remove_sparql_graph(graph_name: str):
    """
    Removes a sparql graph
    """
    sparql = SPARQLWrapper("http://host.docker.internal:3030/mydataset/update")
    sparql.setCredentials(fuseki_username, fuseki_password)
    sparql.setMethod(POST)
    
    sparql.setQuery("""
        PREFIX : <http://example/>
        DROP GRAPH :""" + graph_name + """
    """)
    _ = sparql.query()
    
def insert_pandas_dataframe_into_sparql_graph(graph_name: str, relation_table_name: str, dataframe: pd.DataFrame):
    """
    Inserts a pandas dataframe into a sparql graph, using the relations stored in the django model as a schema.
    The idea is that the user will have selected the schema in which they would like to store the rows of the dataframe
    by choosing the django model which contains the schema.
    
    Preconditions:
    - graph_name is a string with no spaces
    - relation_table_name is a string with no spaces
    - dataframe is a pandas dataframe with the same columns as the relations in the django model
    
    Postconditions:
    - The dataframe is inserted into the sparql graph
    """
    sparql = SPARQLWrapper("http://host.docker.internal:3030/mydataset/update")
    sparql.setCredentials(fuseki_username, fuseki_password)
    sparql.setMethod(POST)
    
    # Create the graph if it doesn't exist
    create_sparql_graph(graph_name)
    
    # Get the relations from the django model
    relations_group = Fuski_Relations_Group.objects.get(name=relation_table_name)
    relations = relations_group.relations.all()
    
    # Insert the dataframe into the graph
    for index, row in dataframe.iterrows():
        row = row.to_dict()
        query = """
            PREFIX : <http://example/>
            INSERT DATA { GRAPH :""" + graph_name + """ { """
            
        for relation in relations:
            query += ":" + row[relation.attribute1] + " :" + relation.name + " :" + row[relation.attribute2] + " . "
        query += "} }"
        
        sparql.setQuery(query)
        _ = sparql.query()

def create_list_of_relations(list_of_relations: list, relation_table_name: str):
    """
    Creates a django Fuseki_Relations_Group model with the given list of relations and table name
    
    Preconditions:
    - list_of_relations is a list of lists of length 3
    - relation_table_name is a string
    
    Postconditions:
    - A django Fuseki_Relations_Group model is created with the given list of relations and table name
    """
    relations_group = Fuski_Relations_Group(
        name=relation_table_name, description="Created by script")
    relations_group.save()

    for relation in list_of_relations:
        attribute1 = relation[0]
        attribute2 = relation[2]
        relation = relation[1]

        new_relation = Fuski_Relation(
            name=relation, description="Created by script", attribute1=attribute1, attribute2=attribute2)
        new_relation.save()
        relations_group.relations.add(new_relation)

    relations_group.save()


def remove_list_of_relations(relation_table_name: str):
    """
    Removes a django Fuseki_Relations_Group model with the given table name
    
    Preconditions:
    - relation_table_name is a string
    
    Postconditions:
    - A django Fuseki_Relations_Group model is removed with the given table name
    """
    relations_group = Fuski_Relations_Group.objects.get(name=relation_table_name)
    relations_group.delete()