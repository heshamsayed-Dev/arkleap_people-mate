# Generated by Django 4.2.2 on 2023-06-24 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("employee", "0003_remove_dependency_created_by_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("address", models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name="employee",
            name="department",
            field=models.CharField(
                choices=[("development", "development"), ("testing", "testing")], default=1, max_length=255
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="employee",
            name="position",
            field=models.CharField(
                choices=[
                    ("software_engineer", "Software engineer"),
                    ("senior_software_engineer", "senior software engineer"),
                ],
                default=1,
                max_length=255,
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="CompanyBranch",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("address", models.TextField()),
                ("company", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="employee.company")),
            ],
        ),
        migrations.AddField(
            model_name="employee",
            name="branch",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="employee.companybranch"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="employee",
            name="company",
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to="employee.company"),
            preserve_default=False,
        ),
    ]
