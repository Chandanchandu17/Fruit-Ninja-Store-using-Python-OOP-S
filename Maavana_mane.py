import random
import time
from datetime import datetime
import requests
import os

# Telegram Notifier Class
class TelegramNotifier:
    def __init__(self, bot_token="AAGjUYc-bp9makKgbqP1Jx6_S4_C23Y_FJY", chat_id=1138856980):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.enabled = bot_token and chat_id
        
    def send_message(self, message):
        """Send message to Telegram. If not configured, just log locally."""
        if self.enabled:
            try:
                url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
                data = {
                    'chat_id': self.chat_id,
                    'text': message
                }
                response = requests.post(url, data=data, timeout=5)
                if response.status_code == 200:
                    print(f"Notification sent: {message}")
                else:
                    print(f"Failed to send notification: {response.status_code}")
            except Exception as e:
                print(f"Notification error: {e}")
        else:
            # Log locally if Telegram is not configured
            print(f" Log: {message}")

class Fruit:
    def __init__(self, name, price, benefits, description, nutritional_info, origin, season):
        self.name = name
        self.price = price
        self.benefits = benefits
        self.description = description
        self.nutritional_info = nutritional_info
        self.origin = origin
        self.season = season

    def show_description(self):
        return f"""{self.name} - ₹{self.price}
Description: {self.description}
Health Benefits: {self.benefits}
Nutritional Info: {self.nutritional_info}
Origin: {self.origin}
Best Season: {self.season}
{'='*50}
"""

    def show_brief(self):
        return f"{self.name} - ₹{self.price}"

class User:
    def __init__(self, username, phone_number=None, email=None):
        self.username = username
        self.phone_number = phone_number
        self.email = email
        self.wishlist = []
        self.order_history = []

    def add_to_wishlist(self, fruit):
        if fruit not in self.wishlist:
            self.wishlist.append(fruit)
            return True
        return False

    def remove_from_wishlist(self, fruit):
        if fruit in self.wishlist:
            self.wishlist.remove(fruit)
            return True
        return False

    def show_wishlist(self):
        print(f"\n{self.username}'s Wishlist:")
        if not self.wishlist:
            print("Your wishlist is empty!")
        else:
            for idx, fruit in enumerate(self.wishlist, 1):
                print(f"{idx}. {fruit.name} - ₹{fruit.price}")

    def add_to_order_history(self, order):
        self.order_history.append(order)

    def show_order_history(self):
        print(f"\{self.username}'s Order History:")
        if not self.order_history:
            print("No previous orders found!")
        else:
            for idx, order in enumerate(self.order_history, 1):
                print(f"{idx}. Order #{order['id']} - ₹{order['total']} - {order['date']}")

class OTPSystem:
    def __init__(self):
        self.generated_otp = None
        self.otp_timestamp = None
        self.otp_validity_minutes = 5

    def generate_otp(self):
        self.generated_otp = random.randint(100000, 999999)
        self.otp_timestamp = time.time()
        return self.generated_otp

    def verify_otp(self, entered_otp):
        if self.generated_otp is None:
            return False, "No OTP generated"
        
        current_time = time.time()
        if current_time - self.otp_timestamp > self.otp_validity_minutes * 60:
            return False, "OTP expired"
        
        if int(entered_otp) == self.generated_otp:
            self.generated_otp = None  # Reset after successful verification
            return True, "OTP verified successfully"
        else:
            return False, "Invalid OTP"

