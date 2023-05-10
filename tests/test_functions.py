import unittest
import psycopg2
from colorama import init, Fore
import datetime

init(autoreset=True)


class TestViews(unittest.TestCase):
    # Установление соединения с базой данных перед каждым тестом
    def setUp(self):
        self.conn = psycopg2.connect(
            dbname="pg_db",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        self.cur = self.conn.cursor()

    # Закрытие соединения с базой данных после каждого теста
    def tearDown(self):
        self.cur.close()
        self.conn.close()

    def test_get_route_info_by_order_id(self):
        # Получение данных из представления
        self.cur.execute("""
                    SELECT get_route_info_by_order_id(5);
                """)
        results = self.cur.fetchall()

        expected_results = [('(7,440,Kungsleden,11000)',)]

        # Проверка результатов
        self.assertEqual(len(results), 1)
        self.assertEqual(results, expected_results)
        print(Fore.GREEN + "TEST PASSED test_get_route_info_by_order_id")

    def test_get_fulfilled_orders(self):
        # Получение данных из представления
        self.cur.execute("""
                    SELECT get_fulfilled_orders('2022-04-14 16:00:00.000000 +00:00', '2023-04-14 16:00:00.000000 +00:00');
                """)
        results = self.cur.fetchall()

        expected_results = [('(5,"Криштиану Роналду",1000)',), ('(6,"Уолт Дисней",3000)',)]

        # Проверка результатов
        self.assertEqual(len(results), 2)
        self.assertEqual(results, expected_results)
        print(Fore.GREEN + "TEST PASSED test_get_fulfilled_orders")

    def test_get_driver_and_car_info(self):
        # Получение данных из представления
        self.cur.execute("""
                    SELECT get_driver_and_car_info('Y013ME');
                """)
        results = self.cur.fetchall()

        expected_results = [('("Брайан О Коннор",79033334455,"Freightliner FLD 120SD",18200)',)]

        # Проверка результатов
        self.assertEqual(len(results), 1)
        self.assertEqual(results, expected_results)
        print(Fore.GREEN + "TEST PASSED test_get_driver_and_car_info")

    def test_get_clients_with_order_count(self):
        # Получение данных из представления
        self.cur.execute("""
                    SELECT get_clients_with_order_count();
                """)
        results = self.cur.fetchall()

        expected_results = [('("Винсент Ван Гог",1)',),
                            ('("Адольф Гитлер",1)',),
                            ('("Уолт Дисней",1)',),
                            ('("Мэрилин Монро",1)',),
                            ('("Чарли Чаплин",1)',),
                            ('("Джоанна Роулинг",1)',),
                            ('("Криштиану Роналду",1)',),
                            ('("Опра Уинфри",1)',),
                            ('("Майкл Джордан",1)',),
                            ('("Альберт Эйнштейн",1)',)]
        # Проверка результатов
        self.assertEqual(len(results), 10)
        self.assertEqual(results, expected_results)
        print(Fore.GREEN + "TEST PASSED test_get_clients_with_order_count")


if __name__ == '__main__':
    unittest.main()
