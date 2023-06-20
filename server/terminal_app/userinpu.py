from os import path

class userinput:
    def __init__(self,path):
        self.path = path
    
    # open file and save text in a shoppinglist dict
    # shoplists dict example:{'apple':['1kg', 'gala'], 'skim milk':['2L',' m2'],'lollies':['10pack',' grape']}
    def get_shoplist(self):
        shoplist={}
        #error handling when no file selected
        try:
            with open(self.path, "r") as file1:
                for line in file1:
                    lines = line.strip()
                    product= lines.split(',')[0]
                    amount = lines.split(',')[1:]
                    shoplist[product] = amount
            return shoplist
        #error handling
        except FileNotFoundError:
            print('no file selected !')
    
# cd = use 




