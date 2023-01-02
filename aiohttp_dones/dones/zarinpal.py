from suds.client import Client

def zarinpal_make_payment(user, amount):
    error = ipg_url = ipg_ref_id = None
    zarinpal_merchant_id = '7186e340-04da-400c-b5a7-b7317a433915'  # Required
    zarinpal_webservice_url = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'  # Required
    call_back_url = 'http://localhost:5002/zarinpal-callback'
    # call_back_url = 'https://goldis.ir/zarinpal-callback'
    description = u'این یک تراکنش تستی از سمت نداست'  # Required
    email = 'user@userurl.ir'  # Optional
    mobile = '09123456789'  # Optional
    # amount = amount / 10 # Convert to toman.
    client = Client(zarinpal_webservice_url)
    result = client.service.PaymentRequest(zarinpal_merchant_id, amount, description, email, mobile, call_back_url)
    if result.Status == 100:
        ipg_ref_id = str(result.Authority)
        ipg_url = f'https://www.zarinpal.com/pg/StartPay/{ipg_ref_id}'
    else:
        error = 'zarinpal_make_payment_error'
    return error, ipg_url, ipg_ref_id

def verify_zarinpal_payment_transaction(transaction):
    error = 'unknown'
    zarinpal_merchant_id = '7186e340-04da-400c-b5a7-b7317a433915'
    zarinpal_webservice_url = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'
    client = Client(zarinpal_webservice_url)
    # amount = int(transaction['amount']) / 10 # Convert to toman.
    amount = transaction['amount']
    result = client.service.PaymentVerification(zarinpal_merchant_id, transaction['ipg_ref_id'], amount)
    return result


