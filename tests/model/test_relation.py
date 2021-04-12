from unittest import TestCase

from ornitho import Relation, RelationType


class TestRelation(TestCase):
    def test_str(self):
        relation = Relation(1, RelationType("same"))
        self.assertEqual(1, relation.with_id)
        self.assertEqual(RelationType("same"), relation.type)
        self.assertEqual("1-same", relation.__str__())
