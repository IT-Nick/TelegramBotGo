from currency import ParsingTrading


class TriggerTrading:
    finanz = ParsingTrading()

    percent_currency = 0.01  # 1. Валютные – (любой скачек от 10%)
    percent_metals = 2.75  # 2. Драгоценные металлы - 2,75%
    percent_materials = 4.27  # 3. Основные материалы - 4,23%

    difference_currency = {}  # Изначальная сумма + процент
    difference_metals = {}
    difference_materials = {}

    current_price_currency = {}  # цена на старте
    current_price_metals = {}
    current_price_materials = {}

    # Ставим изначальную стоимость + находим процент
    def set_current_price(self):
        # Валюта
        self.current_price_currency = self.finanz.get_currency_price()
        for key, value in zip(self.current_price_currency, self.current_price_currency.values()):
            self.difference_currency[key] = str(float(value) / 100 * self.percent_currency)
        print(self.current_price_currency)
        # Металл
        self.current_price_metals = self.finanz.get_metals_price()
        for key, value in zip(self.current_price_metals, self.current_price_metals.values()):
            self.difference_metals[key] = str(float(value) / 100 * self.percent_metals)
        print(self.current_price_metals)
        # Материал
        self.current_price_materials = self.finanz.get_materials_price()
        for key, value in zip(self.current_price_materials, self.current_price_materials.values()):
            self.difference_materials[key] = str(float(value) / 100 * self.percent_materials)
        print(self.current_price_materials)

    # Возвращаем триггерную цену
    def get_current_price(self):
        result = {}
        # Валюта
        result.update(self.current_price_currency)
        # Металл
        result.update(self.current_price_metals)
        # Материал
        result.update(self.current_price_materials)
        return result

    # Сравниваем текущую сумму с изначальной +(-) процент
    def check(self, start_price, difference, current, cur_name, msg, percent) -> bool:
        err = False
        msg = msg
        if float(current) >= float(start_price) + float(difference):
            err = True
            msg.append("Стоимость " + cur_name + " выросла больше чем на " + difference + " рублей! (" + str(
                percent) + "%)\nНовая стоимость: " + current)
        elif float(current) <= float(start_price) - float(difference):
            err = True
            msg.append("Стоимость " + cur_name + " упала больше чем на " + difference + " рублей! (" + str(
                percent) + "%)\nНовая стоимость: " + current)
        return err

    # Валюта | Триггер при изменении на 10% от изначальной стоимости
    def trgger_currency(self):
        current = self.finanz.get_currency_price()
        msg = []
        for p, d, c, n in zip(self.current_price_currency.values(), self.difference_currency.values(), current.values(),
                              current):
            err = self.check(p, d, c, n, msg, self.percent_currency)
            if err:
                self.current_price_currency[n] = c
        return msg

    # Металы | Триггер при изменении на 2.75% от изначальной стоимости
    def trgger_metals(self) -> list:
        current = self.finanz.get_metals_price()
        msg = []
        for p, d, c, n in zip(self.current_price_metals.values(), self.difference_metals.values(), current.values(),
                              current):
            err = self.check(p, d, c, n, msg, self.percent_metals)
            if err:
                self.current_price_metals[n] = c
        return msg

    # Материалы | Триггер при изменении на 4.27% от изначальной стоимости
    def trgger_materials(self) -> list:
        current = self.finanz.get_materials_price()
        msg = []
        for p, d, c, n in zip(self.current_price_materials.values(), self.difference_materials.values(),
                              current.values(), current):
            err = self.check(p, d, c, n, msg, self.percent_materials)
            if err:
                self.current_price_materials[n] = c
        return msg
