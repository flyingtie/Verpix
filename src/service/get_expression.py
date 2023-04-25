import random

def get_expression():
    nums = [num for num in random.choices(range(1, 11), k=2)]
    nums.sort()
    operation = random.choice("+-")
    expression = f"{nums[1]} {operation} {nums[0]}"
    answer = str(eval(expression))
    return expression, answer