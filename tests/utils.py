def assertRaises(exception, callable, *kargs, **kwargs):
    assertRaisesMessage(exception, None, callable, *kargs, **kwargs)

def assertRaisesMessage(exception, message, callable, *kargs, **kwargs):
    threw_error = False

    try:
        callable(*kargs, **kwargs)
    except exception as e:
        if message is not None:
            assert str(e) == message
        threw_error = True

    if threw_error is False:
        raise AssertionError('Expected %s() to throw %s'
            %(callable.__name__, exception.__name__))
