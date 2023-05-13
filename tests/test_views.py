import unittest
import psycopg2
from colorama import init, Fore
import datetime

init(autoreset=True)


class TestViews(unittest.TestCase):
    # Установление соединения с базой данных перед каждым тестом
    def setUp(self):
        self.conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="password",
            host="postgres",
            port="5432"
        )
        self.cur = self.conn.cursor()

    # Закрытие соединения с базой данных после каждого теста
    def tearDown(self):
        self.cur.close()
        self.conn.close()

    def test_client_view(self):
        # Получение данных из представления
        self.cur.execute("""
            SELECT * FROM trucking.client_view;
        """)
        results = self.cur.fetchall()

        expected_results = [
            (1, 'Чарли', 'Чаплин', '*******56789', '568****483'),
            (2, 'Опра', 'Уинфри', '*******34567', '908****210'),
            (3, 'Альберт', 'Эйнштейн', '*******43210', '123****890'),
            (4, 'Криштиану', 'Роналду', '*******89012', '456****123'),
            (5, 'Джоанна', 'Роулинг', '*******67890', '789****456'),
            (6, 'Майкл', 'Джордан', '*******34567', '234****901'),
            (7, 'Адольф', 'Гитлер', '*******65432', '876****109'),
            (8, 'Винсент', 'Ван Гог', '*******90123', '654****987'),
            (9, 'Мэрилин', 'Монро', '*******45678', '321****654'),
            (10, 'Уолт', 'Дисней', '*******78901', '987****210')
        ]

        # Проверка результатов
        self.assertEqual(len(results), 10)
        self.assertEqual(results, expected_results)
        print(Fore.GREEN + "TEST PASSED test_client_view")

    def test_driver_view(self):
        # Получение данных из представления
        self.cur.execute("""
            SELECT * FROM trucking.driver_view
            LIMIT 3;
        """)
        results = self.cur.fetchall()

        expected_results = [
            (1, 'Макс', 'Рокатански', 36, 'M009AX', 79261234567, '123****890'),
            (2, 'Кен', 'Майлз', 37, 'K001EH', 74959876543, '987****21'),
            (3, 'Малыш', 'Майлз', 5, 'B437BY', 74995555555, '334****555')
        ]

        # Проверка результатов
        self.assertEqual(len(results), 3)
        self.assertEqual(results, expected_results)
        print(Fore.GREEN + "TEST PASSED test_driver_view")

    def test_order_view(self):
        # Получение данных из представления
        self.cur.execute("""
            SELECT * FROM trucking.order_view
            LIMIT 3;
        """)
        results = self.cur.fetchall()

        expected_results = [
            (1, 1200, 'Альберт', 'Эйнштейн', 'Инструменты',
             datetime.datetime(2023, 4, 14, 16, 0, tzinfo=datetime.timezone.utc)),
            (2, 2000, 'Чарли', 'Чаплин', 'Одежда',
             datetime.datetime(2023, 4, 19, 18, 0, tzinfo=datetime.timezone.utc)),
            (3, 800, 'Мэрилин', 'Монро', 'Книги',
             datetime.datetime(2023, 4, 15, 11, 45, tzinfo=datetime.timezone.utc))
        ]

        # Проверка результатов
        self.assertEqual(len(results), 3)
        self.assertEqual(results, expected_results)
        print(Fore.GREEN + "TEST PASSED test_order_view")

    def test_client_statistic(self):
        # Получение данных из представления
        self.cur.execute("""
            SELECT * FROM trucking.client_statistic
            LIMIT 3;
        """)
        results = self.cur.fetchall()

        expected_results = [(10, 'Уолт', 'Дисней', 2, 3850),
                            (1, 'Чарли', 'Чаплин', 2, 3200),
                            (7, 'Адольф', 'Гитлер', 2, 2900)]

        # Проверка результатов
        self.assertEqual(len(results), 3)
        self.assertEqual(results, expected_results)
        print(Fore.GREEN + "TEST PASSED test_client_statistic")

    def test_finance_statistic(self):
        # Получение данных из представления
        self.cur.execute("""
            SELECT * FROM trucking.finance_statistic
            LIMIT 3;
        """)
        results = self.cur.fetchall()

        expected_results = [(2021.0, 12.0, 28000, 1300),
                            (2021.0, 8.0, 4000, 1200),
                            (2022.0, 7.0, 24000, 900)]

        # Проверка результатов
        self.assertEqual(len(results), 3)
        self.assertEqual(results, expected_results)
        print(Fore.GREEN + "TEST PASSED test_finance_statistic")

    def test_driver_car_info(self):
        # Получение данных из представления
        self.cur.execute("""
            SELECT * FROM trucking.driver_car_info
            LIMIT 3;
        """)
        results = self.cur.fetchall()

        expected_results = [('Макс', 'Рокатански', 'M009AX', 20000, 18000),
                            ('Кен', 'Майлз', 'K001EH', 11000, 30000),
                            ('Малыш', 'Майлз', 'B437BY', 320000, 90000)]

        # Проверка результатов
        self.assertEqual(len(results), 3)
        self.assertEqual(results, expected_results)
        print(Fore.GREEN + "TEST PASSED test_driver_car_info")

    def test_order_details(self):
        # Получение данных из представления
        self.cur.execute("""
            SELECT * FROM trucking.order_details
            LIMIT 3;
        """)
        results = self.cur.fetchall()

        expected_results = [(1, 'Альберт Эйнштейн', 'Peterbilt 379', 'Coast to coast walk', 'Инструменты', 1200),
                            (2, 'Чарли Чаплин', 'International GW3 9800', 'Shwil Israel', 'Одежда', 2000),
                            (3, 'Мэрилин Монро', 'Daf 95 XF', 'GR10', 'Книги', 800)]

        # Проверка результатов
        self.assertEqual(len(results), 3)
        self.assertEqual(results, expected_results)
        print(Fore.GREEN + "TEST PASSED test_order_details")


if __name__ == '__main__':
    unittest.main()
