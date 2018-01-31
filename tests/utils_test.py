def assertRaises(exception, callable, *kargs, **kwargs):
    threw_error = False
    try:
        callable(*kargs, **kwargs)
    except exception:
        threw_error = True

    if threw_error is False:
        raise AssertionError('Expected %s() to throw %s'
            %(callable.__name__, exception.__name__))
