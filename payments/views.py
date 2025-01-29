import uuid
from django.utils import timezone
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from .models import Gateway,Payment
from .serializers import GatewaySerializer
from subscriptions.models import Package
# Create your views here.

class GatewayView(APIView):
    def get(self,request):
        gateways = Gateway.objects.filter(is_enable=True)
        serializer =GatewaySerializer(gateways,many=True)
        return Response(serializer.data)

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        gateway_id= request.query_params.get('gateway')
        package_id=request.guery_params.get('package')

        try:
            package=Package.objects.get(pk=package_id,is_enable =True)
            gateway = Gateway.objects.get(pk=gateway_id,is_enable=True)
        except (Package.DoesNotExist, Gateway.DoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        peyment = Payment.objects.create(
            user = request.user,
            package = package,
            gateway = gateway,
            price = package.price,
            phone_numbeer=request.user.phone_number,
            token = str(uuid.uuid4())
        )
        # return redirect()
        return Response({'token':payment.token,'callback_url':'http://my-site.com/payments/pay/'})

    def post(self,request):
        token = request.data.get('token')
        st = request.data.get('status')
        try:
            payment = Payment.objects.get(token=token)
        except payment.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if st != 10:
            payment.status = Payment.STATUS_CANCELED
            payment.save()

            # return  (request,'payment-result.html',context = {'status':payment})
            return Response({'detail':'Payment canceled by user'},status=status.HTTP_400_BAD_REQUEST)

        r = request.post('bank_verify_url',data={})
        if r.status_code // 100 !=2:
            payment.status=payment.STATUS_ERROR
            payment.save()
            # render(request,'payment-resulte.html',context= {'status':payment})

            return  Response({'detail':'payment verification failed'},status=status.HTTP_400_BAD_REQUEST)
        payment.status=payment.STATUS_PAID
        payment.save()

        subscriptions.objects.create(
            user = payment.user,
            package = payment.package,
            expire_time = timezone.now() + timezone.timedelta(days=payment.package.duration.days)
        )
        return Response({'detail':'payment is successful'})