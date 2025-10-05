from datetime import date
import json
from attrs import define, field
import random
import time

__timeout = 120 # seconds

@define
class GiftExchange:
    giver: str = field(eq=str.lower)
    receiver: str = field(eq=str.lower)

    def __repr__(self):
        return f"* {self.giver} -> {self.receiver}"

"""Generates an object list from json list

Args:
    jsonData: list of string tuples

Returns:
    The list of gift exchange
"""
def GetGiftExchange(jsonData: list[list[str]]) -> list[GiftExchange] | None:
    gift_exchange = []
    for pair in jsonData:
        if len(pair) == 2:
            gift_exchange.append(GiftExchange(pair[0],pair[1]))
        else:
            print(f'Invalid data in passed list {jsonData}')
    return gift_exchange

"""Generate an object list from a list of names

Args:
    names: The list of names for the exchange

Returns:
    The list of gift exchange
"""
def GenerateList( names: list[GiftExchange]):
    names2 = list(names)
    while True:
        random.shuffle(names2)
        if all(x != y for x, y in zip(names, names2)):
            return [GiftExchange(x, y) for x, y in zip(names, names2)]

"""Pull data from JSON file

Args:
    last_year: the previous year in YYYY format
    xmas_lists: 
"""
def GetJsonData(last_year: int):
    xmas_lists = []
    try:
        with open('./xmas_list.json', 'r') as file:
            data = json.load(file)
        list_of_names = data["list_of_names"]
        for year in data["xmas_lists"]:
            if year["name"].endswith(str(last_year)):
                last_years_list = year["exch_list"]
            elif year["name"] == "Illegal_Exchanges":
                illegal_exchanges = year["exch_list"]
            else:
                xmas_lists.append(year["exch_list"])
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file.")
        return
    return list_of_names,last_years_list,illegal_exchanges,xmas_lists

def RunIter(
        list_of_names: list[str],
        last_years_list: list[GiftExchange], 
        illegal_exchanges: list[GiftExchange], 
        xmas_lists: list[list[GiftExchange]]
        ):
    is_banned = False
    start_time = time.time()

    while True:
        new_list = GenerateList(list_of_names)
        if new_list not in xmas_lists:
            for check in (last_years_list, illegal_exchanges):
                if is_banned:
                    is_banned = False
                    break
                for banned in check:
                    if banned in new_list:
                        is_banned = True
                        break
            else:
                if not is_banned:
                    return new_list

        if time.time() - start_time > __timeout:
            print("New list not calculated. Try again")
            new_list = None
            return None


def main():
    list_of_names = None
    last_year = date.today().year -1
    last_years_list = None
    illegal_exchanges = None
    xmas_lists = []
    list_of_names, last_years_list, illegal_exchanges,xmas_lists = GetJsonData(last_year)
    
    if list_of_names and last_years_list and illegal_exchanges:
        
        # Format data
        last_years_list = GetGiftExchange(last_years_list)
        illegal_exchanges = GetGiftExchange(illegal_exchanges)
        xmas_lists = [GetGiftExchange(raw_list) for raw_list in xmas_lists]

        # Iterate over new list
        new_list = RunIter(list_of_names,last_years_list,illegal_exchanges,xmas_lists)
        if new_list:
            print(new_list)
    else:
        print("Json data was not passed in correctly")


    # for list in data["xmas_lists"]:
    #     print(list)
    # new_list = RunIter()
    # if new_list:
    #     for n in new_list:
    #         print(n)


if __name__ == "__main__":
    main()