from .permissions import RulePermissions, RuleSetRequestPermissions

class RulePermissionMixin():
    permission_classes = [RulePermissions]
    
class RuleSetRequestPermissionMixin():
    permission_classes = [RuleSetRequestPermissions]