from BitUtils import index_to_assignment
from models.TruthTableRow import TruthTableRow


class TruthTableBuilder:
    def build(self, definition):
        rows = []
        variable_count = len(definition.variables)
        for index in range(1 << variable_count):
            assignment = index_to_assignment(index, definition.variables)
            value = definition.root.evaluate(assignment)
            rows.append(TruthTableRow(index, assignment, value))
        return tuple(rows)
