from celery.schedules import crontab
from attendance.views.attendance_calculate_view import calculate_attendance
from attendance.views.utils import calculate_attendances_daily
@app.task
def calculate_attendance_task():
    calculate_attendances_daily()
    

# Schedule the task to run at 23:50 every day
app.conf.beat_schedule = {
    'calculate_attendance': {
        'task': 'attendance.tasks.calculate_attendance_task',
        'schedule': crontab(minute=45, hour=23),
    },
}