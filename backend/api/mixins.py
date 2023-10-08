from rest_framework import permissions

from .permissions import IsNWAdminPermissions, IsAuditorPermissions, IsUserPermissions

class NWAdminPermissionMixin():
    permission_classes = [
        permissions.IsAdminUser,
        IsNWAdminPermissions
        ]
    
class AuditorPermissionMixin():
    permission_classes = [
        IsAuditorPermissions
        ]
    
class UserPermissionMixin():
    permission_classes = [
        IsUserPermissions
        ]