from rest_framework.decorators import api_view
from rest_framework.response import Response

from rules.models import Rule
from rules.serializers import RuleSerializer

@api_view(['POST'])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """
    serializer = RuleSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True): # entweder exception raisen => speaky, oder einfach generic Response (unten)
        return Response(serializer.data)
    return Response({"invalid": "no good"}, status=400)