from rest_framework.permissions import DjangoModelPermissions


class AllowAnonCreate(DjangoModelPermissions):

    def has_permission(self, request, view):
        return any((
            request.method in ['GET', 'POST'],
            super().has_permission(request, view),
        ))
