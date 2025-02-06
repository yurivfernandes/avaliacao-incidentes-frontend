from django.db.models import Q
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from ...models import AssignmentGroup, ResolvedBy, SortedTicket
from ..serializers import SortedTicketSerializer


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class SortedTicketListView(generics.ListAPIView):
    serializer_class = SortedTicketSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = SortedTicket.objects.select_related("incident")

        # Exclui tickets que já possuem avaliações
        queryset = queryset.exclude(incident__avaliacoes__isnull=False)

        mes_ano = self.request.query_params.get("mes_ano", None)
        if mes_ano and mes_ano.strip():  # Só aplica o filtro se tiver valor
            queryset = queryset.filter(mes_ano=mes_ano)

        # Filtro de busca
        search = self.request.query_params.get("search", "")
        if search:
            resolved_by_ids = list(
                ResolvedBy.objects.filter(
                    dv_resolved_by__icontains=search
                ).values_list("id", flat=True)
            )

            assignment_group_ids = list(
                AssignmentGroup.objects.filter(
                    dv_assignment_group__icontains=search
                ).values_list("id", flat=True)
            )

            queryset = queryset.filter(
                Q(incident__number__icontains=search)
                | Q(incident__resolved_by__in=resolved_by_ids)
                | Q(incident__assignment_group__in=assignment_group_ids)
            )

        user = self.request.user
        if not user.is_staff and user.is_gestor:
            # Filtra por grupos do gestor
            queryset = queryset.filter(
                incident__assignment_group__in=user.assignment_groups.values_list(
                    "id", flat=True
                )
            )

        return queryset.order_by("-mes_ano", "incident__number")
