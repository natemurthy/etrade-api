"""Module signer is just this script"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from rauth.oauth import HmacSha1Signature

class OAuthTestHmacSha1Case:
    """
    OAuthTestHmacSha1Case wraps HmacSha1Signature
    """
    consumer_secret = '456'
    access_token_secret = '654'
    method = 'GET'
    url = 'http://example.com/'
    oauth_params = {}
    req_kwargs = {'params': {'foo': 'bar'}}

    def test_hmacsha1_signature(self):
        """
        simple test case
        """
        oauth_signature = HmacSha1Signature().sign(self.consumer_secret,
                                                   self.access_token_secret,
                                                   self.method,
                                                   self.url,
                                                   self.oauth_params,
                                                   self.req_kwargs)
        print(oauth_signature)

if __name__ == "__main__":
    o = OAuthTestHmacSha1Case()
    o.test_hmacsha1_signature()
