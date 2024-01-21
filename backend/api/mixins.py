from .permissions import (
    RulePermissions, 
    RuleSetRequestPermissions, 
    FirewallPermissions, 
)

class RulePermissionMixin():
    permission_classes = [RulePermissions]
    
class RuleSetRequestPermissionMixin():
    permission_classes = [RuleSetRequestPermissions]
    
class FirewallPermissionMixin():
    permission_classes = [FirewallPermissions]
