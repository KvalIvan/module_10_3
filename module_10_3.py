import threading
import time
from random import randint


class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        c_b = 0
        for dep in range(100):
            c_b += 1
            ran_cash = randint(50, 500)
            self.balance = self.balance + ran_cash
            print(f'Номер пополнения: {c_b} Пополнение: {ran_cash}. Баланс: {self.balance}')
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            time.sleep(0.001)

    def take(self):
        t_c = 0
        for take_ in range(100):
            t_c += 1
            take_cash = randint(50, 500)
            print(f'Запрос на {take_cash} №{t_c}')
            if take_cash <= self.balance:
                self.balance = self.balance - take_cash
                print(f'Снятие: {take_cash}. Баланс: {self.balance}')
            else:
                print('Запрос отклонён, недостаточно средств')
                self.lock.acquire()


bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
