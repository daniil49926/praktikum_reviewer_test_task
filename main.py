import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if  # 7
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for Record in self.records:  # 1
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and  # 2
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()  # 6
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):  # 3
        currency_type = currency  # 4
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00  # 4
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:  # 8
            return 'Денег нет, держись'
        elif cash_remained < 0:  # 9
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        super().get_week_stats()  # 5

# Следует исправить:
# 1) В другой области видимости у Вас уже есть класс с названием Record, может стоит переименовать, также стоит
# использовать нижний регистр в названиях переменных
# 2) Рекомендую объеденить данные условия в одно и убрать лишние скобки
# 3) Данные аргументы лишние, в данном методе Вы можете обратиться к переменным-константам класса через self
# 4) В данном случае в строчке 66 Вы используете оператор сравнения. Также, если калькулятор принимает на вход рубли,
# может лучше присвоить значение 'руб' в 57 строчке и удалить условие elif на 65 строчке?
# 5) Если вы не меняете логику функции, то не следует у дочернего класса прописывать
# метод super, данная функция будет унаследованна от класса родителя при создание класса
# 6) Не стоит использовать лишние переменный, тем более однобуквенные
# 7) В данном случае можно указать dt.datetime.now().date() как значение параметра date по дефолту и
# убрать лишние if else. Также вместо dt.datetime.now().date рекомендую использовать dt.date.today()
# 8) Следует вынести данное условие сразу после рассчета cash_remained, таким образом, если денег не будет, функция не
# будет проводить лишних расчетов
# 9) Выше по коду присутсвует проверка ">" и "==", можем убрать elif
# - По коду Вы используете разное форматирование строк, было бы правильно привести все к одному форматированию.
# - Не следует применять '/' для переноса строчки, можно обернуть строку в скобки
# - Также, не следует переносить строчки, если она не выходит за рамки 120 символов в строке.
# - Не стоит оборачивать строки в скобки.
# - В функции get_today_cash_remained в одном из return'ов Вы используете округление до второго знака после запятой,
#   для переменной cash_remained, почему бы не использовать огругление для этой переменной и в другом retern'e. Также
#   следует вынести round из f строки.
# - Вместо комментариев к функциям стоит написать docstring
# - Хорошая практика писать docstring к каждому классу
# - Желательно импортировать только методы, которые используются в коде
# - В строчке 52 и 53 можно использовать типизацию, либо сразу указать значение типа float (70.0)

