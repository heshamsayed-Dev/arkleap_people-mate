# Generated by Django 4.2.2 on 2023-06-22 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Employee",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=60, verbose_name="Employee Name")),
                ("number", models.CharField(max_length=10, verbose_name="Employee Code")),
                ("birth_date", models.DateField(verbose_name="Birth Date")),
                ("email", models.CharField(max_length=20, verbose_name="Email")),
                (
                    "gender",
                    models.CharField(choices=[("M", "Male"), ("F", "Female")], max_length=6, verbose_name="Gender"),
                ),
                ("picture", models.FileField(upload_to="employee_pictures/", verbose_name="Picture")),
                ("hire_date", models.DateField(verbose_name="Hire Date")),
                ("termination_date", models.DateField(verbose_name="Termination Date")),
                ("address_1", models.CharField(max_length=120, verbose_name="Address 1")),
                ("address_2", models.CharField(max_length=120, verbose_name="Address 2")),
                ("phone", models.IntegerField(verbose_name="Phone")),
                ("mobile", models.IntegerField(verbose_name="Mobile")),
                ("birth_place", models.CharField(max_length=120, verbose_name="Place of Birth")),
                ("nationality", models.CharField(max_length=15, verbose_name="Nationality")),
                ("id_type", models.CharField(max_length=15, verbose_name="ID Type")),
                ("id_number", models.CharField(max_length=15, verbose_name="ID Number")),
                ("has_medical", models.BooleanField(verbose_name="Has Medical")),
                ("has_insurance", models.BooleanField(verbose_name="Has Insurance")),
                ("medical_start_date", models.DateField(verbose_name="Medical Start Date")),
                ("medical_end_date", models.DateField(verbose_name="Medical End Date")),
                ("medical_number", models.CharField(max_length=30, verbose_name="Medical Number")),
                ("insurance_date", models.DateField(verbose_name="Insurance Date")),
                ("insurance_number", models.CharField(max_length=30, verbose_name="Insurance Number")),
                ("insurance_salary", models.FloatField(verbose_name="Insurance Salary")),
                ("retirement_insurance_salary", models.FloatField(verbose_name="Retirement Insurance Salary")),
                (
                    "social_status",
                    models.CharField(
                        choices=[
                            ("single", "Single"),
                            ("married", "Married"),
                            ("engaged", "Engaged"),
                            ("divorced", "Divorced"),
                            ("widowed", "Widowed"),
                        ],
                        max_length=10,
                        verbose_name="Social Status",
                    ),
                ),
                (
                    "military_status",
                    models.CharField(
                        choices=[("finished", "Finished"), ("exempted", "Exempted"), ("postponed", "Postponed")],
                        max_length=12,
                        verbose_name="Military Status",
                    ),
                ),
                (
                    "religion",
                    models.CharField(choices=[("muslim", "Muslim"), ("christian", "Christian")], max_length=10),
                ),
                ("study_field", models.CharField(max_length=15, verbose_name="Field Of Study")),
                (
                    "education_degree",
                    models.CharField(
                        choices=[("bachelor", "Bachelor"), ("diploma", "Diploma"), ("masters", "Masters")],
                        max_length=12,
                    ),
                ),
                ("is_active", models.BooleanField(verbose_name="Is Active ")),
                (
                    "manager",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="employees", to="employee.employee"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EmployeeAttachment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=60, verbose_name="Name")),
                ("category", models.CharField(verbose_name="Category")),
                ("expiration_date", models.DateField()),
                ("attachment", models.FileField(upload_to="employee_attachments/")),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="attachments", to="employee.employee"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Dependency",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=60, verbose_name="Name")),
                ("mobile", models.IntegerField(verbose_name="Mobile")),
                (
                    "relation",
                    models.CharField(
                        choices=[("parent", "Parent"), ("child", "Child"), ("wife", "Wife")],
                        max_length=8,
                        verbose_name="Relation",
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dependencies",
                        to="employee.employee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Contract",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("department", models.CharField(max_length=30, verbose_name="Department relation")),
                ("salary_structure", models.CharField(max_length=30, verbose_name="Salary Structure relation")),
                (
                    "employee_type",
                    models.CharField(
                        choices=[("full_time", "Full Time"), ("part_time", "Part Time")],
                        max_length=10,
                        verbose_name="Employee Type",
                    ),
                ),
                ("position", models.CharField(max_length=30, verbose_name="Position")),
                ("contract_type", models.CharField(max_length=30, verbose_name="Contract Type")),
                ("start_date", models.DateField(verbose_name="Start Date")),
                ("end_date", models.DateField(verbose_name="End Date")),
                ("payment_type", models.CharField(verbose_name="Payment Relation")),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="contracts", to="employee.employee"
                    ),
                ),
            ],
        ),
    ]
