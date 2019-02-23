
def st1_max_mean(df, window, cof):
    df['f_price_max'] = df['price'].shift(-window).rolling(window=window).max()
    df['f_price_min'] = df['price'].shift(-window).rolling(window=window).mean()
    df['f_price'] = df['price'].shift(-window)
    df['value_real_1'] = df['f_price_max'] - df['price'] > cof
    df['value_real_2'] = df['price'] - df['f_price_min'] < cof
    return df['value_real_1'] & df['value_real_2']

def st1_max_min(df, window, cof):
    df['f_price_max'] = df['price'].shift(-window).rolling(window=window).max()
    df['f_price_min'] = df['price'].shift(-window).rolling(window=window).min()
    df['f_price'] = df['price'].shift(-window)
    df['value_real_1'] = df['f_price_max'] - df['price'] > cof
    df['value_real_2'] = df['price'] - df['f_price_min'] < cof
    return df['value_real_1'] & df['value_real_2']