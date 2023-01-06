from unittest import TestCase
from statisticAndVacancies import Salary


class SalaryTests(TestCase):
    def test_salary_type(self):
        self.assertEqual(type(Salary(14.0, 27.2, 'RUR')).__name__, 'Salary')

    def test_salary_from(self):
        self.assertEqual(Salary(14.0, 27.2, 'RUR').salary_from, 14)

    def test_salary_to(self):
        self.assertEqual(Salary(14.0, 27.2, 'RUR').salary_to, 27.2)

    def test_salary_currency(self):
        self.assertEqual(Salary(14.0, 27.2, 'RUR').salary_currency, 'RUR')

    def test_int_get_salary(self):
        self.assertEqual(Salary(14.0, 27, 'RUR').getSalaryRu(), 20)

    def test_float_salary_from_in_get_salary(self):
        self.assertEqual(Salary(14, 27.0, 'RUR').getSalaryRu(), 20)

    def test_float_salary_to_in_get_salary(self):
        self.assertEqual(Salary(20, 40, 'RUR').getSalaryRu(), 30)

    def test_currency_in_get_salary(self):
        self.assertEqual(Salary(50, 70, 'USD').getSalaryRu(), 3639.6)