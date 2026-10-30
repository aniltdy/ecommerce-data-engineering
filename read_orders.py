import csv

with open("data/orders.csv","r") as file:
    reader=csv.reader(file)
    next(reader)
    for row in reader:
        print(row)