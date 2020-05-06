def price_format(price) -> str:
    return '{:,} đ'.format(price).replace(',', '.')
