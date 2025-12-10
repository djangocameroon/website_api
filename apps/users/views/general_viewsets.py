from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class BaseModelViewSet(ModelViewSet):
    """
    A base viewset that you can extend to add custom pagination handling.
    """

    def paginated_response(
            self, queryset, request,
            serializer_class, message="Success",
            status_code=status.HTTP_200_OK,
    ):
        """
        Custom paginated response method.
        """
        page = self.paginate_queryset(queryset)
        serializer = serializer_class(page, many=True)
        response_data = {
            "status": True,
            "message": message,
            "status_code": status_code,
            "page": self.paginator.page.number,
            "page_size": self.paginator.page_size,
            "total": self.paginator.page.paginator.count,
            "pagination": {
                "next": self.paginator.get_next_link(),
                "previous": self.paginator.get_previous_link(),
                "count": self.paginator.page.paginator.count,
                "current_page": self.paginator.page.number,
                "total_pages": self.paginator.page.paginator.num_pages,
            },
            "results": serializer.data
        }
        return Response(response_data, status=status_code)
