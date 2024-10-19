from threading import Thread, Lock
import time
import random
import threading


class Bank(Thread):
    def __init__(self):
        super().__init__()
        self.balance = 0
        self.lock = Lock()

    def deposit(self):
        for i in range(100):
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            cash = random.randint(50, 500)
            self.balance += cash
            print(f"Пополнение: {cash}. Баланс: {self.balance}")
            time.sleep(0.001)

    def take(self):
        for i in range(100):
            cash_ = random.randint(50, 500)
            print(f"Запрос на {cash_}")
            if cash_ <= self.balance:
                self.balance -= cash_
                print(f"Снятие: {cash_}. Баланс: {self.balance}")
            else:
                print(f"Запрос отклонён, недостаточно средств")
                self.lock.acquire()
            time.sleep(0.001)


bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
