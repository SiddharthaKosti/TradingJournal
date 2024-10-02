
from jugaad_data.nse import stock_df
from datetime import date

df = stock_df(symbol="SBIN", from_date=date(2024,9,23),
            to_date=date(2024,9,27), series="EQ")
print(df.head())