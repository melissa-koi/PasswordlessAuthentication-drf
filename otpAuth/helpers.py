import random
from django.core.cache import cache

def create_otp( mobile, user_obj):
    if cache.get(mobile):
        return False, cache.ttl(mobile)
    try:
        otp_to_send = random.randint(1000, 9999)
        cache.set(mobile, otp_to_send, timeout=1)
        user_obj.otp = otp_to_send
        user_obj.save()
        return True, 0
    except Exception as e:
        print('exception2 here!')
        print(e)

