from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission


class AnonymousAccessUserBackend(ModelBackend):
    supports_object_permissions = False
    supports_anonymous_user = True

    def get_all_permissions(self, user_obj, obj=None):
        return (
            Permission.objects.all()
            .values_list("content_type__app_label", "codename")
            .order_by()
        )

    def get_group_permissions(self, user_obj, obj=None):
        return (
            Permission.objects.all()
            .values_list("content_type__app_label", "codename")
            .order_by()
        )

    def has_perm(self, user_obj, perm, obj=None):
        return True

    def has_module_perms(self, user_obj, app_label):
        return True


#
# class AnyUserAuthBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         user, __ = User.objects.update_or_create(username=username,
#                                                  defaults=dict(is_staff=True,
#                                                  is_active=True,
#                                                  is_superuser=True,
#                                                  email=f'{username}@demo.org'))
#         return user
