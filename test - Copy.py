import logging
LOG_FILENAME = f'logging_example.out'
logging.basicConfig(filename=LOG_FILENAME ,level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
input()
f = open(LOG_FILENAME, 'rt')
try:
    body = f.read()
finally:
    f.close()

print('FILE:')
print (body)