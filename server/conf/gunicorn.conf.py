from multiprocessing import cpu_count


def max_workers():
    return cpu_count()


bind = '127.0.0.1:8000'
workers = max_workers()
user = "maxim"
timeout = 120
