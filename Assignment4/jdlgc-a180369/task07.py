# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10bZVZLj1O3vIV6-4mylFF0U9xHmKuD2I

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

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

ns = Namespace("http://somewhere#")
from rdflib.plugins.sparql import prepareQuery

print("RDFLib:")
for s,p,o in g.triples((None, RDFS.subClassOf, ns.LivingThing)):
  print(s)

print("\nSPARQL:")
q1 = prepareQuery('''
  SELECT
    ?Subject
  WHERE {
    ?Subject rdfs:subClassOf ns:LivingThing
  }
  ''',
  initNs = {"rdfs": RDFS, "ns": ns}
)
# Visualize the results
for r in g.query(q1):
  print(r.Subject)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

print("RDFLib:")
for s,p,o in g.triples((None, RDF.type, ns.Person)):
  print(s)
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for ss,pp,oo in g.triples((None, RDF.type, s)):
    print(ss)

print("\nSPARQL:")
q2 = prepareQuery('''
  SELECT
    ?Subject
  WHERE {
    {
      ?Subject rdf:type ns:Person
    }
    UNION
    {
     ?Person rdfs:subClassOf ns:Person.
     ?Subject rdf:type ?Person
    }
  }
  ''',
  initNs = {"rdf": RDF, "ns": ns}
)
# Visualize the results
for r in g.query(q2):
  print(r.Subject)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

print("Using rdflib:")
for s,p,o in g.triples((None, RDF.type, ns.Person)):
  print(f"Indiviudal: {s}")
  for ss,pp,oo in g.triples((s, None, None)):
    print(f"Property: {pp}; Object: {oo}")
  print("\n")

for s,p,o in g.triples((None, RDF.type, ns.Animal)):
  print(f"Indiviudal: {s}")
  for ss,pp,oo in g.triples((s, None, None)):
    print(f"Property: {pp}; Object: {oo}")
  print("\n")

print("\nSPARQL:")
q3 = prepareQuery('''
  SELECT
    ?Subject ?Pred ?Obj
  WHERE {
    {
      ?Subject rdf:type ns:Person.
    }
    UNION
    {
     ?Subject rdf:type ns:Animal.
    }
    ?Subject ?Pred ?Obj
  }
  ''',
  initNs = {"rdf": RDF, "ns": ns}
)

# Visualize the results
results = {}
for r in g.query(q3):
  if r.Subject not in results:
    results[r.Subject] = []
  results[r.Subject].append((r.Pred, r.Obj))

for subject, properties in results.items():
  print(f"Indiviudal: {s}")
  for prop in properties:
    print(f"Property: {prop[0]}; Object: {prop[1]}")
  print("\n")

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

foaf = Namespace("http://xmlns.com/foaf/0.1/")

print("RDFLib:")
for s,p,o in g.triples((None, RDF.type, ns.Person)):
  print(s)
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for ss,pp,oo in g.triples((None, RDF.type, s)):
    for sss,ppp,ooo in g.triples((s, foaf.knows, ns.RockySmith)):
      print(sss)

print("\nSPARQL:")
q4 = prepareQuery('''
  SELECT
    ?Subject
  WHERE {
    {
      ?Subject rdf:type ns:Person
    }
    UNION
    {
     ?Person rdfs:subClassOf ns:Person.
     ?Subject rdf:type ?Person
    }
    ?Subject foaf:knows ns:RockySmith.
  }
  ''',
  initNs = {"rdf": RDF, "ns": ns, "foaf": foaf}
)
# Visualize the results
for r in g.query(q4):
  print(r.Subject)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

print("RDFLib:")
printed = set()
for s,p,o in g.triples((None, foaf.knows, None)):
  for ss,pp,oo in g.triples((s, foaf.knows, None)):
    if (oo != o) and (s not in printed):
      print(s)
      printed.add(s)

print("\nSPARQL:")
q5 = prepareQuery('''
  SELECT distinct
    ?Subject
  WHERE {
    ?Subject foaf:knows ?Obj1 .
    ?Subject foaf:knows ?Obj2 .
    FILTER (?Obj1 != ?Obj2).
  }
  ''',
  initNs = {"foaf": foaf}
)
# Visualize the results
for r in g.query(q5):
  print(r.Subject)