class Maavana_mane:
    def __init__(self, notifier):
        self.menu = []
        self.cart = []
        self.total = 0
        self.user = None
        self.notifier = notifier
        self.otp_system = OTPSystem()
        self.order_counter = 1000

    def register_user(self):
        print("\nUser Registration")
        username = input("Enter your username: ")
        phone = input("Enter your phone number: ")
        email = input("Enter your email: ")
        
        self.user = User(username, phone, email)
        print(f"Welcome, {self.user.username}! Registration successful.")
        self.notifier.send_message(f"New user registered: {self.user.username}")

    def login(self):
        if self.user is None:
            print("Please register first!")
            self.register_user()
        else:
            username = input("Enter your username: ")
            if username == self.user.username:
                print(f"Welcome back, {self.user.username}!")
                self.notifier.send_message(f"User logged in: {self.user.username}")
            else:
                print("Invalid username!")

    def add_fruit_to_menu(self, fruit):
        self.menu.append(fruit)

    def show_menu(self):
        print("  \n Maavana mane Menu ")
        print("="*50)
        for idx, fruit in enumerate(self.menu, start=1):
            print(f"{idx}. {fruit.show_brief()}")
        print("="*50)

    def show_all_fruit_descriptions(self):
        print("\n Hannugalu - All Fruit Descriptions")
        print("="*50)
        for idx, fruit in enumerate(self.menu, start=1):
            print(f"{idx}. {fruit.show_description()}")

    def show_fruit_description(self, index):
        if 0 <= index < len(self.menu):
            print(self.menu[index].show_description())
        else:
            print("Invalid fruit selection!")

    def add_to_cart(self, index, quantity=1):
        if 0 <= index < len(self.menu):
            fruit = self.menu[index]
            for _ in range(quantity):
                self.cart.append(fruit)
                self.total += fruit.price
            print(f"{quantity}x {fruit.name} added to cart.")
            self.notifier.send_message(f" {self.user.username} added {quantity}x {fruit.name} - ₹{fruit.price * quantity} to cart")
        else:
            print("Invalid fruit selection!")

    def remove_from_cart(self, index):
        if 0 <= index < len(self.cart):
            fruit = self.cart.pop(index)
            self.total -= fruit.price
            print(f"{fruit.name} removed from cart.")
        else:
            print("Invalid cart item!")

    def add_to_wishlist(self, index):
        if 0 <= index < len(self.menu):
            fruit = self.menu[index]
            if self.user.add_to_wishlist(fruit):
                print(f"{fruit.name} added to wishlist.")
                self.notifier.send_message(f"{self.user.username} added {fruit.name} to wishlist")
            else:
                print(f"{fruit.name} is already in your wishlist!")
        else:
            print("Invalid fruit selection!")

    def show_cart(self):
        print("\n Your Shopping Cart:")
        if not self.cart:
            print("Your cart is empty!")
        else:
            fruit_count = {}
            for fruit in self.cart:
                fruit_count[fruit.name] = fruit_count.get(fruit.name, 0) + 1
            
            for fruit_name, count in fruit_count.items():
                fruit_price = next(f.price for f in self.menu if f.name == fruit_name)
                print(f"- {fruit_name} x{count} - ₹{fruit_price * count}")
            print(f"\nTotal: ₹{self.total}")

    def search_fruit(self, keyword):
        print(f"\n Search Results for '{keyword}':")
        found_fruits = []
        for idx, fruit in enumerate(self.menu):
            if (keyword.lower() in fruit.name.lower() or 
                keyword.lower() in fruit.benefits.lower() or
                keyword.lower() in fruit.description.lower()):
                found_fruits.append((idx, fruit))
        
        if found_fruits:
            for idx, fruit in found_fruits:
                print(f"{idx + 1}. {fruit.show_brief()}")
                print(f"{fruit.description[:100]}...")
                print()
        else:
            print("Hann sikklilla guru!.")

    def apply_discount(self):
        """Apply discount based on total amount"""
        if self.total >= 200:
            discount = self.total * 0.1  # 10% discount
            self.total -= discount
            print(f"10% discount Maja maadu! You saved ₹{discount:.2f}")
            return discount
        return 0

    def send_otp(self):
        """Simulate sending OTP to user's phone"""
        otp = self.otp_system.generate_otp()
        print(f"\nOTP sent to {self.user.phone_number}")
        print(f"Your OTP is: {otp}")  # In real app, this would be sent via SMS
        self.notifier.send_message(f"OTP {otp} sent to {self.user.username}")
        return otp

    def process_payment(self, payment_method):
        """Process payment with OTP verification"""
        print(f"\nProcessing payment via {payment_method}")
        
        # Send OTP
        self.send_otp()
        
        # Get OTP from user
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            entered_otp = input("Enter the OTP sent to your phone: ")
            is_valid, message = self.otp_system.verify_otp(entered_otp)
            
            if is_valid:
                print(f"{message}")
                break
            else:
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"{message}. {remaining} attempts remaining.")
                else:
                    print("Maximum OTP attempts exceeded. Payment failed.")
                    return False
        
        if attempts >= max_attempts:
            return False
        
      
        print("Processing payment...")
        time.sleep(2)
        
        if payment_method == "UPI":
            upi_id = input("Enter UPI ID: ")
            print(f"Payment request sent to {upi_id}")
        elif payment_method in ["Debit Card", "Credit Card"]:
            card_number = input("Enter card number (last 4 digits): ")
            print(f"Processing {payment_method} ending in {card_number}")
        
        return True

    def checkout(self):
        if not self.cart:
            print("Your cart is empty!")
            return

        print("\nCheckout Summary:")
        self.show_cart()
        
        # Apply discount if eligible
        discount = self.apply_discount()
        
        print(f"\nFinal Total: ₹{self.total}")
        
        print("\n Payment Methods:")
        print("1. UPI")
        print("2. Debit Card")
        print("3. Credit Card")
        print("4. Cancel")
        
        choice = input("Choose payment method (1-4): ")
        payment_methods = {"1": "UPI", "2": "Debit Card", "3": "Credit Card"}
        
        if choice == "4":
            print("Checkout cancelled.")
            return
        
        if choice not in payment_methods:
            print("Saala keli Sneha kaledhukolla bedi.")
            return
        
        payment_method = payment_methods[choice]
        
      
        if self.process_payment(payment_method):
            
            order = {
                'id': self.order_counter,
                'items': self.cart.copy(),
                'total': self.total,
                'payment_method': payment_method,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'discount': discount
            }
            
            self.user.add_to_order_history(order)
            self.order_counter += 1
            
            print("Payment successful!, Order confirmed.")
            print(f"Order ID: {order['id']}")
            print("Enjoy Your fruit in 2-3 hours!")
            
            self.notifier.send_message(f"{self.user.username} completed order #{order['id']} - ₹{self.total}")
            
            # Clear cart
            self.cart.clear()
            self.total = 0
        else:
            print("Payment failed. Please try again.")

    def show_recommendations(self):
        """Show personalized fruit recommendations"""
        print("\n Recommended for You:")
        seasonal_fruits = [f for f in self.menu if "summer" in f.season.lower() or "all year" in f.season.lower()]
        
        if seasonal_fruits:
            for fruit in seasonal_fruits[:3]:  # Show top 3
                print(f"{fruit.name} - ₹{fruit.price}")
                print(f"    {fruit.benefits}")
                print()
        else:
            print("Try our fresh Apple - perfect for any season!")

