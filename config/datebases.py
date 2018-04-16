import sys


def get_database():
    DATABASES = {}
    # 本地远程连接
    if 'runserver' in sys.argv or 'migrate' in sys.argv or 'makemigrations' in sys.argv:
        print('使用远程数据库')
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'plover_cloud2',
                'USER': 'root',
                'PASSWORD': 'chenshun@yaolili',
                'HOST': '101.200.36.42'
            }
        }
    elif 'test' in sys.argv:
        print('使用测试数据库')
        DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'test_db'}
    else:
        print('使用本地数据库')
        # 服务器本地环境
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'plover_cloud2',
                'USER': 'root',
                'PASSWORD': 'chenshun@yaolili',
                'HOST': '127.0.0.1'
            }
        }
    return DATABASES
