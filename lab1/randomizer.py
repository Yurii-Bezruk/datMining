import random

file = open('films.txt', encoding='UTF-8')
films = []
for line in file:
    films.append(line.strip())

print(films[random.randint(0, len(films) - 1)], end='')
