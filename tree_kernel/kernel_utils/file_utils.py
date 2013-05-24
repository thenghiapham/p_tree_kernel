'''
Created on May 24, 2013

@author: thenghiapham
'''

def open_all_files(files, mode):
    streams = []
    for file_path in files:
        stream = open(file_path, mode)
        streams.append(stream)
    return streams

def close_all_files(streams):
    for stream in streams:
        stream.close()
        
def flush_all_files(streams):
    for stream in streams:
        stream.flush()