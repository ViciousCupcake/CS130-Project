"""
This module contains helper functions for parsing excel sheets to rdf
"""


import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef

def parse_excel(file, name):
    """
    Convert an excel sheet to rdf
    
    :param file: excel file to be converted
    :param name: name of the excel file
    :return: a tuple of prefixes and triples
    """

    df = pd.read_excel(file)
    
    # Create an RDF graph
    g = Graph()

    # Define a namespace
    ns = Namespace("http://" + name.split('.')[0] + ".org/")
    g.bind('ex', ns)

    # Convert DataFrame rows to RDF triples
    for index, row in df.iterrows():
        subject = URIRef(ns + str(index))
        for column, value in row.items():
            predicate = URIRef(ns + column)
            obj = Literal(value)
            g.add((subject, predicate, obj))

    # Serialize the graph to RDF format
    rdf_data = g.serialize(format='turtle')
    rdf_data = rdf_data.replace("@prefix", "PREFIX")

    # seperate the prefix with triples
    prefixes, triples = rdf_data.split('\n\n', 1)
    prefixes = '\n'.join(line.rstrip(' .') for line in prefixes.splitlines())
    return (prefixes, triples)
