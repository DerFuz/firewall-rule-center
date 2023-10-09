from rest_framework import permissions

from .permissions import RulePermissions

class RulePermissionMixin():
    permission_classes = [RulePermissions]