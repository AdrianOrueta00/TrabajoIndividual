from neo4j import GraphDatabase
import time

class HelloWorldExample:

    def __init__(self, uri):
        self.driver = GraphDatabase.driver(uri)

    def close(self):
        self.driver.close()

    def insert_data(self):

        studentId = "adrian"
        studentName = "Adrian"

        teacherId = "unai"
        teacherName = "Unai"

        with self.driver.session() as session:
            session.write_transaction(self._delete_all)
            greeting = session.write_transaction(self._insert_entity, studentId, "Student", studentName)
            print(greeting)
            greeting = session.write_transaction(self._insert_entity, teacherId, "Teacher", teacherName)
            print(greeting)
            greeting = session.write_transaction(self._create_relation, teacherName, "Teacher", studentName, "Student", "TEACHES_TO")
            print(greeting)

    @staticmethod
    def _delete_all(tx):
        tx.run("MATCH (n) DETACH DELETE n")

    @staticmethod
    def _insert_entity(tx, objectId, entity, name):
        result = tx.run(
            "CREATE (%s:%s {name: '%s'}) RETURN 'New %s was inserted in node ' + id(%s) + ', with name %s and id %s'" % (
            objectId, entity, name, entity, objectId, name, objectId))
        return result.single()[0]

    @staticmethod
    def _create_relation(tx, attribute1, entity1, attribute2, entity2, relation):
        result = tx.run(
            "MATCH (a:%s {name: '%s'}) MATCH (b:%s {name: '%s'}) CREATE (a)-[rel:%s]->(b) RETURN 'New relation ´%s´ was created between object ´%s´ of type ´%s´ and object ´%s´ of type ´%s´'" % (
            entity1, attribute1, entity2, attribute2, relation, relation, attribute1, entity1, attribute2, entity2))
        return result.single()[0]


if __name__ == "__main__":

    for i in range(8):
        if i == 1:
            print("Waiting until Neo4J starts...")
        time.sleep(5)
    greeter = HelloWorldExample("bolt://neo4j:7687")
    greeter.insert_data()
    greeter.close()
