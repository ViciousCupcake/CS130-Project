from SPARQLWrapper import SPARQLWrapper, JSON, POST, GET
from app.models import Mapping
import pandas as pd
from os import environ
from cs130_efi.settings import FUSEKI_PREFIX

fuseki_username = environ.get('FUSEKI_ADMIN_USER')
fuseki_password = environ.get('FUSEKI_ADMIN_PASSWORD')

API_BASE_URL = "http://fuseki:3030/mydataset"

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
    sparql = SPARQLWrapper(f"{API_BASE_URL}/update")
    sparql.setCredentials(fuseki_username, fuseki_password)
    sparql.setMethod(POST)
    
    sparql.setQuery("""
        PREFIX : """ + FUSEKI_PREFIX + """
        CREATE GRAPH :""" + graph_name + """
    """)
    _ = sparql.query()
    
def remove_sparql_graph(graph_name: str):
    """
    Removes a sparql graph
    """
    sparql = SPARQLWrapper(f"{API_BASE_URL}/update")
    sparql.setCredentials(fuseki_username, fuseki_password)
    sparql.setMethod(POST)
    
    sparql.setQuery("""
        PREFIX : """ + FUSEKI_PREFIX + """
        DROP GRAPH :""" + graph_name + """
    """)
    _ = sparql.query()
    
def insert_pandas_dataframe_into_sparql_graph(graph_name: str, relation_mapping_name: str, dataframe: pd.DataFrame):
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
    sparql = SPARQLWrapper(f"{API_BASE_URL}/update")
    sparql.setCredentials(fuseki_username, fuseki_password)
    sparql.setMethod(POST)
    
    # Create the graph if it doesn't exist
    create_sparql_graph(graph_name)
    
    # Get the relations from the django model
    relations_group = Mapping.objects.get(title=relation_mapping_name, graph_name=graph_name)
    relations = relations_group.fuseki_relations
    
    # Insert the dataframe into the graph
    for index, row in dataframe.iterrows():
        row = row.to_dict()
        query = """
            PREFIX : """ + FUSEKI_PREFIX + """
            INSERT DATA { GRAPH :""" + graph_name + """ { """

        for relation in relations:
            query += ":" + str(row[relation[0]]) + " :" + relation[1] + " :" + str(row[relation[2]])+ " . "
        query += "} }"
        
        sparql.setQuery(query)
        _ = sparql.query()

def fuseki_relations_to_sparql_response(map_relations, graph_name: str):
    """
    Converts fuseki_relations field of mapping model into a fuseki sparql query to retrieve
    data from the knowledge base based on that data
    
    Preconditions:
    - Relations is a JSON object

    Postcondition:
    - Return the response returned form the query
    """

    sparql = SPARQLWrapper(f"{API_BASE_URL}/query")
    sparql.setCredentials(fuseki_username, fuseki_password)
    sparql.setMethod(POST)

    # construct a list of column names
    query_fields = set()
    for relation in map_relations: # [["Test_Attribute_1", "Test_Relation", "Test_Attribute_2"]]
        query_fields.add(relation[0])
        query_fields.add(relation[2])
    query_fields = "?"+ (" ?").join(query_fields)
    
    # add each relation to query
    query = """
            PREFIX : """ + FUSEKI_PREFIX + """
            SELECT """ + query_fields +  """ 
            WHERE { GRAPH :""" + graph_name + """ {
                  """
    
    for relation in map_relations:
        query += " ?" + relation[0] + " :" + relation[1] + " ?" + relation[2] + " ."
    query += "} }"

    # execute query
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    result = sparql.query().convert()
    return result

def fuseki_response_to_DataFrame(response):
    """
    Converts fuseki response to a pandas DataFrame.

    Preconditions:
    - response is a response from fuseki
    Postcondition:
    - Return the converted DataFrame
    """
    
    response = response["results"]["bindings"]
    result = {}

    # parse response row by row into dictionary
    for data_row in response:
        for attribute in data_row:
            value = data_row[attribute]["value"][len(FUSEKI_PREFIX)-2:]
            if attribute in result:
                result[attribute].append(value)
            else:
                result[attribute] = [value]

    headers = result.keys()
    df = pd.DataFrame(result)

    return (headers, df)
