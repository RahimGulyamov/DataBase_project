import unittest
import psycopg2
from colorama import init, Fore

init(autoreset=True)


class TestQueries(unittest.TestCase):
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

    # Тестирование успешного выполнения запроса INSERT
    def test_insert_to_table_car(self):
        query = """
        INSERT INTO trucking.car 
        VALUES ('A777AA', 0, 'International GW3 9800')
        """
        self.cur.execute(query)
        self.conn.commit()

        # Проверяем, что добавление произошло успешно
        self.assertEqual(self.cur.rowcount, 1)
        print(Fore.GREEN + "TEST PASSED test_insert_to_table_car")
        query_reset = """
        DELETE
        FROM trucking.car
        WHERE car_number = 'A777AA';
        """
        self.cur.execute(query_reset)
        self.conn.commit()

    # Тестирование ошибки нарушения уникального ограничения на car_number
    def test_insert_query_unique_error(self):
        # Добавляем запись с уже существующим car_number
        query = """
        INSERT INTO trucking.car
        VALUES ('M009AX', 0, 'International GW3 9800')
        """
        with self.assertRaises(psycopg2.errors.UniqueViolation):
            self.cur.execute(query)
            self.conn.commit()
        print(Fore.GREEN + "TEST PASSED test_insert_query_unique_error")

    # Тестирование ошибки нарушения внешнего ключа на model
    def test_insert_query_fk_error(self):
        # Добавляем запись с несуществующей моделью
        query = "INSERT INTO trucking.car VALUES ('A888BB', 0, 'Some Unknown Model')"
        with self.assertRaises(psycopg2.errors.ForeignKeyViolation):
            self.cur.execute(query)
            self.conn.commit()
        print(Fore.GREEN + "TEST PASSED test_insert_query_fk_error")

    def test_order_history_price_greater_than_500(self):
        # Выполняем запрос
        query = """
        SELECT order_id, price, history_dttm
        FROM trucking.order_history
        WHERE price > 500;
        """
        self.cur.execute(query)
        result = self.cur.fetchall()
        # Проверяем, что результат не пустой
        assert len(result) > 0
        # Проверяем, что все элементы результата имеют значение price больше 500
        assert all(item[1] > 500 for item in result)
        print(Fore.GREEN + "TEST PASSED test_order_history_price_greater_than_500")

    def test_update_table_transportation(self):
        query = """
        UPDATE trucking.trasportation
        SET departure_date = '2023-04-17 10:15:00', arrival_date = '2023-04-19 12:15:00'
        WHERE transportation_id = 3;
        """
        self.cur.execute(query)
        self.conn.commit()

        # Проверка, что данные были изменены
        self.cur.execute("""
        SELECT departure_date, arrival_date
        FROM trucking.trasportation
        WHERE transportation_id = 3
        """)
        result = self.cur.fetchone()

        self.assertEqual(str(result[0])[:-6], '2023-04-17 10:15:00')  # Проверка, что departure_date было изменено
        self.assertEqual(str(result[1])[:-6], '2023-04-19 12:15:00')  # Проверка, что arrival_date было изменено
        print(Fore.GREEN + "TEST PASSED test_update_table_transportation")

        query_reset = """
        UPDATE trucking.trasportation
        SET departure_date = '2023-04-15 10:15:00', arrival_date = '2023-04-16 12:15:00'
        WHERE transportation_id = 3;
        """
        self.cur.execute(query_reset)
        self.conn.commit()

    def test_delete_from_table_car(self):
        self.cur.execute("""
                        INSERT INTO trucking.car
                        VALUES ('A777AA', 1000, 'Kenworth W900')
                    """)
        self.conn.commit()

        self.cur.execute("""
            DELETE FROM trucking.car
            WHERE car_number = 'A777AA'
        """)
        self.conn.commit()

        # Проверяем, что запись была удалена
        self.cur.execute("""
            SELECT car_number
            FROM trucking.car
            WHERE car_number = 'A777AA'
        """)
        result = self.cur.fetchone()
        self.assertIsNone(result)
        print(Fore.GREEN + "TEST PASSED test_delete_from_table_car")

    def test_crud_insert_to_table_car(self):
        query = """
        INSERT INTO trucking.car
        VALUES ('M009AM', 200000, 'Peterbilt 379');
        """
        self.cur.execute(query)
        self.conn.commit()

        # Проверяем, что добавление произошло успешно
        self.assertEqual(self.cur.rowcount, 1)
        print(Fore.GREEN + "TEST PASSED test_crud_insert_to_table_car")
        query_reset = """
        DELETE
        FROM trucking.car
        WHERE car_number = 'M009AM';
        """
        self.cur.execute(query_reset)
        self.conn.commit()

    def test_crud_select_from_transportation_history(self):
        query = """
        SELECT transportation_id, route_id, driver_id
        FROM trucking.trasportation_history
        LIMIT 5;
        """
        expected_result = [
            (1, 3, 6),
            (2, 3, 8),
            (3, 1, 3),
            (4, 1, 8),
            (5, 10, 1)
        ]

        self.cur.execute(query)
        result = self.cur.fetchall()
        self.assertEqual(expected_result, result)
        print(Fore.GREEN + "TEST PASSED test_crud_select_from_transportation_history")

    def test_crud_update_table_car_models(self):
        query = """
        UPDATE trucking.car_models
        SET capacity = 23000
        WHERE model = 'Peterbilt 379';
        """
        self.cur.execute(query)
        self.conn.commit()

        self.cur.execute("""
        SELECT capacity
        FROM trucking.car_models
        WHERE model = 'Peterbilt 379';
        """)

        result = self.cur.fetchone()
        self.assertEqual(result[0], 23000)
        print(Fore.GREEN + "TEST PASSED test_crud_update_table_car_models")

        query_reset = """
        UPDATE trucking.car_models
        SET capacity = 18000
        WHERE model = 'Peterbilt 379';
        """

        self.cur.execute(query_reset)
        self.conn.commit()

    def test_crud_delete_from_table_car(self):
        self.cur.execute("""
            INSERT INTO trucking.car
            VALUES ('M009AM', 200000, 'Peterbilt 379');
                    """)
        self.conn.commit()

        self.cur.execute("""
            DELETE FROM trucking.car
            WHERE car_number = 'M009AM'
        """)
        self.conn.commit()

        # Проверяем, что запись была удалена
        self.cur.execute("""
            SELECT car_number
            FROM trucking.car
            WHERE car_number = 'M009AM'
        """)
        result = self.cur.fetchone()
        self.assertIsNone(result)
        print(Fore.GREEN + "TEST PASSED test_crud_delete_from_table_car")

    def test_query_9(self):
        # Выполняем тестируемый запрос
        self.cur.execute("""
            SELECT o.order_id, o.price, c.first_name, c.last_name, t.type
            FROM trucking.order o
            JOIN trucking.client c ON o.client_id = c.client_id
            JOIN trucking.type_of_goods t ON o.type_id = t.type_id;
        """)

        # Проверяем, что запрос вернул корректные данные
        result = self.cur.fetchall()
        expected_result = [
            (1, 1200, 'Альберт', 'Эйнштейн', 'Инструменты'),
            (2, 2000, 'Чарли', 'Чаплин', 'Одежда'),
            (3, 800, 'Мэрилин', 'Монро', 'Книги'),
            (4, 1500, 'Опра', 'Уинфри', 'Косметика'),
            (5, 1000, 'Криштиану', 'Роналду', 'Электроника'),
            (6, 3000, 'Уолт', 'Дисней', 'Еда'),
            (7, 900, 'Майкл', 'Джордан', 'Спортивное снаряжение'),
            (8, 1800, 'Джоанна', 'Роулинг', 'Игрушки'),
            (9, 700, 'Винсент', 'Ван Гог', 'Ювелирные изделия'),
            (10, 2500, 'Адольф', 'Гитлер', 'Мебель'),
        ]
        self.assertEqual(result, expected_result)
        print(Fore.GREEN + "TEST PASSED test_query_9")

    def test_query_10(self):
        # Выполняем тестируемый запрос
        self.cur.execute("""
            SELECT d.first_name, d.last_name, COUNT(t.transportation_id) as number_of_trips
            FROM trucking.driver d
                LEFT JOIN trucking.trasportation t ON d.driver_id = t.driver_id
            GROUP BY d.driver_id;
        """)

        # Проверяем, что запрос вернул корректные данные
        result = self.cur.fetchall()
        expected_result = [
            ('Рэндол', 'Рэйес', 1),
            ('Даниэль', 'Моралес', 1),
            ('Брайан', 'О Коннор', 1),
            ('Тобби', 'Маршал', 1),
            ('Макс', 'Рокатански', 1),
            ('Молния', 'МакКвин', 1),
            ('Кен', 'Майлз', 1),
            ('Френк', 'Булит', 1),
            ('Доминик', 'Торетто', 1),
            ('Малыш', 'Майлз', 1)
        ]
        self.assertEqual(result, expected_result)
        print(Fore.GREEN + "TEST PASSED test_query_10")

    def test_query_11(self):
        # Выполняем тестируемый запрос
        self.cur.execute("""
            SELECT r.name
            FROM trucking.route r
                LEFT JOIN trucking.trasportation t ON r.route_id = t.route_id
            WHERE t.transportation_id IS NULL;
        """)

        # Проверяем, что запрос вернул корректные данные
        result = self.cur.fetchall()
        expected_result = [
            ('Mont Blanc',),
            ('Arctic Circle Trail',),
            ('HRP',),
            ('St Jakovs route',),
        ]
        self.assertEqual(result, expected_result)
        print(Fore.GREEN + "TEST PASSED test_query_11")

    def test_query_12(self):
        # Выполняем тестируемый запрос
        self.cur.execute("""
            SELECT c.first_name, c.last_name, COUNT(o.order_id) as number_of_orders, SUM(o.price) as total_price
            FROM trucking.client c
                LEFT JOIN trucking.order o ON c.client_id = o.client_id
            GROUP BY c.client_id;
        """)

        # Проверяем, что запрос вернул корректные данные
        result = self.cur.fetchall()
        expected_result = [
            ('Винсент', 'Ван Гог', 1, 700),
            ('Адольф', 'Гитлер', 1, 2500),
            ('Уолт', 'Дисней', 1, 3000),
            ('Мэрилин', 'Монро', 1, 800),
            ('Чарли', 'Чаплин', 1, 2000),
            ('Джоанна', 'Роулинг', 1, 1800),
            ('Криштиану', 'Роналду', 1, 1000),
            ('Опра', 'Уинфри', 1, 1500),
            ('Майкл', 'Джордан', 1, 900),
            ('Альберт', 'Эйнштейн', 1, 1200)

        ]
        self.assertEqual(result, expected_result)
        print(Fore.GREEN + "TEST PASSED test_query_12")


if __name__ == '__main__':
    unittest.main()
