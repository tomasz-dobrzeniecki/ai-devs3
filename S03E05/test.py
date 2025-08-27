from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j","haslo"))
with driver.session() as s:
    print(s.run("RETURN 1").single()[0])
driver.close()