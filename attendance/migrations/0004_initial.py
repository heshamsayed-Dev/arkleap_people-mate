# Generated by Django 4.2.2 on 2023-07-05 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("attendance", "0003_remove_attendancedetail_attendance_delete_attendance_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attendance",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("employee", models.CharField(max_length=255)),
                ("date", models.DateField()),
                ("check_in", models.DateTimeField()),
                ("check_out", models.DateTimeField()),
                ("worked_hours", models.FloatField()),
                ("default_check_in", models.FloatField()),
                ("default_check_out", models.FloatField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="AttendanceDetail",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("branch", models.CharField(max_length=255)),
                ("check_in", models.DateTimeField()),
                ("check_out", models.DateTimeField()),
                (
                    "attendance",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attendance_details",
                        to="attendance.attendance",
                    ),
                ),
            ],
        ),
    ]
