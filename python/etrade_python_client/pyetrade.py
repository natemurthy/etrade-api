import pyetrade

'''
this libarary seems broken, exits with

AttributeError: partially initialized module 'pyetrade' has no attribute 'ETradeOAuth' (most likely due to a circular import)
'''

consumer_key = "b9bf2ceaafdea1f27e611a802a0635a4"
consumer_secret = "1f8cae208838bf73aa11a7485e3236bfb52c3443ea84d0e152f280f3460e596d"

oauth = pyetrade.ETradeOAuth(consumer_key, consumer_secret)
print(oauth.get_request_token())  # Use the printed URL

verifier_code = input("Enter verification code: ")
tokens = oauth.get_access_token(verifier_code)
print(tokens)
