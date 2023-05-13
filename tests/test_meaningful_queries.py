import unittest
import psycopg2
from colorama import init, Fore

init(autoreset=True)


class TestMeaningfulQueries(unittest.TestCase):
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

    def test_meaningful_query_1(self):
        # Выполняем тестируемый запрос
        self.cur.execute("""
            SELECT model, AVG(distance) as avg_distance
            FROM trucking.car
            GROUP BY model
            HAVING COUNT(*) >= 2
            ORDER BY avg_distance DESC
            LIMIT 10;
                """)

        # Проверяем, что запрос вернул корректные данные
        result = self.cur.fetchall()
        expected_result = [
            ('Mack Titan', 191500),
            ('MAN TGA 33.480', 70000),
            ('Volvo FH', 5900)
        ]
        self.assertEqual(result, expected_result)
        print(Fore.GREEN + "TEST PASSED test_meaningful_query_1")

    def test_meaningful_query_2(self):
        # Выполняем тестируемый запрос
        self.cur.execute("""
            SELECT first_name, last_name, SUM(o.price) + SUM(oh.price) as total_spent
            FROM trucking.client c
                     JOIN trucking.order o ON c.client_id = o.client_id
                     JOIN trucking.order_history oh ON c.client_id = oh.client_id
            GROUP BY first_name, last_name
            HAVING SUM(o.price) + SUM(oh.price) > 2000
            ORDER BY total_spent DESC;
                """)

        # Проверяем, что запрос вернул корректные данные
        result = self.cur.fetchall()
        expected_result = [
            ('Уолт', 'Дисней', 3850),
            ('Чарли', 'Чаплин', 3200),
            ('Адольф', 'Гитлер', 2900),
            ('Джоанна', 'Роулинг', 2600),
            ('Опра', 'Уинфри', 2400)
        ]
        self.assertEqual(result, expected_result)
        print(Fore.GREEN + "TEST PASSED test_meaningful_query_2")

    def test_meaningful_query_3(self):
        # Выполняем тестируемый запрос
        self.cur.execute("""
            SELECT DISTINCT d.driver_id,
                            first_name,
                            last_name,
                            SUM(distance) OVER (PARTITION BY d.driver_id)        as total_distance,
                            SUM(drivers_payment) OVER (PARTITION BY d.driver_id) as total_payment
            FROM trucking.driver d
                     JOIN trucking.trasportation_history th ON d.driver_id = th.driver_id
                     JOIN trucking.route r ON th.route_id = r.route_id
            WHERE DATE_PART('year', th.history_dttm) = 2022
            ORDER BY total_distance DESC, total_payment DESC;

                """)

        # Проверяем, что запрос вернул корректные данные
        result = self.cur.fetchall()
        expected_result = [
            (8, 'Рэндол', 'Рэйес', 1755, 44000),
            (1, 'Макс', 'Рокатански', 800, 20000),
            (5, 'Молния', 'МакКвин', 440, 11000),
            (6, 'Доминик', 'Торетто', 440, 11000)
        ]
        self.assertEqual(result, expected_result)
        print(Fore.GREEN + "TEST PASSED test_meaningful_query_3")

    def test_meaningful_query_4(self):
        # Выполняем тестируемый запрос
        self.cur.execute("""
            SELECT DISTINCT DATE_PART('year', th.history_dttm)                                          AS year,
                            SUM(drivers_payment) OVER (PARTITION BY DATE_PART('year', th.history_dttm)) AS total_payment,
                            SUM(price) OVER (PARTITION BY DATE_PART('year', th.history_dttm))           AS total_price
            FROM trucking.trasportation_history th
                     JOIN trucking.route r ON th.route_id = r.route_id
                     JOIN trucking.order_history oh ON th.transportation_id = oh.transportation_id
            ORDER BY total_price DESC, total_payment;
                """)

        # Проверяем, что запрос вернул корректные данные
        result = self.cur.fetchall()
        expected_result = [
            (2021, 77800, 3700),
            (2022, 86000, 3550)
        ]
        self.assertEqual(result, expected_result)
        print(Fore.GREEN + "TEST PASSED test_meaningful_query_4")

    def test_meaningful_query_5(self):
        # Выполняем тестируемый запрос
        self.cur.execute("""
            SELECT first_name,
                   last_name,
                   driving_exp,
                   RANK() OVER (ORDER BY driving_exp DESC) as rank
            FROM trucking.driver
            ORDER BY rank
            LIMIT 10;
                """)

        # Проверяем, что запрос вернул корректные данные
        result = self.cur.fetchall()
        expected_result = [
            ('Кен', 'Майлз', 37, 1),
            ('Макс', 'Рокатански', 36, 2),
            ('Доминик', 'Торетто', 22, 3),
            ('Даниэль', 'Моралес', 15, 4),
            ('Тобби', 'Маршал', 11, 5),
            ('Молния', 'МакКвин', 10, 6),
            ('Френк', 'Булит', 9, 7),
            ('Брайан', 'О Коннор', 8, 8),
            ('Малыш', 'Майлз', 5, 9),
            ('Рэндол', 'Рэйес', 4, 10)
        ]
        self.assertEqual(result, expected_result)
        print(Fore.GREEN + "TEST PASSED test_meaningful_query_5")

    def test_meaningful_query_6(self):
        # Выполняем тестируемый запрос
        self.cur.execute("""
            SELECT DISTINCT r.route_id,
                            name AS route_name,
                            COUNT(*) OVER (PARTITION BY r.route_id) AS amount,
                            SUM(price) OVER (PARTITION BY r.route_id) AS total_price
            FROM trucking.route r
                     JOIN trucking.trasportation_history th ON r.route_id = th.route_id
                     JOIN trucking.order_history oh ON th.transportation_id = oh.transportation_id
            ORDER BY  total_price DESC, amount DESC;
                """)

        # Проверяем, что запрос вернул корректные данные
        result = self.cur.fetchall()
        expected_result = [
            (8, 'Arctic Circle Trail', 2, 2200),
            (7, 'Kungsleden', 2, 1650),
            (3, 'HRP', 3, 1500),
            (1, 'GR10', 2, 1200),
            (10, 'Shwil Israel', 1, 700)
        ]
        self.assertEqual(result, expected_result)
        print(Fore.GREEN + "TEST PASSED test_meaningful_query_6")


if __name__ == '__main__':
    unittest.main()
