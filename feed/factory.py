import json
from django_celery_beat.models import PeriodicTask, IntervalSchedule


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


operation_add_factory()
