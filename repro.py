import time
import tasks
from celery.exceptions import TimeoutError
from celery import chain

from subprocess import call, Popen

if __name__ == '__main__':
    call('celery -A tasks:app purge -f', shell=True)
    worker = Popen('celery -A tasks:app worker', shell=True)

    # Wait for worker to open up
    time.sleep(3)
    subtasks = []
    upper = 100
    for x in xrange(0, upper):
        task = tasks.simple.si('chain {}'.format(upper))
        task.set(countdown=1)
        subtasks.append(task)
    chain(subtasks).delay()

    result = tasks.simple.delay('unchained')
    try:
        result.get(timeout=5)
    except TimeoutError:
        print("first simple task timed out!")
    else:
        print("first simple task succeeded!")

    for i in xrange(0, 10):
        upper = 200
        subtasks = []
        for x in xrange(0, upper):
            task = tasks.simple.si('chain {}'.format(upper))
            task.set(countdown=1)
            subtasks.append(task)
        chain(subtasks).delay()

    # Wait a few seconds for those tasks to be received
    time.sleep(2)
    result = tasks.simple.delay('unchained')
    try:
        result.get(timeout=5)
    except TimeoutError:
        print("second simple task timed out!")
    else:
        print("second simple task succeeded!")

    worker.terminate()
