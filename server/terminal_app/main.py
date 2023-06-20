from terminal_app.userinpu import userinput
from terminal_app.brow import brow
from terminal_app.analyzor import analyzor

def get_plans(budget, path):
    try:
        userinputs = userinput(path)
        user_dict = userinputs.get_shoplist()
        price_item_list =[]
        for i in user_dict:
            item = brow(i)
            price_item = item.get_title_price()
            price_item_list += price_item
        item.closewindow()
        analyze = analyzor(budget,user_dict, price_item_list)
        output = analyze.price_budget_match()
        return output
    except (KeyboardInterrupt, ValueError, TypeError,AttributeError) :
        return None