import unittest
from main import CoffeeOrder, CoffeeOrderBuilder

class TestCoffeeBuilder(unittest.TestCase):

    def setUp(self):
        self.builder = CoffeeOrderBuilder()

    def test_basic_order(self):
        order1 = (
            self.builder.set_base("latte")
            .set_size("medium")
            .set_milk("oat")
            .add_syrup("vanilla")
            .set_sugar(2)
            .set_iced()
            .build()
        )

        # Ожидаемая цена: (300 * 1.2) + 60 + 40 + 20 = 480
        self.assertIsInstance(order1, CoffeeOrder)
        self.assertEqual(order1.base, "latte")
        self.assertEqual(order1.size, "medium")
        self.assertEqual(order1.milk, "oat")
        self.assertIn("vanilla", order1.syrups)
        self.assertEqual(order1.sugar, 2)
        self.assertTrue(order1.iced)
        self.assertEqual(order1.price, 480.0)
        self.assertEqual(str(order1), "medium latte with oat milk + vanilla (iced) 2 tsp sugar")
        print("\nTest 1 (Basic Order) Passed!")

    def test_builder_reuse(self):
        order1 = self.builder.set_base("latte").set_size("medium").build()
        self.assertEqual(order1.price, 360.0)

        order2 = (
            self.builder.set_base("americano")
            .set_size("large")
            .clear_extras()
            .add_syrup("caramel")
            .build()
        )

        # Ожидаемая цена: (250 * 1.4) + 40 = 390
        self.assertEqual(order2.price, 390.0)
        self.assertEqual(order2.base, "americano")
        self.assertEqual(order2.milk, "none")
        self.assertFalse(order2.iced)

        self.assertEqual(order1.base, "latte")
        self.assertEqual(order1.price, 360.0)
        print("Test 2 (Builder Reuse) Passed!")

    def test_validation(self):
        with self.assertRaisesRegex(ValueError, "Base must be set"):
            self.builder.reset().set_size("small").build()

        with self.assertRaisesRegex(ValueError, "Size must be set"):
            self.builder.reset().set_base("espresso").build()

        with self.assertRaisesRegex(ValueError, "Sugar must be between"):
            self.builder.set_sugar(10)
        print("Test 3 (Validation) Passed!")

    def test_logic_checks(self):
        """Тест 4: Логические проверки"""
        order_syrup = (
            self.builder.reset()
            .set_base("cappuccino")
            .set_size("small")
            .add_syrup("chocolate")
            .add_syrup("chocolate")
            .build()
        )
        # Цена: 320 * 1.0 + 40 (один сироп) = 360
        self.assertEqual(order_syrup.price, 360.0)
        self.assertEqual(len(order_syrup.syrups), 1)

        order_no_ice = self.builder.set_iced(False).build()
        order_with_ice = self.builder.set_iced(True).build()
        self.assertEqual(order_with_ice.price, order_no_ice.price + self.builder.ICED_PRICE)
        print("Test 4 (Logic Checks) Passed!")


if __name__ == '__main__':
    unittest.main()