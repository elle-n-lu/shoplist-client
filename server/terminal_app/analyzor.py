import os
import tkinter.filedialog
import csv


class analyzor:
    # analyzor object need three params when initialized/created
    def __init__(self, budget,  user_dict:dict, search_lists:list[dict]) -> None:
        self.budget = budget
        self.user_dict = user_dict
        self.search_lists = search_lists

    # match keywords in shoplist and return remaining searching results
    def search_item_match_records(self):
        # general match the target amount of product in the list
        # not consider adding nultiple weights to match the target amount for now!
        search_keep_list = []
        #loop product, keywords in userinput dict,
        for key1, val1 in self.user_dict.items():
            index1 = list(self.user_dict).index(key1)
            item_search_dict = {}
            # index of userinput is same as the search results
            # get the product, price of the search result with the index of the item
            t = 0
            for price2, key2 in self.search_lists[index1].items():
                # loop keyword in keywords list
                s = 0
                for std in val1:
                    # id keyword is in the name in search results, then save the search record
                    if str.lower(std) in str.lower(key2):
                        item_search_dict[price2] = key2
                    else:
                        s += 1
                if s == len(val1):
                    t += 1
            # if all keywords not match, ask customer to see other results or quit
            if t == len(list(self.search_lists[index1])):
                # if only one item in shoplist and no match, then quit
                if len(self.search_lists) == 1:
                    raise SystemExit(f'sorry, no search result match key words of {key1},')
                # ask input to decide
                print(f'sorry, no search result match key words of {key1},')
                # decision = input('you wanna see the rest press y; quit press enter ')
                # if decision != 'y':
                #     raise SystemExit('left')
                # else:
                #     continue
            if len(item_search_dict) != 0:
                search_keep_list.append(item_search_dict)
        # save format is a list of dict: [{ price: name},{..},{..}]
        return search_keep_list

    # pure function
    # add each element of 1st list to each ele of 2nd list
    def add_price(self,arr1):
        total = []
        n = len(arr1)
        # if only one item for searching, then all prices for one item put in a list of dict
        if n == 1:
            return [{price: val} for price,val in arr1[0].items()]
        # if more than one item
        else:
            # if two items, then loop two lists, add each price, put relevant price and product name in list.
            for price1, x in arr1[0].items():
                for price2, y in arr1[1].items():
                    total.append({round(float(price1)+float(price2),2): [[x, price1], [y, price2]]})
            # the 'total' list will be applied to next addition loop if more than 2 items
            if n > 2:
                k = 2
                tt = []
                while k < n:
                    for i in total:
                        for price1, x in i.items():
                            for price2, y in arr1[k].items():
                                tt.append(
                                    {round(float(price1)+float(price2),2): x+[[y, price2]]})
                    total = tt
                    tt = []
                    k += 1
        return total
    
    # to find if the total cost of each possibility <= budget, then keep results in list
    # each possibility is a lsit of dict like this:
    # {12.9: [['SOGA', '1.4'], ['SOoden Handle', '2.7'], ['La Extra Large', '2.9'], ['Lemon And Lime wrap iron 6.5cm 4PK', '5.9']]}
    def price_budget_match(self):
        try:
            search_items = self.search_item_match_records()
            total_price_list = self.add_price(search_items)
            total_price_list_copy = total_price_list.copy()
            for i in range(len(total_price_list)-1,-1,-1):
                for key in total_price_list[i]:
                    if float(key)>self.budget:
                        total_price_list.remove(total_price_list[i])
            # budget not enough, let user choose to show the remaining results or quit
            if len(total_price_list) == 0:
                print('budget not enough to buy all products in the list! Try remove some or increase budget!')
                decision = input('check the search results, enter y;To Quit press enter  ')
                if decision != 'y':
                    raise SystemExit('left')
            
            # sort all results by the total cost
            total_price_list = sorted(total_price_list_copy, key= lambda item: list(item)[0])
            # # only return 10 possibility combinations for now
            return total_price_list[:10]
        except SystemExit as e:
            print(e)

   
