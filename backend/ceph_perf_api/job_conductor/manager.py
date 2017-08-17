import time


class Manager(object):
    def example_job(self, ctxt, body):
        print "run example, body:", body
        time.sleep(10)
        print "done!"
