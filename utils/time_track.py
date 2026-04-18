import time
from functools import partial


def base_time_desc_decorator(method, desc='test_description'):
    def timed(*args, **kwargs):
        print(desc)
        start = time.time()
        try:
            result = method(*args, **kwargs)
        except TypeError:
            result = method(**kwargs)
        print('Done! It took {:.2} secs\n'.format(time.time() - start))
        if result is not None:
            return result
    return timed

def time_desc_decorator(desc):
    return partial(base_time_desc_decorator, desc=desc)
