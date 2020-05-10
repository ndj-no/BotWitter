from my_models.coupon import Coupon
from my_web_setting import my_web_url

url = my_web_url.MyWebApi.get_all_coupons_available()
print(url.status_code)
coupons = []
for coupon in url.json():
    c = Coupon(coupon)
    coupons.append(Coupon(coupon))
    print(c)
