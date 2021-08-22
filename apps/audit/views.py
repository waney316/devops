from base.views import BadeModelViewSet

from apps.audit.models import AuditLogModel
from apps.audit.serializer import AuditLogSerializer

# Create your views here.
class AuditLogView(BadeModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = AuditLogModel.objects.all()
    serializer_class = AuditLogSerializer
    search_fields = ("uri", )
    filterset_fields = ("method", "uri")