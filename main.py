from attrs import define, field
import random
import time

b = "Betty"
c = "Cody"
e = "Erin"
j = "Jimmy"
r = "Rob"
s = "Steve"

timeout = 120 # seconds
start_time = time.time()

@define
class GiftExchange:
    giver: str = field(eq=str.lower)
    receiver: str = field(eq=str.lower)

    def __repr__(self):
        return f"* {self.giver} -> {self.receiver}"

# Lists
list_of_names = [ b, c, e, j, r, s]

christmas_2022 = [
    GiftExchange(b, e),
    GiftExchange(s, r),
    GiftExchange(c, s),
    GiftExchange(j, c),
    GiftExchange(r, j),
    GiftExchange(e, b)
]

christmas_2023 = [
    GiftExchange(b, c),
    GiftExchange(s, e),
    GiftExchange(c, r),
    GiftExchange(j, b),
    GiftExchange(r, s),
    GiftExchange(e, j)
]

christmas_2024 = [
    GiftExchange(b, r),
    GiftExchange(s, j),
    GiftExchange(c, b),
    GiftExchange(j, e),
    GiftExchange(r, c),
    GiftExchange(e, s)
]

do_not_allow = [
    GiftExchange(b, s),
    GiftExchange(s, b),
    GiftExchange(e, r),
    GiftExchange(r, e)
]

def GenerateList( names: list[GiftExchange]):
    names2 = list(names)
    while True:
        random.shuffle(names2)
        if all(x != y for x, y in zip(names, names2)):
            return [GiftExchange(x, y) for x, y in zip(names, names2)]

def RunIter():
    while True:
        new_list = GenerateList(list_of_names)
        if new_list not in (christmas_2023, christmas_2022):
            for check in (christmas_2024, do_not_allow):
                if all(banned not in new_list for banned in check):
                    return new_list
        if time.time() - start_time > timeout:
            print("New list not calculated. Try again")
            new_list = None
            return None


def main():
    new_list = RunIter()
    if new_list:
        for n in new_list:
            print(n)


if __name__ == "__main__":
    main()