import redis
from os import environ



class REDISManager:
    def __init__(self):
        self.redis = None
        self.init()

    def init(self):
        self.redis = redis.Redis(
            host=environ.get('REDIS_HOST'),
            port=environ.get('REDIS_PORT'),
            password=environ.get('REDIS_PWD')
        )

    def test(self):
        self.redis.set('foo','bar')
        print(self.redis.get('asdf'))

    def checkUsage(self):
        return self.redis.dbsize()

    """
    :return None, res
    """

    def get_from_redis(self, id):
        res = self.redis.get(str(id))
        if res:
            return res.decode()
        return None

    def add_to_redis(self, id, longURL):
        self.redis.set(str(id), longURL)


if __name__ == '__main__':
    r = REDISManager()
    r.checkUsage()
    #print(r.checkUsage())
