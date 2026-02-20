import time
import numpy as np


def div2_carry_numpy(s: str) -> str:
    if not s or s == '0':
        return '0'

    arr = np.frombuffer(s.encode('ascii'), dtype=np.uint8) - 48
    n = len(arr)

    result = np.zeros(n, dtype=np.uint8)
    carry = 0

    for i in range(n):
        current = carry * 10 + arr[i]
        result[i] = current >> 1
        carry = current & 1

    # حذف صفرهای ابتدایی
    first = np.argmax(result != 0)
    if first == 0 and result[0] == 0:
        return '0'

    return ''.join(map(str, result[first:]))


s = '1' + '0' * 9999999  # وقتی خواستی تست بزرگ
# s='123456789987654321'
print(f"طول ورودی: {len(s):,} رقم")

k = []
start_time = time.perf_counter_ns()

k = div2_carry_numpy(s)
#    print(value, end=" ")
#   count += 1
# print(k)
# print(result)  # خط جدید بعد از اعداد

time_ms = (time.perf_counter_ns() - start_time) / 1_000_000

# print(f"\nتعداد مقادیر: {count:,}")
print(f"زمان کل: {time_ms:,.9f} میلی‌ثانیه")