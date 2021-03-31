import json
from django_celery_beat.models import PeriodicTask, IntervalSchedule

"""
This was for testing whether we are able to create periodic tasks from a pre-configured
periodic task, we would call the below function from the pre-configured periodic
task.
"""


def operation_add_factory():
    x = input("Input x: ")
    y = input("Input y: ")
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
    )
    PeriodicTask.objects.create(
        interval=schedule,
        name="Operation Addition Task",
        task="dcross_celery.tasks.operation_add",
        args=json.dumps([x, y])
    )


# operation_add_factory()
