import csv
def calculate_revenue():
    total_revenue=0
    # total_orders=0
    # highest_amount=0
    # highest_product=""

    with open("data/orders.csv","r") as file:
        reader=csv.reader(file)
        next(reader)
        for row in reader:
            order_id=row[0]
            customer_name=row[1]
            product_name=row[2]
            amount=int(row[3])
            # if amount>10000:
            #     print("Large Order Found:",product_name)
            # total_orders=total_orders+1
            total_revenue=total_revenue+amount
        return total_revenue
            # if amount>highest_amount:
            #     highest_amount=amount
            #     highest_product=product_name
    # average_order_value=total_revenue/total_orders
    # print("========SALES REPORT=========")
    # print("Total Orders:",total_orders)
    # print("Total Revenue:",total_revenue)
    # print("Average Order Value:",average_order_value)
    # print("Highest value order product:",highest_product)
    # print("Highest value order amount:",highest_amount)
revenuee=calculate_revenue()
print(revenuee)