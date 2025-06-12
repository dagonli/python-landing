import logging
import contextvars
import uuid
import inspect
import sys
class CustomHandler(logging.StreamHandler):
    def emit(self, record):
        if record.levelno < logging.WARNING:
            self.stream = sys.stdout
        else:
            self.stream = sys.stderr
        super().emit(record)

# logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = CustomHandler()
formatter = logging.Formatter(
    fmt='%(asctime)s.%(msecs)03d %(levelname)s [%(processName)s-%(process)d] [req:%(request_id)s|rip:%(remote_ip)s|channel:%(user_no)s] [%(file_name)s %(func_name)s %(line_number)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
ch.setFormatter(formatter)
logger.addHandler(ch)


log_extra = contextvars.ContextVar('correlation_id', default=None)


def log_start(func):
    def wrap(*args, **kwargs):
        request_id = str(uuid.uuid4()).replace('-', '')
        token = log_extra.set(dict(request_id=request_id))
        try:
            return func(*args, **kwargs)
        finally:
            log_extra.reset(token)

    async def wrapAsync(*args, **kwargs):
        request_id = str(uuid.uuid4()).replace('-', '')
        token = log_extra.set(dict(request_id=request_id))
        try:
            return await func(*args, **kwargs)
        finally:
            log_extra.reset(token)

    if inspect.iscoroutinefunction(func):
        return wrapAsync
    return wrap


def _log(k, msg, *args, **extra):
    if len(msg) > 3000:
        msg = msg[:1500] + ' ... ' + msg[-1500:]
    d = log_extra.get() or {}

    # 获取调用栈信息
    caller = inspect.currentframe().f_back.f_back
    func_name = caller.f_code.co_name
    file_name = caller.f_code.co_filename
    line_number = caller.f_lineno

    getattr(logger, k)(msg, *args, extra={
        **d,
        'request_id': extra.get('request_id', d.get('request_id')) or '-',
        'remote_ip': extra.get('remote_ip', d.get('remote_ip')) or '-',
        'user_no': extra.get('user_no', d.get('user_no')) or '-',
        'class_name': extra.get('class_name', d.get('class_name')) or '-',
        'func_name': func_name,
        'file_name': file_name,
        'line_number': line_number,
        **extra
    })


def log(msg, *args, **extra):
    _log('info', msg, *args, **extra)


def debug(msg, *args, **extra):
    _log('debug', msg, *args, **extra)


def warn(msg, *args, **extra):
    _log('warn', msg, *args, **extra)

def error(msg, *args, **extra):
    _log('error', msg, *args, **extra)
