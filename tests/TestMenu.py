import unittest
from unittest.mock import patch
from Menu import Menu
from IEEECalculator import IEEECalculator

class TestMenu(unittest.TestCase):

    @patch("builtins.input", side_effect=["1"])
    def test_select_normal_calculator(self, mock_input):
        menu = Menu()
        menu.select_calculator()
        self.assertEqual(menu.calc_type, "normal")

    @patch("builtins.input", side_effect=["2"])
    def test_select_ieee_calculator(self, mock_input):
        menu = Menu()
        menu.select_calculator()
        self.assertEqual(menu.calc_type, "ieee")

    @patch("builtins.input", side_effect=["3"])
    def test_select_bcd_calculator(self, mock_input):
        menu = Menu()
        menu.select_calculator()
        self.assertEqual(menu.calc_type, "bcd")

    @patch("builtins.input", side_effect=["1", "2"])
    def test_input_numbers_normal(self, mock_input):
        menu = Menu()
        menu.calc_type = "normal"
        menu.calc = __import__("Calculator").Calculator()
        menu.input_numbers()
        self.assertIsNotNone(menu.a)
        self.assertIsNotNone(menu.b)

    @patch("builtins.input", side_effect=["2", "3"])
    def test_input_numbers_ieee(self, mock_input):
        menu = Menu()
        menu.calc_type = "ieee"
        from IEEECalculator import IEEECalculator
        menu.ieee_calc = IEEECalculator()
        menu.input_numbers()
        self.assertIsNotNone(menu.a)
        self.assertIsNotNone(menu.b)

    @patch("builtins.input", side_effect=["123", "456"])
    def test_input_numbers_bcd(self, mock_input):
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

    @patch("builtins.input", side_effect=[
        "2",      # выбор IEEE
        "2",      # число A
        "3",      # число B
        "1",      # сложение
        "0"       # выход
    ])
    def test_run_ieee_add_and_exit(self, mock_input):
        menu = Menu()
        with patch("builtins.print"): 
            menu.run()
        self.assertFalse(menu.running)

    @patch("builtins.input", side_effect=[
        "2",    
        "5",    
        "0",     
        "4",    
        "0"      
    ])
    def test_division_by_zero_in_run(self, mock_input):
        menu = Menu()
        with patch("builtins.print") as mock_print:
            menu.run()

        printed_text = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("деление", printed_text.lower())

    def test_ieee_exit_flag(self):
        menu = Menu()
        menu.calc_type = "ieee"
        menu.running = True
        menu._handle_ieee("0")
        self.assertFalse(menu.running)

    def test_ieee_invalid_choice_does_not_change_running(self):
        menu = Menu()
        menu.calc_type = "ieee"
        menu.running = True
        menu.a = IEEECalculator().decimal_to_ieee("1")
        menu.b = IEEECalculator().decimal_to_ieee("2")
        menu.ieee_calc = IEEECalculator()
        menu._handle_ieee("99")
        self.assertTrue(menu.running)

    def test_input_numbers_sets_a_b_ieee(self):
        menu = Menu()
        menu.calc_type = "ieee"
        menu.ieee_calc = IEEECalculator()
        menu.a = menu.ieee_calc.decimal_to_ieee("1.5")
        menu.b = menu.ieee_calc.decimal_to_ieee("2.5")
        self.assertEqual(menu.a.from_bits_to_decimal(), 1.5)
        self.assertEqual(menu.b.from_bits_to_decimal(), 2.5)


    def test_normal_invalid_choice_does_not_change_running(self):
        menu = Menu()
        menu.calc_type = "normal"
        menu.running = True
        menu._handle_normal("99")  # неправильный пункт
        self.assertTrue(menu.running)    
