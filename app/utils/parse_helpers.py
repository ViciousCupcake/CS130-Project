# Helpers that include all necessary parsers
import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef

def parse_excel(file, name):
    """Convert an excel sheet to rdf"""
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
    return rdf_data