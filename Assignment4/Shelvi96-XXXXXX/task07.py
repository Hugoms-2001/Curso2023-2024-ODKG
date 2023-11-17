# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yPniC8cCIRK0ofpUQK_h0bcNOa4CroCF

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

# Helpers:

from rdflib.plugins.sparql import prepareQuery

ns = Namespace("http://somewhere#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")


"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

q1 = prepareQuery('''
    SELECT ?SubClass WHERE { 
        ?SubClass rdfs:subClassOf* ns:LivingThing.
    }
    ''',
    initNs = {"rdfs": RDFS, "ns": ns}
)

for r in g.query(q1):
    print(r)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

q2 = prepareQuery('''
    SELECT ?individual WHERE { 
        ?individual a ?type .
        ?type rdfs:subClassOf* ns:Person
    }
    ''',
    initNs = {"rdfs": RDFS, "ns": ns}
)
for r in g.query(q2):
    print(r)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

q3 = prepareQuery('''
    SELECT ?individual ?property ?value
    WHERE {
        {
            ?individual rdf:type ns:Person .
        } UNION {
            ?individual rdf:type ns:Animal .
        }
        ?individual ?property ?value .
    }
    ''',
    initNs = {"rdfs": RDFS, "ns": ns}
)

for ns in g.query(q3):
    print(ns)

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

q4 = prepareQuery('''
    SELECT ?name
    WHERE {
        ?individual rdf:type ns:Person.
        ?individual foaf:knows ns:RockySmith.
        ?individual foaf:name ?name.
    }  
    ''',
    initNs = { "foaf": FOAF, "ns": ns, "rdf": RDF}
)

for ns in g.query(q4):
    print(ns)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

q5 = prepareQuery('''
    SELECT ?individual
    WHERE {
        ?individual foaf:knows ?individual1 .
        ?individual foaf:knows ?individual2 .
        FILTER(?individual1 != ?individual2)
    }
    GROUP BY ?individual
    HAVING (
        COUNT(?individual) >= 2
    )
    ''',
    initNs = { "foaf": FOAF, "ns": ns, "rdf": RDF}
)

for ns in g.query(q5):
    print(ns)

