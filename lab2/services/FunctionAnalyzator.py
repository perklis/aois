from Minimization import Minimization
from services.SdnfSknfBuilder import SdnfSknfBuilder
from services.Differentiation import Differentiation
from services.ExpressionProperties import ExpressionProperties
from services.FictiveVariableService import IsFictiveVariable
from services.PostClassService import PostClassService
from services.TruthTableBuilder import TruthTableBuilder
from services.ZhegalkinPolinom import ZhegalkinPolinom


class FunctionAnalyzator:
    def __init__(self):
        self.expression_service = ExpressionProperties()
        self.truth_table_service = TruthTableBuilder()
        self.canonical_service = SdnfSknfBuilder()
        self.post_service = PostClassService()
        self.zhegalkin_service = ZhegalkinPolinom()
        self.fictive_service = IsFictiveVariable()
        self.derivative_service = Differentiation()
        self.minimization_service = Minimization()

    def set_expression(self, expression):
        return self.expression_service.set_expression(expression)

    def definition(self):
        return self.expression_service.require_definition()

    def shape(self):
        return self.expression_service.analyze_shape()

    def truth_table(self):
        return self.truth_table_service.build(self.definition())

    def canonical(self):
        definition = self.definition()
        return self.canonical_service.build(self.truth_table(), definition.variables)

    def post(self):
        definition = self.definition()
        return self.post_service.analyze(self.truth_table(), definition.variables)

    def zhegalkin(self):
        definition = self.definition()
        return self.zhegalkin_service.build(self.truth_table(), definition.variables)

    def fictive(self):
        definition = self.definition()
        return self.fictive_service.find(self.truth_table(), definition.variables)

    def derivative(self, variables):
        definition = self.definition()
        return self.derivative_service.build(
            self.truth_table(), definition.variables, variables
        )

    def minimize_calculation(self):
        definition = self.definition()
        return self.minimization_service.minimize_calculation(
            self.truth_table(), definition.variables
        )

    def minimize_tabular(self):
        definition = self.definition()
        return self.minimization_service.minimize_tabular(
            self.truth_table(), definition.variables
        )

    def minimize_karnaugh(self):
        definition = self.definition()
        return self.minimization_service.minimize_karno(
            self.truth_table(), definition.variables
        )
