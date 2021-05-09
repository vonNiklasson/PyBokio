# PyBokio

Unofficial SDK for interacting with [Bokio](https://www.bokio.se)

> Currently the project is in very early development and very little 
> functionality can be used. But if you are eager to get stuff going, 
> please consider helping out by [contributing](#contributing)!


## Usage

### Connecting

#### Connecting with credentials

The simplest way to connect with the client is through credentials.

```python
from pybokio import BokioClient

client = BokioClient(
    company_id="00000000-0000-4000-0000-000000000000",
    username="your@email.here",
    password="your.password"
)
client.connect()
```

#### Connecting with cookies

A preferred way to connect is to reuse the cookies after logging in with credentials.

**Saving cookies from an existing session**

```python
import pickle

...

cookies = client.get_cookies()
with open('session.pickle', 'wb') as f:
    pickle.dump(cookies, f)
```

**Reusing cookies to connect again**

```python
from pybokio import BokioClient
import pickle

with open('session.pickle') as f:
    cookies = pickle.load(f)

client = BokioClient.from_cookies(
    company_id="00000000-0000-4000-0000-000000000000",
    cookies=cookies
)
client.connect()
```

  
## Contributing

Contributions are always welcome!

To contribute, please take the following steps:

1. [Fork](https://github.com/vonNiklasson/PyBokio/fork) the repo
2. Add your change
3. Make a pull request with a short description of the change you're proposing.


## Authors

- [@vonNiklasson](https://www.github.com/vonNiklasson)

  