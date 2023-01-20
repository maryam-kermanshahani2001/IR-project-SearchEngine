# def tokenize():
#     token = {}
#     my_normalizer = Normalizer()
#     my_tokenizer = Tokenizer()
#     for k in
#         Tokenizer.tokenize_words(my_normalizer.normalize(all_data[]))

from itertools import chain, pairwise
from typing import List


# from https://docs.python.org/3/library/itertools.html#itertools-recipes
def triplewise(iterable):
    "Return overlapping triplets from an iterable"
    # triplewise('ABCDEFG') --> ABC BCD CDE DEF EFG
    for (a, _), (b, c) in pairwise(pairwise(iterable)):
        yield a, b, c


def consecutive_numbers_in_list(*lists: List[list]) -> bool:
    big_list = sorted(chain(*lists))
    for first, second, third in triplewise(big_list):
        if (first + 1) == second == (third - 1):
          return True
    return False

a = [1, 6, 10]
b = [2, 7, 11]
c = [3, 8]
consecutive_numbers_in_list(a, b, c)
