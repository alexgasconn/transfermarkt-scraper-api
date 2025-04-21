def parse_market_value(value_str):
    value_str = value_str.replace("€", "").strip()
    if value_str.endswith("m"):
        return int(float(value_str[:-1].replace(",", ".")) * 1_000_000)
    elif value_str.endswith("k"):
        return int(float(value_str[:-1].replace(",", ".")) * 1_000)
    return 0
