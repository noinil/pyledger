#!/usr/bin/env python3

import sys
from datetime import datetime

def main(datafile_name):
    print("============================================================")
    print(" Reading org ledger file:", datafile_name)

    with open(datafile_name, 'r') as data_in:
        iline = 0
        read_flag = False
        for line in data_in:
            iline += 1
            if line.strip() == '#+BEGIN_SRC ledger :noweb yes':
                read_flag = True
                print(line, read_flag)
                continue
            if not read_flag:
                continue
            if line.strip() == '#+END_SRC':
                read_flag = False
                print(line, read_flag)
                continue
            if read_flag:
                words = line.split()
                if len(words) < 1:
                    continue
                try:
                    entry_date = datetime.strptime(words[0], "%Y/%m/%d").date()
                    # print("{0:4d}-{1:2d}-{3:2d}".format(entry_date.year, entry_date.month, entry_date.day), end=" ")
                    print("{0:%Y-%m-%d}".format(entry_date), end=" | ")
                    star_index = line.find('*')
                    if star_index == -1:
                        place_index = line.find(words[1])
                    else:
                        place_index = star_index + 2
                    entry_place = line[place_index:].strip()
                    print("  at: {0:10s} ".format(entry_place[:10]))
                    local_balance_amount = 0
                    local_balance_currency = 'NONE'
                except:
                    entry_branch_line = words[0]
                    print(entry_branch_line)
                    if len(words) > 1:
                        entry_amount = float(words[1])
                        entry_currency = words[2]
                        if '@' not in words:
                            if local_balance_currency == 'NONE':
                                local_balance_currency = entry_currency
                            elif local_balance_currency != entry_currency:
                                print(" ERROR! Inconsistent currency in one block!  Line:", iline)
                                exit()
                            local_balance_amount += entry_amount
                        else:
                            exchange_rate = float(words[4])
                            balance_currency = words[5]
                            if local_balance_currency == 'NONE':
                                local_balance_currency = balance_currency
                            elif local_balance_currency != balance_currency:
                                print(" ERROR! Inconsistent currency in one block!")
                                exit()
                            local_balance_amount += entry_amount * exchange_rate
                    else:
                        entry_amount = - local_balance_amount
                        entry_currency = local_balance_currency
                    print("{0:7.2f} {1:3s}".format(entry_amount, entry_currency))

            

if __name__ == '__main__':
    datafile_name = sys.argv[1]
    main(datafile_name)
