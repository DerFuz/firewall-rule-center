from .permissions import (
    RulePermissions, 
    RuleSetRequestPermissions, 
    FirewallPermissions, 
    UserPermissions
)

class RulePermissionMixin():
    permission_classes = [RulePermissions]
    
class RuleSetRequestPermissionMixin():
    permission_classes = [RuleSetRequestPermissions]
    
class FirewallPermissionMixin():
    permission_classes = [FirewallPermissions]
    
class UserPermissionMixin():
    permission_classes = [UserPermissions]