# -------------------------------------------------------------Vectorized Fastest way to MZ-Method_Using Array

import numpy as np
import time


def vectorized_fast(arr, length):
    if length < 2:
        return 0
    # parity ارقام قبلی
    prev_parity = arr[:-1] & 1

    # بخش اصلی MZ
    arr[1:length] = (prev_parity * 5) + (arr[1:length] >> 1)

    # رقم اول
    first = arr[0] >> 1
    if first > 0:
        arr[0] = first
        return length
    else:
        # شیفت به چپ (حذف صفر اول)
        arr[:length - 1] = arr[1:length]
        return length - 1


# ---------------------------------------------------------------------
def read_number():
    # s = '10203040'
    s = input("Enter string same as : '1' + '0' * 9999999")
    s = '1' + '0' * 9999999  # وقتی خواستی تست بزرگ
    # s = '11111'
    print(f"طول ورودی: {len(s):,} رقم")

    start_time = time.perf_counter_ns()

    arr = np.frombuffer(s.encode(), dtype=np.uint8) - 48
    for i in range(1, 1000):
        length = len(arr)
        length = vectorized_fast(arr, length)
    # print(arr[:length])

    # print("--------------------------------------------------------------")
    # length = len(arr)
    # length = vectorized_fast(arr, length)
    # print(arr[:length])
    time_ms = (time.perf_counter_ns() - start_time) / 1_000_000
    print(f"زمان کل: {time_ms:,.9f} میلی‌ثانیه")


read_number()