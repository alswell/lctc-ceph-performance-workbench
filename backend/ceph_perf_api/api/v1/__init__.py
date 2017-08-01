import os


path = os.path.dirname(__file__)
for parent, dirnames, filenames in os.walk(path):
    for filename in filenames:
        filename = filename.split('.')
        if filename[1] == 'py' and filename[0] != '__init__' and filename[0] != 'urls':
            __import__('api.%s.%s' % (os.path.basename(parent), filename[0]))
    break


