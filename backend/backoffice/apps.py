from django.contrib.admin.apps import AdminConfig


class AdminConfig(AdminConfig):
    default_site = "backoffice.admin.AdminSite"
