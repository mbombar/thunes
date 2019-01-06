
def getKey(item):
    return item[1]

def balance_transactions(users_balance):
    usr_plus = []
    usr_mins = []
    transactions = []
    for user, balance in users_balance.items():
        if balance > 0:
            usr_plus.append([user, balance])
        elif balance < 0:
            usr_mins.append([user, balance])
    usr_plus = sorted(usr_plus, reverse=False, key=getKey)
    usr_mins = sorted(usr_mins, reverse=True, key=getKey)
    while len(usr_plus) != 0:
        for i in usr_plus:
            for j in usr_mins:
                if i[1] == -j[1]:
                    transactions.append([j[0], i[0], i[1]])
                    usr_plus.remove(i)
                    usr_mins.remove(j)
                elif i[1] > j[1]:
                    continue
        if len(usr_plus) == 0:
            break
        trs_value = min(usr_plus[0][1], -usr_mins[0][1])
        transactions.append([usr_mins[0][0], usr_plus[0][0], trs_value])
        if trs_value == usr_plus[0][1]:
            usr_plus.remove(usr_plus[0])
            usr_mins[0][1] += trs_value
            usr_mins = sorted(usr_mins, reverse=True, key=getKey)
        else:
            usr_mins.remove(usr_mins[0])
            usr_plus[0][1] -= trs_value
            usr_plus = sorted(usr_plus, reverse=False, key=getKey)
    return transactions
