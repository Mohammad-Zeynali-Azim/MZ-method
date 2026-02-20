# -------------------------------------------------------------Vectorized Fastest way to MZ-Method_Using List
import time
import numpy as np


def vectorized(s):
    arr = np.frombuffer(s.encode(), dtype=np.uint8) - 48
    first_digit = arr[0] >> 1
    if len(arr) < 2:
        return []
    prev_parity = arr[:-1] & 1
    if first_digit > 0:
        return np.concatenate(([first_digit], (prev_parity * 5 + (arr[1:] >> 1)).tolist()))
    else:
        return (prev_parity * 5 + (arr[1:] >> 1)).tolist()

def read_number():
        s=input("Plase Enter Your  Number For Dividing by Two:")
        et =int(input("Plase Enter Eteration:"))

        s = '1' + '0' * 999999999  # وقتی خواستی تست بزرگ
        #s='1380275369'
        # s='11111'
        print(f"طول ورودی: {len(s):,} رقم")

        k = []
        start_time = time.perf_counter_ns()

        k = vectorized(s)
        #    print(value, end=" ")
        #   count += 1
        # print(k)
        # print(result)  # خط جدید بعد از اعداد

        time_ms = (time.perf_counter_ns() - start_time) / 1_000_000

        # print(f"\nتعداد مقادیر: {count:,}")
        print(f"زمان کل: {time_ms:,.9f} میلی‌ثانیه")
read_number()