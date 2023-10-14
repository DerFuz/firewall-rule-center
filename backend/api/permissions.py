from rest_framework import permissions
#from django_auth_ldap.backend import LDAPBackend

class RulePermissions(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
    
    # for permission debugging purpose
    # def has_permission(self, request, view):
    #     user = request.user
    #     ldap_user = LDAPBackend().populate_user(username=user.username)
    #     print(f'LDAP-Perm: {LDAPBackend().get_all_permissions(ldap_user)}')
    #     print(f'Permissions: {user.get_all_permissions()}')
    #     return super().has_permission(request, view)
    
class RuleSetRequestPermissions(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }