# secret-token

This is a utility library for working with [RFC8959][rfc8959] secret-token URIs.

It provides 3 functions:

- `encode` - Encodes a generated secret into a URI
- `decode` - Decodes a URI for passing secrets to systems that do not support URI data
- `validate` - Checks if a secret-token URI is conforms to the spec

There are two main expected use cases for this library:

1. Creating a service that generates and validates user secrets such as an API server. As per the RFC all secrets should be stored at rest encoded as URIs, so the `encode` function is used immediately after generating tokens and the `validate` function is called when recieving tokens from users.
2. Use in a service that talks to external services that do _not_ support RFC8959 but where you would like to store all your secrets using it. For example:

```python
import os

import secret_token

API_TOKEN = secret_token.decode(os.environ.get("API_TOKEN"))
```

[rfc8959]: https://tools.ietf.org/html/rfc8959 "The \"secret-token\" URI Scheme"
