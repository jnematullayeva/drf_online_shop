from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from shared.permissions import IsAdminOrReadOnly
from .models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_role == "admin":
            return Payment.objects.all()
        return Payment.objects.filter(order__user=self.request.user)

    @action(detail=True, methods=["post"])
    def confirm_payment(self, request, pk=None):
        payment = self.get_object()
        if payment.status != "pending":
            return Response({"error": "Tolov allaqachon amalga oshirilgan"}, status=400)
        payment.status = "completed"
        payment.transaction_id = "simulated_txn_id"
        payment.save()
        # buyurtmani holatini "paid" ga o'zgartirish
        payment.order.status = "paid"
        payment.order.save()
        return Response(PaymentSerializer(payment).data)