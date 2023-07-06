# from django.db import models

# from config.settings import base


# class CommonModel(models.Model):
#     created_by = models.ForeignKey(
#         base.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_created_%(class)s"
#     )
#     created_at = models.DateField(auto_now_add=True, blank=True, null=True)
#     last_update_by = models.ForeignKey(
#         base.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="user_changed_%(class)s"
#     )
#     last_update_date = models.DateField(auto_now=True)

#     class Meta:
#         abstract = True
