"""
- Generator is faster than the list
  because it waits for make call to yield the result
"""
# def square_numbers(nums):
# 	for i in nums:
# 		yield (i*i)

# my_nums = square_numbers([1, 2, 3, 4, 5])

my_nums = (x*x for x in [1, 2, 3, 4, 5]) # generator Comprehension
print(my_nums) # all result are not stored in memory yet.

for num in my_nums:
	print(num)
