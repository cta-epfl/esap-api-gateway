from rest_framework import viewsets, permissions

from .serializers import RucioSerializer


class RucioViewSet(viewsets.ModelViewSet):
    serializer_class = RucioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.staging.all()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)