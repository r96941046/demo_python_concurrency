from redis import Redis
from rq import Queue, Connection, Worker

REDIS_PORT = 6379

redis_connection = Redis('localhost', REDIS_PORT)

with Connection(redis_connection):
    queue = Queue('rqworker')
    worker = Worker(queue)
    worker.work()
