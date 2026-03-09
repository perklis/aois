import unittest
from unittest.mock import patch

from Menu import Menu
from IEEECalculator import IEEECalculator
from Calculator import Calculator
from BCD2421Calculator import BCD2421Calculator


class TestMenu(unittest.TestCase):
    def setUp(self):
        self.print_patcher = patch("builtins.print")
        self.mock_print = self.print_patcher.start()

    def tearDown(self):
        self.print_patcher.stop()

    @patch("builtins.input", side_effect=["1"])
    def test_select_normal_calculator(self, _):
        menu = Menu()
        menu.select_calculator()
        self.assertEqual(menu.calc_type, "normal")

    @patch("builtins.input", side_effect=["2"])
    def test_select_ieee_calculator(self, _):
        menu = Menu()
        menu.select_calculator()
        self.assertEqual(menu.calc_type, "ieee")

    @patch("builtins.input", side_effect=["3"])
    def test_select_bcd_calculator(self, _):
        menu = Menu()
        menu.select_calculator()
        self.assertEqual(menu.calc_type, "bcd")

    @patch("builtins.input", side_effect=["9", "1"])
    def test_select_retry_on_invalid_choice(self, _):
        menu = Menu()
        menu.select_calculator()
        self.assertEqual(menu.calc_type, "normal")

    @patch("builtins.input", side_effect=["5", "6"])
    def test_input_numbers_normal(self, _):
        menu = Menu()
        menu.calc_type = "normal"
        menu.calc = Calculator()
        menu.input_numbers()
        self.assertIsNotNone(menu.a)
        self.assertIsNotNone(menu.b)

    @patch("builtins.input", side_effect=["1.5", "2.5"])
    def test_input_numbers_ieee(self, _):
        menu = Menu()
        menu.calc_type = "ieee"
        menu.ieee_calc = IEEECalculator()
        menu.input_numbers()
        self.assertEqual(menu.a.from_bits_to_decimal(), 1.5)
        self.assertEqual(menu.b.from_bits_to_decimal(), 2.5)

    @patch("builtins.input", side_effect=["123", "456"])
    def test_input_numbers_bcd(self, _):
        menu = Menu()
        menu.calc_type = "bcd"
        menu.input_numbers()
        self.assertEqual(menu.a, [1, 2, 3])
        self.assertEqual(menu.b, [4, 5, 6])

    def test_handle_exit_normal(self):
        menu = Menu()
        menu.calc_type = "normal"
        menu.running = True
        menu._handle_normal("0")
        self.assertFalse(menu.running)

    def test_handle_exit_ieee(self):
        menu = Menu()
        menu.calc_type = "ieee"
        menu.running = True
        menu._handle_ieee("0")
        self.assertFalse(menu.running)

    def test_handle_exit_bcd(self):
        menu = Menu()
        menu.calc_type = "bcd"
        menu.running = True
        menu._handle_bcd("0")
        self.assertFalse(menu.running)

    def test_normal_invalid_choice_does_not_exit(self):
        menu = Menu()
        menu.calc_type = "normal"
        menu.running = True
        menu._handle_normal("99")
        self.assertTrue(menu.running)

    def test_ieee_invalid_choice_does_not_exit(self):
        menu = Menu()
        menu.calc_type = "ieee"
        menu.ieee_calc = IEEECalculator()
        menu.a = menu.ieee_calc.decimal_to_ieee("1")
        menu.b = menu.ieee_calc.decimal_to_ieee("2")
        menu.running = True
        menu._handle_ieee("99")
        self.assertTrue(menu.running)

    def test_bcd_invalid_choice_does_not_exit(self):
        menu = Menu()
        menu.calc_type = "bcd"
        menu.running = True
        menu._handle_bcd("99")
        self.assertTrue(menu.running)

    @patch("builtins.input", side_effect=["2", "2", "3", "1", "0"])
    def test_run_ieee_add_and_exit(self, _):
        menu = Menu()
        menu.run()
        self.assertFalse(menu.running)

    @patch("builtins.input", side_effect=["2", "5", "0", "4", "0"])
    def test_division_by_zero_in_run(self, _):
        menu = Menu()
        menu.run()
        printed_text = " ".join(str(call) for call in self.mock_print.call_args_list)
        self.assertIn("деление", printed_text.lower())

    def test_ieee_exit_flag(self):
        menu = Menu()
        menu.calc_type = "ieee"
        menu.running = True
        menu._handle_ieee("0")
        self.assertFalse(menu.running)

    def test_input_numbers_sets_a_b_ieee(self):
        menu = Menu()
        menu.calc_type = "ieee"
        menu.ieee_calc = IEEECalculator()
        menu.a = menu.ieee_calc.decimal_to_ieee("1.5")
        menu.b = menu.ieee_calc.decimal_to_ieee("2.5")
        self.assertEqual(menu.a.from_bits_to_decimal(), 1.5)
        self.assertEqual(menu.b.from_bits_to_decimal(), 2.5)

    def test_print_menu_normal(self):
        menu = Menu()
        menu.calc_type = "normal"
        menu.calc = Calculator()
        menu.a = Calculator().add(
            __import__("NumbersConverter").NumbersConverter.from_decimal_to_direct_code(
                1
            ),
            __import__("NumbersConverter").NumbersConverter.from_decimal_to_direct_code(
                0
            ),
        )
        menu.b = menu.a
        menu.print_menu()
        self.assertTrue(self.mock_print.called)

    def test_print_menu_ieee(self):
        menu = Menu()
        menu.calc_type = "ieee"
        menu.ieee_calc = IEEECalculator()
        menu.a = menu.ieee_calc.decimal_to_ieee("1.0")
        menu.b = menu.ieee_calc.decimal_to_ieee("2.0")
        menu.print_menu()
        self.assertTrue(self.mock_print.called)

    def test_print_menu_bcd(self):
        menu = Menu()
        menu.calc_type = "bcd"
        menu.bcd_calc = BCD2421Calculator()
        menu.a = [1, 2]
        menu.b = [3, 4]
        menu.print_menu()
        self.assertTrue(self.mock_print.called)

    def test_handle_normal_operations(self):
        menu = Menu()
        menu.calc_type = "normal"
        menu.calc = Calculator()
        menu.a = __import__(
            "NumbersConverter"
        ).NumbersConverter.from_decimal_to_direct_code(8)
        menu.b = __import__(
            "NumbersConverter"
        ).NumbersConverter.from_decimal_to_direct_code(2)

        menu._handle_normal("1")
        menu._handle_normal("2")
        menu._handle_normal("3")
        menu._handle_normal("4")
        menu._handle_normal("5")

        self.assertTrue(self.mock_print.called)

    def test_handle_ieee_operations(self):
        menu = Menu()
        menu.calc_type = "ieee"
        menu.ieee_calc = IEEECalculator()
        menu.a = menu.ieee_calc.decimal_to_ieee("6.0")
        menu.b = menu.ieee_calc.decimal_to_ieee("2.0")

        menu._handle_ieee("1")
        menu._handle_ieee("2")
        menu._handle_ieee("3")
        menu._handle_ieee("4")

        self.assertTrue(self.mock_print.called)

    def test_handle_bcd_addition(self):
        menu = Menu()
        menu.calc_type = "bcd"
        menu.bcd_calc = BCD2421Calculator()
        menu.a = [1, 2]
        menu.b = [3, 4]
        menu._handle_bcd("1")
        self.assertTrue(self.mock_print.called)

    @patch("builtins.input", side_effect=["abc", "1", "2", "3"])
    def test_input_numbers_normal_value_error(self, _):
        menu = Menu()
        menu.calc_type = "normal"
        menu.calc = Calculator()
        menu.input_numbers()
        self.assertIsNotNone(menu.a)
        self.assertIsNotNone(menu.b)

    @patch("builtins.input", side_effect=["nan", "1"])
    def test_input_numbers_ieee_nan(self, _):
        menu = Menu()
        menu.calc_type = "ieee"
        menu.ieee_calc = IEEECalculator()
        menu.input_numbers()
        self.assertIsNotNone(menu.a)

    @patch("builtins.input", side_effect=["1", "1", "2", "x", "0"])
    def test_run_value_error_branch(self, _):
        menu = Menu()
        menu.run()
        self.assertFalse(menu.running)
