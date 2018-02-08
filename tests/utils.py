def assertRaises(exception, callable, *kargs, **kwargs):
    assertRaisesMessage(exception, None, callable, *kargs, **kwargs)

def assertRaisesMessage(exception, message, callable, *kargs, **kwargs):
    threw_error = False

    try:
        callable(*kargs, **kwargs)
    except exception as e:
        e = str(e)
        if message is not None and e != message:
            raise AssertionError('Excepted thrown error to be: \r\n %s \r\n but was: \r\n %s' %(message, e    ))
        threw_error = True

    if threw_error is False:
        raise AssertionError('Expected %s() to throw Error %s'
            %(callable.__name__, exception.__name__))
