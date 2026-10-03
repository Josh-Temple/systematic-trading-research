import unittest
from decimal import Decimal
from fx_quantity_examples import quantity

class ArithmeticTests(unittest.TestCase):
    def case(self, **updates):
        inputs = dict(budget=50, distance='0.50', unit_cost='0.02', fixed_cost=0,
                      equity=10000, price=150, leverage_cap=2, minimum=1, step=1)
        inputs.update(updates)
        return quantity(**inputs)

    def test_matsui_costs_and_floor(self):
        r = self.case()
        self.assertEqual(r['units'], '96')
        self.assertEqual(Decimal(r['reserved_loss_jpy']), Decimal('49.92'))
        self.assertGreater(97 * Decimal('0.52'), 50)

    def test_xm_minimum_cannot_force_tighter_stop(self):
        self.assertEqual(self.case(minimum=100, step=10)['status'], 'SKIP')

    def test_exposure_cap_and_xm_step(self):
        r = self.case(distance='0.30', minimum=100, step=10)
        self.assertEqual(r['units'], '130')
        self.assertLessEqual(Decimal(r['effective_leverage']), 2)
        self.assertGreater(140 * 150, 10000 * 2)

    def test_shared_budget_can_block_xm(self):
        self.assertEqual(self.case(budget=25, distance='0.30', minimum=100, step=10)['status'], 'SKIP')

    def test_exact_boundary(self):
        self.assertEqual(self.case(distance='0.48', minimum=100, step=10)['units'], '100')

    def test_fixed_cost(self):
        self.assertEqual(self.case(fixed_cost=50)['status'], 'SKIP')
        self.assertEqual(self.case(fixed_cost=10)['units'], '76')

    def test_missing_input_blocks(self):
        self.assertEqual(self.case(unit_cost=None)['status'], 'BLOCKED')

    def test_invalid_values(self):
        for changes in [dict(distance=0), dict(unit_cost=-1), dict(price='NaN'),
                        dict(minimum=101, step=10), dict(budget='Infinity')]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.case(**changes)

if __name__ == '__main__':
    unittest.main()
