#!/bin/env/python

from carota import carota
import argparse
import time
from functools import wraps
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

    
# Arguments
ENCLOSER = ''
DELIMITER = ','
ROWS = 10
TEXT = 'index; uuid::seed=0; firstname::seed=0; lastname::seed=0; int::start=18,end=95,seed=0; date::delta=365,seed=0'
# TEXT = 'uuid::seed=0; uuid::seed=1; uuid::seed=10'
OUTPUT = ''
CHUNK_SIZE = 1000000


def timeit(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        print(f"{method.__name__} => {time.time() - start_time:.2f}s")

        return result

    return wrapper


def getArgs():
    """ Get command line args """
    parser = argparse.ArgumentParser(description='Generate data')
    parser.add_argument("-r", "--rows", dest='ROWS',
                        default=ROWS, help='Number of rows, default <' + str(ROWS) + '>')
    parser.add_argument("-t", "--text", dest='TEXT',
                        default=TEXT, help='Text, default <' + TEXT + '>')
    parser.add_argument("-d", "--delimiter", dest='DELIMITER',
                        default=DELIMITER, help='Delimiter, default <' + DELIMITER + '>')
    parser.add_argument("-e", "--encloser", dest='ENCLOSER',
                        default=ENCLOSER, help='Encloser, default <' + ENCLOSER + '>')
    parser.add_argument("-o", "--output", dest='OUTPUT',
                        default=OUTPUT, help='output filepath, default =  STDOUT')
    parser.add_argument("-c", "--chunck-size", dest='CHUNK_SIZE',
                        default=CHUNK_SIZE, help='count of rows to write to file at a time, default <' + str(CHUNK_SIZE) + '>'),
    parser.add_argument("--append", action='store_true', help='Whether to append to the output file.')                    
    return parser.parse_args()


@timeit
def writedown(l, path):
    with open(path, 'a') as f:
        f.write('\n'.join(l) + '\n')

@timeit
def main():
    options = getArgs()

    # trick to allow passing tab as a delimiter   
    options.DELIMITER = '\t' if options.DELIMITER == '\\t' else options.DELIMITER

    iterator = carota(rows = int(options.ROWS), 
                        text = options.TEXT, 
                        delimiter = options.DELIMITER, 
                        encloser = options.ENCLOSER)
    

    l = []
    hasMore = True
    sum = 0

    if options.OUTPUT == '':
        for v in iterator:
            print(v)
    else:
        # create/override file
        if not options.append:
            with open(options.OUTPUT, 'w') as f:
                pass

        while hasMore:
            for i in range(int(options.CHUNK_SIZE)):
                try:
                    l.append(next(iterator))
                    
                except StopIteration:
                    hasMore = False
                    break
            
            writedown(l, options.OUTPUT)
            # with open(options.OUTPUT, 'a') as f:
            #     f.write('\n'.join(l) + '\n')

            sum = sum + i + 1
            print("written lines: " + str(sum))
            l=[]

            
if __name__ == "__main__":
    main()
