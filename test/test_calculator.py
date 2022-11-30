import unittest
from server import calculator

class FormulaToTokensTest(unittest.TestCase):
    # Normal test
    def test_normal1(self):
        arg = "3+4-5*6/7"
        expected = [3, "+", 4, "-", 5, "*", 6, "/", 7]
        result = calculator.formula_to_tokens(arg)
        self.assertEqual(result, expected)

    def test_normal2(self):
        arg = "(1+2)-(6676-1)*3/(33)"
        expected = ["(", 1, "+", 2, ")", "-", "(", 6676, "-", 1, ")", "*", 3, "/", "(", 33, ")"]
        result = calculator.formula_to_tokens(arg)
        self.assertEqual(result, expected)

    def test_normal3(self):
        arg = "3+4-5.5*6/7"
        expected = [3, "+", 4, "-", 5.5, "*", 6, "/", 7]
        result = calculator.formula_to_tokens(arg)
        self.assertEqual(result, expected)

    def test_normal4(self):
        arg = "1+2"
        expected = [1/3*3, "+", 2]
        result = calculator.formula_to_tokens(arg)
        self.assertEqual(result, expected)

    def test_formula_with_space(self):
        arg = "1 + 2"
        expected = [1, "+", 2]
        result = calculator.formula_to_tokens(arg)
        self.assertEqual(result, expected)

    # Empty bracket exception test
    def test_empty_bracket(self):
        self.assertRaises(calculator.CalculatorInvalidFormulaError, calculator.formula_to_tokens, "()")

    # Empty formula exception test
    def test_empty_formula(self):
        self.assertRaises(calculator.CalculatorInvalidFormulaError, calculator.formula_to_tokens, "")

    # Invalid tokens exception test
    def test_invalid_token(self):
        self.assertRaises(calculator.CalculatorInvalidTokenError, calculator.formula_to_tokens, "1*.7$")

class InfixToPostfixTest(unittest.TestCase):
    def test_normal1(self):
        arg = [1.0, "+", 2.0]
        expected = [1.0, 2.0, "+"]
        result = calculator.infix_to_postfix(arg)
        self.assertEqual(expected, result)

    def test_normal2(self):
        arg = [1.0, "+", 2.0, "*", 3.0]
        expected = [1.0, 2.0, 3.0, "*", "+"]
        result = calculator.infix_to_postfix(arg)
        self.assertEqual(expected, result)

    def test_normal3(self):
        arg = [1.0, "*", 2.0, "+", 3.0]
        expected = [1.0, 2.0, "*", 3.0, "+"]
        result = calculator.infix_to_postfix(arg)
        self.assertEqual(expected, result)

    def test_normal4(self):
        arg = [5.0, "*", 2.0, "^", 2.0, "%", 3.0]
        expected = [5.0, 2.0, 2.0, "^", "*", 3.0, "%"]
        result = calculator.infix_to_postfix(arg)
        self.assertEqual(expected, result)

    def test_bracket(self):
        arg = [1.0, "*", "(", 2.0, "+", 3.0, ")"]
        expected = [1.0, 2.0, 3.0, "+", "*"]
        result = calculator.infix_to_postfix(arg)
        self.assertEqual(expected, result)

    def test_invalid_bracket(self):
        self.assertRaises(calculator.CalculatorInvalidFormulaError, calculator.infix_to_postfix, [1.0, "*", 2.0, "+", 3.0, ")"])

class ComputePostfixTest(unittest.TestCase):
    def test_normal1(self):
        arg = [1.0, 2.0, "+"]
        expected = 3
        result = calculator.compute_postfix(arg)
        self.assertEqual(result, expected)

    def test_normal2(self):
        arg = [1.0, 2.0, 3.0, "*", "+"]
        expected = 7
        result = calculator.compute_postfix(arg)
        self.assertEqual(result, expected)

    def test_normal3(self):
        arg = [1.0, 2.0, "*", 3.0, "+"]
        expected = 5
        result = calculator.compute_postfix(arg)
        self.assertEqual(result, expected)

    def test_normal4(self):
        arg = [5.0, 2.0, 2.0, "^", "*", 3.0, "%"]
        expected = 2
        result = calculator.compute_postfix(arg)
        self.assertEqual(result, expected)
    
    def test_divided_by_zero(self):
        self.assertRaises(calculator.CalculatorInvalidFormulaError, calculator.compute_postfix, [1, 0, "/"])

class ComputeTest(unittest.TestCase):
    def test_normal1(self):
        arg = "1+2"
        expected = "3.00"
        result = calculator.compute(arg)
        self.assertEqual(result, expected)

    def test_normal2(self):
        arg = "5*2^2%3"
        expected = "2.00"
        result = calculator.compute(arg)
        self.assertEqual(result, expected)

    def test_normal3(self):
        arg = "2*9%5+2*8/4"
        expected = "7.00"
        result = calculator.compute(arg)
        self.assertEqual(result, expected)

    def test_normal4(self):
        arg = "12+5*8+(9.12-7.774)*8"
        expected = "62.77"
        result = calculator.compute(arg)
        self.assertEqual(result, expected)

    def test_big_number(self):
        arg = "1111111111111111111111111111111111111+1111111111111111111111111111111111111"
        expected = "2222222222222222222222222222222222222.00"
        result = calculator.compute(arg)
        self.assertEqual(result, expected)

    def test_divided_by_zero(self):
        arg = "1/0"
        expected = "invalid input"
        result = calculator.compute(arg)
        self.assertEqual(result, expected)

    def test_invalid_formula(self):
        arg = "59-*/6"
        expected = "invalid input"
        result = calculator.compute(arg)
        self.assertEqual(result, expected)