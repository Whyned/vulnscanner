from threading import Lock

# LOG LEVELS
LOG_INFO = 'INFO'
LOG_WARN = 'WARN'
LOG_ERROR = 'ERROR'
LOG_DEBUG = 'DEBUG'
LOG_SILLY = 'SILLY'

LOG_LEVELS_STDOUT = [LOG_INFO, LOG_ERROR, LOG_SILLY]
LOG_LEVELS_FILES = {
    'error.txt': [LOG_ERROR]
}

log_to_stdout_lock = Lock()
def log_to_stdout(str):
    """
    Acts like normal print() but thread safe
    """
    with log_to_stdout_lock: print(str)

def log_to_file(file, str):
    f = open(file, 'a')
    f.write(str+'\r\n')
    f.close()

def log_to_file_curry(file):
    return lambda str: log_to_file(file, str)

def log_compose(log_str, callables):
    for c in callables: c(log_str)

def log_concat(level, *kargs, **kwargs):
    return '%s: ' %level + \
           ' '.join(kargs) + \
           ' ' + \
           ' '.join(['%s=%s' %(k,v) for (k,v) in kwargs.items()])

def log_curry(level):
    composes = []
    if level in LOG_LEVELS_STDOUT:
        composes += [log_to_stdout]

    for file, levels in LOG_LEVELS_FILES.items():
        if level in levels:
            composes += [log_to_file_curry(file)]

    if len(composes) == 0: return lambda *kargs, **kwargs: None
    return lambda *kargs, **kwargs: \
        log_compose(log_concat(level, *kargs, **kwargs), composes)

info = log_curry(LOG_INFO)
warn = log_curry(LOG_WARN)
error = log_curry(LOG_ERROR)
debug = log_curry(LOG_DEBUG)
silly = log_curry(LOG_SILLY)
