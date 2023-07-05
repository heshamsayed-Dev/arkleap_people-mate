# Generated by Django 4.2.2 on 2023-06-22 09:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("employee", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="contract",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="contract",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="created_contracts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contract",
            name="updated_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="contract",
            name="updated_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="updated_contracts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="dependency",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="dependency",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="created_employee_dependencies",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="dependency",
            name="updated_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="dependency",
            name="updated_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="updated_employee_dependencies",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="employee",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="employee",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="created_employees",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="employee",
            name="updated_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="employee",
            name="updated_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="updated_employees",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="employeeattachment",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="employeeattachment",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="created_employee_attachments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="employeeattachment",
            name="updated_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="employeeattachment",
            name="updated_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="updated_employee_attachments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="insurance_date",
            field=models.DateField(null=True, verbose_name="Insurance Date"),
        ),
        migrations.AlterField(
            model_name="employee",
            name="insurance_number",
            field=models.CharField(max_length=30, null=True, verbose_name="Insurance Number"),
        ),
        migrations.AlterField(
            model_name="employee",
            name="insurance_salary",
            field=models.FloatField(null=True, verbose_name="Insurance Salary"),
        ),
        migrations.AlterField(
            model_name="employee",
            name="manager",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="employees",
                to="employee.employee",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="medical_end_date",
            field=models.DateField(null=True, verbose_name="Medical End Date"),
        ),
        migrations.AlterField(
            model_name="employee",
            name="medical_number",
            field=models.CharField(max_length=30, null=True, verbose_name="Medical Number"),
        ),
        migrations.AlterField(
            model_name="employee",
            name="medical_start_date",
            field=models.DateField(null=True, verbose_name="Medical Start Date"),
        ),
        migrations.AlterField(
            model_name="employee",
            name="phone",
            field=models.IntegerField(null=True, verbose_name="Phone"),
        ),
        migrations.AlterField(
            model_name="employee",
            name="retirement_insurance_salary",
            field=models.FloatField(null=True, verbose_name="Retirement Insurance Salary"),
        ),
        migrations.AlterField(
            model_name="employee",
            name="termination_date",
            field=models.DateField(null=True, verbose_name="Termination Date"),
        ),
    ]
