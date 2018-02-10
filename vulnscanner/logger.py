from threading import Lock

# LOG LEVELS
LOG_INFO = 'INFO'
LOG_WARN = 'WARN'
LOG_ERROR = 'ERROR'
LOG_DEBUG = 'DEBUG'
LOG_SILLY = 'SILLY'
LOG_RESULT = 'RESULT'
_LOG_ALL = [LOG_INFO, LOG_WARN, LOG_ERROR, LOG_DEBUG, LOG_SILLY, LOG_RESULT]
_LOG_ERROR_AND_WARN = [LOG_ERROR, LOG_WARN]

LOG_LEVELS_STDOUT = _LOG_ERROR_AND_WARN
LOG_LEVELS_FILES = {
    'error.txt': [LOG_ERROR],
    #'debug.txt': [LOG_INFO, LOG_WARN, LOG_ERROR, LOG_DEBUG, LOG_SILLY]
}

write_to_stdout_lock = Lock()
def write_to_stdout(str):
    """
    Acts like normal print() but thread safe
    """
    with write_to_stdout_lock: print(str)

def append_to_file(file, str):
    f = open(file, 'a')
    f.write(str+'\r\n')
    f.close()

def append_to_file_curry(file):
    return lambda str: append_to_file(file, str)

def log_concat(level, *kargs, **kwargs):
    return '%s: ' %level + \
           ' '.join(kargs) + \
           ' ' + \
           ' '.join(['%s=%s' %(k,v) for (k,v) in kwargs.items()])

def log_curry(level):
    composes = []
    if level in LOG_LEVELS_STDOUT:
        composes += [write_to_stdout]

    for file, levels in LOG_LEVELS_FILES.items():
        if level in levels:
            composes += [append_to_file_curry(file)]

    def composer(*kargs, **kwargs):
        lc = log_concat(level, *kargs, **kwargs)
        for c in composes:
            c(lc)

    return composer

_LOG_RESULT_TO_STDOUT = None
def log_result(worker_name, type, file, str):
    if _LOG_RESULT_TO_STDOUT is True:
        write_to_stdout('RESULT: [%s]{%s} %s' %(worker_name, type, str))
    append_to_file(file, str)

def raiser_not_attached_yet(*kargs, **kwargs):
    raise Exception('Logger not attached yet. Please first call #attach()')
    sys.exit(0)

info = warn = error = debug = silly = result = raiser_not_attached_yet

def attach():
    global info, warn, error, debug, silly, result, _LOG_RESULT_TO_STDOUT
    info = log_curry(LOG_INFO)
    warn = log_curry(LOG_WARN)
    error = log_curry(LOG_ERROR)
    debug = log_curry(LOG_DEBUG)
    silly = log_curry(LOG_SILLY)
    _LOG_RESULT_TO_STDOUT = LOG_RESULT in LOG_LEVELS_STDOUT
    result = log_result
