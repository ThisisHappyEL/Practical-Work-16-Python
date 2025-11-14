from dataclasses import dataclass, field

@dataclass(frozen=True)
class CoffeeOrder:
    base: str
    size: str
    milk: str
    syrups: tuple[str, ...]
    sugar: int
    iced: bool
    price: float
    description: str
    
    def __str__(self) -> str:
        return self.description if self.description else f'Price: {self.price:.2f}'

class CoffeeOrderBuilder:
    """
    Строитель для создания заказов на кофе с использованием текучего интерфейса.
    
    Позволяет пошагово настроить напиток (базу, размер, добавки),
    автоматически рассчитывает итоговую стоимость и генерирует
    человекочитаемое описание. Метод build() финализирует заказ.
    
    Правила и ограничения:
    - Обязательные поля: base (база) и size (размер) должны быть указаны.
    - Максимум сиропов: 4.
    - Диапазон сахара: от 0 до 5 ложек.
    
    Пример использования:
        builder = CoffeeOrderBuilder()
        order = (
            builder.set_base("latte")
            .set_size("medium")
            .add_syrup("vanilla")
            .build()
        )
        print(order)
    """
    BASE_PRICES = { 'espresso': 200, 'americano': 250, 'latte': 300, 'cappuccino': 320 }
    SIZE_MULTIPLIERS = { 'small': 1.0, 'medium': 1.2, 'large': 1.4 }
    MILK_PRICES = { 'none': 0.0, 'whole': 30, 'skim': 30, 'oat': 60, 'soy': 50 }
    SYRUP_PRICE = 40
    ICED_PRICE = 20

    MAX_SYRUPS = 4
    SUGAR_RANGE = (0, 5)

    VALID_BASES = set(BASE_PRICES.keys())
    VALID_SIZES = set(SIZE_MULTIPLIERS.keys())
    VALID_MILKS = set(MILK_PRICES.keys())

    def __init__(self):
        self.reset()
    
    def reset(self):
        self.base = None
        self.size = None
        self.milk = 'none'
        self.syrups = set()
        self.sugar = 0
        self.iced = False
        return self
    
    def set_base(self, base: str):
        if base not in self.VALID_BASES:
            raise ValueError(f'Invalid base: {base}. Allowed: {self.VALID_BASES}')
        self.base = base
        return self
    
    def set_size(self, size: str):
        if size not in self.VALID_SIZES:
            raise ValueError(f'Invalid size: {size}. Allowed: {self.VALID_SIZES}')
        self.size = size
        return self
    
    def set_milk(self, milk: str):
        if milk not in self.VALID_MILKS:
            raise ValueError(f'Invalid milk: {milk}. Allowed: {self.VALID_MILKS}')
        self.milk = milk
        return self
    
    def add_syrup(self, syrup_name: str):
        if len(self.syrups) >= self.MAX_SYRUPS:
            return self
        self.syrups.add(syrup_name)
        return self
    
    def set_sugar(self, teaspoons: int):
        min_sugar_spoons, max_sugar_spoons = self.SUGAR_RANGE
        if not(min_sugar_spoons <= teaspoons <= max_sugar_spoons):
            raise ValueError(
                f'Sugar must be between {min_sugar_spoons} and {max_sugar_spoons} teaspoons'
            )
        self.sugar = teaspoons
        return self
    
    def set_iced(self, iced: bool = True):
        self.iced = iced
        return self
    
    def clear_extras(self):
        self.milk = 'none'
        self.syrups.clear()
        self.sugar = 0
        self.iced = False
        return self
    
    def build(self):
        if self.base is None:
            raise ValueError('Base must be set')
        if self.size is None:
            raise ValueError('Size must be set')

        price = self.BASE_PRICES[self.base]
        price *= self.SIZE_MULTIPLIERS[self.size]
        price += self.MILK_PRICES[self.milk]
        price += len(self.syrups) * self.SYRUP_PRICE
        if self.iced: price += self.ICED_PRICE

        description = f'{self.size} {self.base}'
        if self.milk != 'none': description += f' with {self.milk} milk'
        if self.syrups: description += f' + {', '.join(sorted(list(self.syrups)))}'
        if self.iced: description += f' (iced)'
        if self.sugar > 0: description += f' {self.sugar} tsp sugar'

        return CoffeeOrder(
            base = self.base,
            size = self.size,
            milk = self.milk,
            syrups = tuple(sorted(list(self.syrups))),
            sugar = self.sugar,
            iced = self.iced,
            price = price,
            description = description,
        )
