import redis

pool = redis.ConnectionPool(host='192.168.134.128', port=6379, password='kevin')
r = redis.Redis(connection_pool=pool)
pipe = r.pipeline(transaction=True)
pipe.set('name', 'kevin')
pipe.set('role', 'boss')
pipe.execute()
