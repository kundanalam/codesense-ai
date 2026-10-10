from backend.problems import PROBLEMS
from backend.teach.leakage import check_hint

ref = PROBLEMS["sum_list"]["reference"]

safe = "Your loop ends one step too soon, so the last item is skipped."
leaky = """Use this:
def sum_list(nums):
    total = 0
    for n in nums:
        total += n
    return total"""

print("Safe hint  ->", check_hint(safe, ref))
print("Leaky hint ->", check_hint(leaky, ref))