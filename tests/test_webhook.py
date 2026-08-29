import hmac, hashlib
import backend.api.webhook as wh
def test_signature():
    wh.RAZORPAY_WEBHOOK_SECRET="secret"
    body=b'{"event":"payment.captured"}'
    sig=hmac.new(b"secret",body,hashlib.sha256).hexdigest()
    assert wh.verify_signature(body,sig)
