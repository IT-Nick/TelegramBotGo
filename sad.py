
current_price = {'RUB_RUB' : 135.212, 'USD_RUB' : 21.452, 'CON_RUB' : 32, 'asd_RUB' : 0.44}
difference_price_moex = {}
percent = 30

ab = ""

for key, value in zip(current_price, current_price.values()): 
    ab += (key + " " + str(value) + "; ")

print(ab)

a = '10.32443'
if float(a) < 11:
    print(a + "a")

