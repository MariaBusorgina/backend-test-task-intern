
def generate_sequence(n):
    result = ""
    number = 1

    while len(result) < n:
        result += str(number) * number
        number += 1

    return result[:n]


n = int(input("Введите количество элементов последовательности: "))
result = generate_sequence(n)

print("Последовательность:", result)
