import datetime
import hashlib
import random
import string
import uuid


def get_token(user_name):
    now_time = datetime.datetime.now()
    now_time_1 = now_time + datetime.timedelta(days=1)
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    md = hashlib.md5()
    md.update(str(salt + user_name + str(now_time)).encode('utf8'))
    return md.hexdigest() + str(now_time_1)


if __name__ == '__main__':
    print(uuid.uuid3(uuid.NAMESPACE_URL, "1"))
    print(uuid.uuid3(uuid.NAMESPACE_URL, "1"))
    print(uuid.uuid3(uuid.NAMESPACE_URL, "2"))