def main():
    bot_token = '8103048894:AAGjUYc-bp9makKgbqP1Jx6_S4_C23Y_FJY'
    chat_id = 1138856980    # ''
    notifier = TelegramNotifier(bot_token, chat_id)
    
    store = Maavana_mane(notifier)
    fruits_data = [
        Fruit("Apple", 40, "Rich in fiber, supports heart health, aids digestion", 
              "Crisp and sweet red apples, perfect for snacking or cooking",
              "Fiber: 4g, Vitamin C: 14% DV, Potassium: 6% DV per 100g",
              "Himachal Pradesh, India", "October - March"),
        
        Fruit("Banana", 20, "Energy booster, rich in potassium, aids muscle function",
              "Fresh yellow bananas, naturally sweet and creamy",
              "Potassium: 358mg, Vitamin B6: 20% DV, Vitamin C: 15% DV per 100g",
              "Kerala, India", "All year round"),
        
        Fruit("Mango", 50, "Boosts immunity, rich in vitamins A & C, antioxidants",
              "Sweet and juicy Alphonso mangoes, the king of fruits",
              "Vitamin A: 54% DV, Vitamin C: 60% DV, Folate: 6% DV per 100g",
              "Maharashtra, India", "March - June"),
        
        Fruit("Pineapple", 60, "Anti-inflammatory, aids digestion, rich in bromelain",
              "Fresh tropical pineapple, sweet with a tangy twist",
              "Vitamin C: 79% DV, Manganese: 76% DV, Bromelain: Natural enzyme per 100g",
              "Kerala, India", "December - February"),
        
        Fruit("Orange", 35, "High in Vitamin C, boosts immunity, hydrating",
              "Juicy sweet oranges, perfect for fresh juice or eating",
              "Vitamin C: 92% DV, Folate: 8% DV, Calcium: 5% DV per 100g",
              "Nagpur, India", "November - February"),
        
        Fruit("Grapes", 80, "Antioxidants, heart health, natural sugars for energy",
              "Sweet seedless grapes, perfect for snacking",
              "Vitamin K: 18% DV, Vitamin C: 4% DV, Antioxidants: High per 100g",
              "Maharashtra, India", "November - February")
    ]
    
    for fruit in fruits_data:
        store.add_fruit_to_menu(fruit)
    
   
    print("Welcome to Maavana mane! Alias Thavrmane")
    store.register_user()
    
    while True:
        print("\n" + "="*50)
        print("Maavana mane - MAIN MENU")
        print("="*50)
        print("1. View Menu")
        print("2. View All Fruit Descriptions")
        print("3. View Specific Fruit Description")
        print("4. Add to Cart")
        print("5. Add to Wishlist")
        print("6. View Wishlist")
        print("7. Search Fruits")
        print("8. View Cart")
        print("9. Remove from Cart")
        print("10.Checkout")
        print("11.View Recommendations")
        print("12.Order History")
        print("13.Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-13): ")
        

        if choice == '1':
            store.show_menu()
            
        elif choice == '2':
            store.show_all_fruit_descriptions()
            
        elif choice == '3':
            store.show_menu()
            index = int(input("Enter fruit number for description: ")) - 1
            store.show_fruit_description(index)
            
        elif choice == '4':
            store.show_menu()
            index = int(input("Enter fruit number to add to cart: ")) - 1
            quantity = int(input("Enter quantity: "))
            store.add_to_cart(index, quantity)
            
        elif choice == '5':
            store.show_menu()
            index = int(input("Enter fruit number to add to wishlist: ")) - 1
            store.add_to_wishlist(index)
            
        elif choice == '6':
            store.user.show_wishlist()
            
        elif choice == '7':
            keyword = input("Enter fruit name or keyword to search: ")
            store.search_fruit(keyword)
            
        elif choice == '8':
            store.show_cart()
            
        elif choice == '9':
            store.show_cart()
            if store.cart:
                    index = int(input("Enter item number to remove: ")) - 1
                    store.remove_from_cart(index)
            
        elif choice == '10':
            store.checkout()
            
        elif choice == '11':
            store.show_recommendations()
            
        elif choice == '12':
            store.user.show_order_history()
        elif choice == '13':
            print("Maavana mane ge Vist hakiddhukke thumba santhosha!")
            print("Henn keldhe hann thakondidhukku thumba dhanyavadhagalu!")
            break
            
        else:
            print("Sariyag number Hottho lo : 1-13.")
main()