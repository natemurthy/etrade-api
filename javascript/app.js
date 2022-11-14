const express = require('express')
const app = express()

const axios = require('axios');
const { v1 } = require('uuid');
const crypto = require('crypto');

function generateSignature() {
  const method = 'GET',
        url = 'http://localhost/',
        encodedUrl = encodeURIComponent(url),
        paramaters = {
          oauth_consumer_key: process.env.ETRADE_SANDBOX_API_KEY,
          oauth_signature_method: 'HMAC-SHA1',
          oauth_timestamp: Math.floor(Date.now() / 1000),
          oauth_nonce: v1(),
          oauth_callback: 'oob'
        }

  var ordered = {};
  Object.keys(paramaters).sort().forEach((key) => {
    ordered[key] = paramaters[key];
  });

  var encodedParameters = '';

  for(k in ordered) {
    const encodedValue = escape(ordered[k]);
    const encodedKey = encodeURIComponent(k);

    if(encodedParameters === '') {
      encodedParameters += encodeURIComponent(`${encodedKey}=${encodedValue}`);
    } else {
      encodedParameters += encodeURIComponent(`&${encodedKey}=${encodedValue}`);
    }
  }

  encodedParameters = encodeURIComponent(encodedParameters);

  const signature_base_string = `${method}&${encodedUrl}&${encodedParameters}`;
  console.log("signature_base_string", signature_base_string);

  const signing_key = process.env.ETRADE_SANDBOX_SECRET_KEY;
  const signature = crypto.createHmac("SHA1", signing_key).update(signature_base_string).digest().toString('base64');
  const encodedSignature = encodeURIComponent(signature);

  console.log('oauth_signature', encodedSignature);
  return encodedSignature;
}

const request = async (req, res) => {
  console.log('Fetching request token from etrade...');

  try {
    var response = await axios.get(`https://apisb.etrade.com/oauth/request_token`, {
      params: {
        oauth_consumer_key: process.env.ETRADE_SANDBOX_API_KEY,
        oauth_signature_method: 'HMAC-SHA1',
        oauth_signature: generateSignature(),
        oauth_timestamp: Math.floor(Date.now() / 1000),
        oauth_nonce: v1(),
        oauth_callback: 'oob'
      }
    });

    console.log('Fetched request token...', response.data);
  } catch (error) {
    console.log('Could not fetch request token...', error.response.data);
  }
  res.send("token request sent")
}


app.route('/auth/request').get(request);


// launch the server
const port = process.env.PORT || 3000
const server = app.listen(port, () => {
  console.log("listening on port %s...", server.address().port)
})
