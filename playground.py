from __future__ import print_function
from hello import tasks
from datetime import datetime, timedelta
from celery import chain
from contexttimer import Timer

while True:
    print('r - retrier; retries self with 1 second delay')
    print('s - Simple task, logs one line of text and returns text')
    print('p - simple task with eta in the past')
    print('f - flood with retriers')
    taskspec = raw_input('What task do you want to queue? [s] ')
    if taskspec.lower().startswith('r'):
        print('queueing retrier')
        tasks.retrier.apply_async(countdown=2)
    elif taskspec.lower().startswith('p'):
        print('queueing past simple')
        dt = datetime.utcnow() - timedelta(minutes=30)
        tasks.simple.apply_async(args=['past'], eta=dt)
    elif taskspec.lower().startswith('f'):
        print('queuing 1000 retriers')
        for x in xrange(0, 1000):
            tasks.retrier.apply_async(args=['flood'], countdown=2)
    elif taskspec.lower().startswith('c'):
        print('queuing 100 chain of simples')
        for upper in xrange(155, 155):
            subtasks = []
            for x in xrange(0, upper):
                task = tasks.simple.si('chain {}'.format(upper))
                task.set(countdown=1)
                subtasks.append(task)
            chain(subtasks).delay()
    else:
        print('waiting for simple')
        result = tasks.simple.apply_async(countdown=0)
        with Timer() as t:
            print(result.get())
        print(t.elapsed)
