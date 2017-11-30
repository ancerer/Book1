class Restaurant():
    def __init__(self, name, type):
        self.restaurant_name = name
        self.cuisine_type = type
        self.number_served = 0

    def describe_restaurant(self):
        print(self.cuisine_type, self.restaurant_name)

    def open_restaurant(self):
        print('This restaurant is open')

    def set_number_served(self, number):
        self.number_served = number
        print(self.number_served)

    def increment_number_served(self, innumber):
        self.number_served = innumber
        print("你认为这家餐馆每天可能接待的就餐人数：", self.number_served)


restaurant = Restaurant('YangYang', 'coffice')
print(restaurant.restaurant_name, restaurant.cuisine_type)

restaurant.describe_restaurant()
restaurant.open_restaurant()
restaurant.set_number_served(5)
restaurant.increment_number_served(10)