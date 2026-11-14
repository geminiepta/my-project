import datetime
import os

# ------------------------------
# Класс кондиционера
# ------------------------------
class AirConditioner:
    def __init__(self):
        self.power = False          # включен/выключен
        self.mode = "Охлаждение"    # текущий режим
        self.setpoint = 24.0        # уставка температуры
        self.sleep = False
        self.turbo = False
        self.eco = False

    def toggle_power(self, on):
        self.power = on
        return f"Кондиционер {'ВКЛЮЧЕН' if on else 'ВЫКЛЮЧЕН'}"

    def set_mode(self, mode):
        if not self.power:
            return "Ошибка: кондиционер выключен"
        self.mode = mode
        return f"Режим установлен: {mode}"

    def change_temp(self, delta):
        if not self.power:
            return "Ошибка: кондиционер выключен"
        new_temp = self.setpoint + delta
        # Ограничение по ТЗ: -50…+50 °C (для уставки возьмём разумные 16…30)
        if new_temp < 16:
            return "Минимальная уставка: 16 °C"
        if new_temp > 30:
            return "Максимальная уставка: 30 °C"
        self.setpoint = new_temp
        return f"Уставка: {self.setpoint:.1f} °C"

    def toggle_function(self, func):
        if not self.power:
            return "Ошибка: кондиционер выключен"
        if func == "sleep":
            self.sleep = not self.sleep
            return f"Sleep: {'ВКЛ' if self.sleep else 'ВЫКЛ'}"
        elif func == "turbo":
            self.turbo = not self.turbo
            return f"Turbo: {'ВКЛ' if self.turbo else 'ВЫКЛ'}"
        elif func == "eco":
            self.eco = not self.eco
            return f"ECO: {'ВКЛ' if self.eco else 'ВЫКЛ'}"

    def get_status(self):
        status = [
            f"Питание: {'ВКЛ' if self.power else 'ВЫКЛ'}",
            f"Режим: {self.mode}",
            f"Уставка: {self.setpoint:.1f} °C",
            f"Sleep: {'ВКЛ' if self.sleep else 'ВЫКЛ'}",
            f"Turbo: {'ВКЛ' if self.turbo else 'ВЫКЛ'}",
            f"ECO: {'ВКЛ' if self.eco else 'ВЫКЛ'}",
        ]
        return "\n".join(status)


# ------------------------------
# Логирование
# ------------------------------
LOG_FILE = "ac_history.log"

def log_action(action):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {action}\n")

# ------------------------------
# Вывод справки
# ------------------------------
def show_help():
    print("""
Доступные команды:
  0  — выключить кондиционер
  1  — включить кондиционер
  +  — увеличить уставку на 0.5 °C
  -  — уменьшить уставку на 0.5 °C
  2  — режим «Охлаждение»
  3  — режим «Нагрев»
  4  — режим «Вентиляция»
  5  — режим «Осушение»
  6  — функция «Sleep»
  7  — функция «Turbo»
  8  — функция «ECO»
  s  — показать состояние
  h  — справка
  q  — выход
""")

# ------------------------------
# Основная программа
# ------------------------------
def main():
    ac = AirConditioner()
    print("=== Система управления кондиционером ===")
    show_help()
    log_action("Запуск программы")

    while True:
        try:
            cmd = input("\nВведите команду: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            log_action("Принудительный выход")
            break

        if cmd == "q":
            print("Выход из программы.")
            log_action("Выход из программы")
            break

        result = ""
        if cmd == "0":
            result = ac.toggle_power(False)
        elif cmd == "1":
            result = ac.toggle_power(True)
        elif cmd == "+":
            result = ac.change_temp(0.5)
        elif cmd == "-":
            result = ac.change_temp(-0.5)
        elif cmd == "2":
            result = ac.set_mode("Охлаждение")
        elif cmd == "3":
            result = ac.set_mode("Нагрев")
        elif cmd == "4":
            result = ac.set_mode("Вентиляция")
        elif cmd == "5":
            result = ac.set_mode("Осушение")
        elif cmd == "6":
            result = ac.toggle_function("sleep")
        elif cmd == "7":
            result = ac.toggle_function("turbo")
        elif cmd == "8":
            result = ac.toggle_function("eco")
        elif cmd == "s":
            result = "\n" + ac.get_status()
        elif cmd == "h":
            show_help()
            log_action("Запрошена справка")
            continue
        else:
            print("Неизвестная команда. Введите h для справки.")
            log_action(f"Неизвестная команда: {cmd}")
            continue

        print(result)
        log_action(f"Команда '{cmd}' -> {result.strip()}")

if __name__ == "__main__":
    main()
