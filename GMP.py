import gmpy2
import time
def GMP2():
        s=input("Plase Enter Your Number For /2 Same as ('1' + '0' * 9999999):")
        et =int(input("Plase Enter Eteration:"))
        s = '1' + '0' * 9999999
        # s = '10203040'          # برای تست سریع و کوچک

        print(f"طول رشته ورودی: {len(s):,}")

        t0 = time.perf_counter()

        # تبدیل رشته به mpz (عدد صحیح با دقت دلخواه)
        n = gmpy2.mpz(s)

        t1 = time.perf_counter()

        print("\nانجام ۱۰۰ بار تقسیم متوالی بر ۲ (شیفت راست):\n")

        current = n
        div_count = 0

        for i in range(1, et+1):
                current = current >> 1  # شیفت راست - سریع‌ترین روش تقسیم بر ۲
                # current = current // 2        # روش جایگزین (کمی کندتر)

                div_count += 1

        t2 = time.perf_counter()

        print("\n" + "─" * 70)
        print(f"زمان تبدیل رشته به mpz    : {t1 - t0:8.3f} ثانیه")
        print(f"زمان {div_count} بار تقسیم بر ۲     : {t2 - t1:8.3f} ثانیه")
        print(f"زمان کل عملیات              : {t2 - t0:8.3f} ثانیه")