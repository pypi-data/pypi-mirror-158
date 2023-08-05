# Tether Price

### Tether price is a library that helps you to get the Tether price from various websites.

## How To Install

#### You can use the following command to install it.

```commandline
pip install tether-price
```

## Getting Started

```python
from tether import SourceManager
from tether.sources import *

manager = SourceManager()
manager.add(Bitbarg())
manager.add(ArzPaya())

if __name__ == '__main__':
    prices_list = manager.get_prices_list()
    for price in prices_list.prices:  # type: Price
        print(f'{price.source} | Buy: {price.buy} | Sell: {price.sell}')
```

## License

[MIT](https://github.com/iAliF/Tether-Price/blob/main/LICENSE)