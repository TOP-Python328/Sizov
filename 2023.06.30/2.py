from time import sleep

def exception_delay_repeat(function):
    """Спустя полсекунды повторяет вызов декорируемой функции в случае возникновения исключения."""
    def wrapper(*args, **kwargs):
        try:
            result = function(*args, **kwargs)
        except:
            sleep(0.5)
            try:
                result = function(*args, **kwargs)
            except Exception as exception:
                print(f'{exception.__class__.__name__}: {exception}')
                result = None
        return result
    return wrapper
    
# >>> from random import randrange
# >>> def test_func():
# ...     if randrange(2):
# ...             raise ConnectionError('failure')
# ...     else:
# ...             return 'success'
# ...
# >>> test_func
# <function test_func at 0x0000020FC1223240>
# >>>
# >>> test_func = exception_delay_repeat(test_func)
# >>> test_func
# <function exception_delay_repeat.<locals>.wrapper at 0x0000020FC1290220>
# >>>
# >>> test_func()
# 'success'
# >>> test_func()
# 'success'
# >>> test_func()
# ConnectionError: failure    