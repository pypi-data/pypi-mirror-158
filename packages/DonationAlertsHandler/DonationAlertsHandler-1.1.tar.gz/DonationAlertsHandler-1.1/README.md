# DonationAllertsHandler

Simple example:


```py
from donation_alerts_handler.donation_alerts import Client
from donation_alerts_handler import filters
client = Client("DonationAlerts_TOKEN")

@client.on_donate(filters.minimum_value(1), filters.currency("RUB"), filters.message_prefix("tgc"))
async def on_donate(donate: Donations):
    print("Handled donate", donate)
    donations = await client.donations()
    print(len(donations))


client.run()
```

## You can create your filters. They needed to return boolean value:
```py
def minimum_value(n: int):
    async def f(donate: Donations):
        return n <= donate.amount

    return f
```
