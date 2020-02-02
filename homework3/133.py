my_list = [1, 2, 3, 4, 5, 6]

# for even_num in my_list[1::2]:
#     print(even_num)

def stock_list(listup):
    for listup_stock in listup[1::2]:
        print(listup_stock)

stock_list(my_list)
