import unittest
from unittest.mock import patch
from Menu import Menu


class TestMenu(unittest.TestCase):
    def test_unknown_option(self):
        menu = Menu()
        with patch("builtins.print") as print_mock:
            menu._handle("999")
        print_mock.assert_called_with("Неизвестный пункт меню")

    def test_input_expression_action(self):
        menu = Menu()
        with patch("builtins.input", return_value="a|b"):
            menu._input_expression()
        self.assertEqual(menu.facade.definition().variables, ("a", "b"))

    def test_show_fictive_without_values(self):
        menu = Menu()
        menu.facade.set_expression("a")
        with patch("builtins.print") as print_mock:
            menu._show_fictive()
        print_mock.assert_called_with("Фиктивных переменных нет")

    def test_show_derivative(self):
        menu = Menu()
        menu.facade.set_expression("a&b")
        with patch("builtins.input", return_value="a"):
            with patch("builtins.print") as print_mock:
                menu._show_derivative()
        self.assertTrue(print_mock.called)
