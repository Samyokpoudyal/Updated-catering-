from typing import Any
from django.views.generic import TemplateView
import uuid
import hmac
import hashlib
import base64

# General Error to be fixed before final defence :

#   1) This code which has indicated the invalid payload signature

#   2) After the payment the payment records for which the models be corrected.



class EsewaTemplate(TemplateView):
    template_name = 'esewapayment/esewa.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

       
        total_amount = int(self.kwargs.get('category_price_info'))
        category_id = self.kwargs.get('category_id')
        uid = str(uuid.uuid4())

       
        secret = "8gBm/:&EnhH.1/q"
        # key_bytes = secret.encode('utf-8')
        message = f'total_amount={total_amount},transaction_uuid={uid},product_code=EPAYTEST'
        

       
        hmac_sha256 = hmac.new(secret, message, hashlib.sha256)
        digest = hmac_sha256.digest()
        signature = base64.b64encode(digest).decode('utf-8')

        context['signature'] = signature
        context['tax_amount'] = int(0.13 * total_amount)  
        context['uid'] = uid
        context['amount'] = total_amount
        context['total_amount'] = total_amount + context['tax_amount']
        context['category_id'] = category_id

        return context
