# Author: Khushboo Patel
# Date: 06/21/2021
# Description: This file contains an online store simulator. It has these classes:
# Product, Customer and Store.


class InvalidCheckoutError(Exception):
    """Custom exception used when executing the 'check_out_member' method in the Store class."""
    pass


class Product:
    """Common base class for all products."""

    def __init__(self, ID, title, description, price, quantity_available):
        """Creates a product object and initializes it's attributes."""
        self._ID = ID
        self._title = title
        self._description = description
        self._price = price
        self._quantity_available = quantity_available

    def get_product_id(self):
        """Returns the product ID."""
        return self._ID

    def get_title(self):
        """Returns the product title."""
        return self._title

    def get_description(self):
        """Returns the product description."""
        return self._description

    def get_price(self):
        """Returns the product price."""
        return self._price

    def get_quantity_available(self):
        """Returns quantity available."""
        return self._quantity_available

    def decrease_quantity(self):
        """Decreases quantity available by one."""
        self._quantity_available -= 1


class Customer:
    """Common base class for all customers."""

    def __init__(self, name, ID, premium_member):
        """Creates a Customer object and initializes it's attributes."""
        self._name = name
        self._ID = ID
        self._premium_member = premium_member
        self._cart = []

    def get_name(self):
        """Returns the customer's name."""
        return self._name

    def get_customer_id(self):
        """Returns the customer's ID."""
        return self._ID

    def is_premium_member(self):
        """Returns whether the customer is a premium member."""
        return self._premium_member

    def get_cart(self):
        """Returns the customer's cart."""
        return self._cart

    def add_product_to_cart(self, ID):
        """Takes a product ID code and adds it to the customer's cart."""
        self._cart.append(ID)

    def empty_cart(self):
        """Empties the customer's cart."""
        self._cart.clear()


class Store:
    """Common base class for all stores."""

    def __init__(self):
        """Creates a Store object and initializes it's attributes."""
        self._inventory = []
        self._member = []

    def add_product(self, product):
        """Takes a Product object and adds it to the inventory."""
        self._inventory.append(product)

    def add_member(self, customer):
        """Takes a Customer object and adds it to the member list."""
        self._member.append(customer)

    def lookup_product_from_id(self, ID):
        """Takes a Product ID and returns the Product with the matching ID.
        If no matching ID is found in the inventory, it returns the special value None."""
        # Available upon request
        pass

    def lookup_member_from_id(self, ID):
        """Takes a Customer ID and returns the Customer with the matching ID.
        If no matching ID is found in the membership, it returns the special value None."""
        # Available upon request
        pass

    def product_search(self, string):
        """Takes a search string and returns a stored list of ID codes for every product in the inventory
        whose title or description contains the search string."""
        # Available upon request
        pass

    def add_product_to_member_cart(self, product_ID, customer_ID):
        """Takes a Product ID and a Customer ID (in that order).
        If the product isn't found in the inventory, returns "product ID not found".
        If the product was found, but the member isn't found in the membership, returns "member ID not found".
        If both are found and the product is still available, calls the member's add_product_to_cart method to add the product and then returns "product added to cart".
        If the product was not still available, returns "product out of stock". """
        # Available upon request
        pass


    def check_out_member(self, customer_ID):
        """Takes a Customer ID. If the ID doesn't match a member of the store, raises a custom exception.
        Otherwise returns the charge for the member cart. This is the total cost of all the items in the cart,
        not including any items that are not in the inventory or are out of stock, plus the shipping cost.
        If a product is not out of stock, price is added to the total and available quantity of that product is decreased by 1.
        For premium members, the shipping cost is $0. For normal members, the shipping cost is 7% of the total cost of the items in the cart.
        When the charge for the member's cart has been tabulated, the member's cart should be emptied, and the charge amount returned."""
        # Available upon request
        pass


def main():
    """Tries to check out a customer based on store membership."""
    try:
        p1 = Product("1", "Burger", "Cheese Burger", 5.99, 3)
        p2 = Product("2", "French Fries", "Unsalted", 2.99, 0)
        # print(p1.get_product_id())
        # print(p1.get_title())
        # print(p1.get_description())
        # print(p1.get_price())
        # print(p1.get_quantity_available())
        # print(p1.decrease_quantity())
        # print(p1.get_quantity_available())

        c1 = Customer("Kay", 8, False)
        c2 = Customer("Annia", 2, False)
        # print(c2.get_name())
        # print(c2.get_customer_id())
        # print(c2.is_premium_member())
        # print(c2.get_cart())
        # c2.add_product_to_cart("1")
        # print(c2.get_cart())

        myStore = Store()
        myStore.add_product(p1)
        myStore.add_product(p2)
        myStore.add_member(c1)
        myStore.add_member(c2)
        print(myStore.lookup_product_from_id("2"))
        print(myStore.lookup_member_from_id(8))
        print(myStore.product_search("Fries"))
        print(myStore.add_product_to_member_cart("4", 2))
        print(myStore.add_product_to_member_cart("1", 7))
        print(myStore.add_product_to_member_cart("1", 8))
        print(myStore.add_product_to_member_cart("2", 8))

        print(myStore.check_out_member(8))
        print(myStore.check_out_member(2))
        print(myStore.check_out_member(1))

    except InvalidCheckoutError:
        print("member ID not found")


if __name__ == '__main__':
    main()
