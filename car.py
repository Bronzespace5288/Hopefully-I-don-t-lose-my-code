import random
import time


def Auction():
    print("Welcome to the central auction house!")
    print("\nWhich auction house would you like to go to?")
    print("1. Discount rides")
    print("2. Luxury cars")
    print("3. American classics")
    print("4. Hyper cars")
    print("5. Japanese classics")
    print("6. German manufacturers")


    choice = input("Enter your choice (1-6): ")


    cars = {
        '1': [
            ("2017 Ford Focus Titanium", 9000),
            ("2019 Subaru Outback Premium", 17000),
            ("2015 Chevrolet Malibu LT", 8000),
            ("2018 Hyundai Elantra SEL", 13000),
            ("2016 Honda Civic LX", 13000),
            ("2018 Toyota Camry SE", 15000)
        ],
        '2': [
            ("2017 BMW 5 Series 540i", 25000),
            ("2018 Audi A6 3.0 TFSI", 23000),
            ("2016 Mercedes-Benz E-Class E350", 21000),
            ("2019 Lexus ES 350", 27000),
            ("2018 Cadillac CTS 3.6L", 19000),
            ("2017 Jaguar XF 35t", 22000)
        ],
        '3': [
            ("1967 Chevrolet Camaro SS", 35000),
            ("1969 Ford Mustang Mach 1", 32000),
            ("1957 Chevrolet Bel Air", 40000),
            ("1965 Pontiac GTO", 30000),
            ("1970 Dodge Challenger R/T", 38000),
            ("1966 Ford Shelby GT350", 55000)
        ],
        '4': [
            ("2018 Bugatti Chiron", 2500000),
            ("2020 McLaren Speedtail", 2000000),
            ("2021 Ferrari SF90 Stradale", 1700000),
            ("2019 Pininfarina Battista", 2200000),
            ("2021 Rimac C_Two", 2000000),
            ("2018 Aston Martin Valkyrie", 3000000)
        ],
        '5': [
            ("1989 Nissan GT-R R32", 30000),
            ("1991 Toyota Supra MK3 Turbo", 28000),
            ("1973 Datsun 240Z", 25000),
            ("1988 Honda CRX Si", 18000),
            ("1992 Mazda RX-7", 22000),
            ("1985 Toyota Celica GT-S", 20000)
        ],
        '6': [
            ("1985 Mercedes-Benz 500SL", 22000),
            ("1972 BMW 2002tii", 28000),
            ("1969 Porsche 911 T", 45000),
            ("1984 Audi Quattro", 20000),
            ("1970 Mercedes-Benz 280SE", 25000),
            ("1967 BMW 1600", 22000)
        ]
    }


    if choice in cars:
        print("\nAvailable cars:")
        for i, (car, price) in enumerate(cars[choice], 1):
            print(f"{i}. {car}, starting bid: ${price}")
       
        car_choice = int(input("\nWhich car would you like to bid on? (Enter the number): ")) - 1
        if 0 <= car_choice < len(cars[choice]):
            car, current_bid = cars[choice][car_choice]
            print(f"\nBidding starts for {car} at ${current_bid}")
           
            auction_duration = 60  # 60 seconds
            start_time = time.time()
            your_last_bid = 0


            while time.time() - start_time < auction_duration:
                remaining_time = int(auction_duration - (time.time() - start_time))
                print(f"\nCurrent bid: ${current_bid} | Time remaining: {remaining_time} seconds")
               
                try:
                    your_bid = int(input("Enter your bid (or press Enter to skip): "))
                    if your_bid > current_bid:
                        current_bid = your_bid
                        your_last_bid = your_bid
                        print(f"You are the highest bidder at ${current_bid}")
                    elif your_bid <= current_bid:
                        print("Your bid must be higher than the current bid.")
                except ValueError:
                    pass  # User skipped bidding


                # Simulate other bidders
                if random.random() < 0.3:  # 30% chance of competitor bidding
                    competitor_bid = current_bid + random.randint(100, 1000)
                    if competitor_bid > current_bid:
                        current_bid = competitor_bid
                        print(f"A competitor has bid ${current_bid}")


                time.sleep(1)  # Wait for 1 second before the next bid


            print("\nAuction ended!")
            if your_last_bid == current_bid:
                print(f"Congratulations! You won the auction for {car} at ${current_bid}")
               
                # Add the chance to win the car for free
                free_car_roll = random.randint(1, 100)
                win_threshold = 10


                print("\nYou have a chance to win the car for free!")
                print("Rolling the dice...")
                time.sleep(2)  # Add a bit of suspense
               
                if free_car_roll <= win_threshold:
                    print(f"Incredible luck! You rolled a {free_car_roll}.")
                    print("You've won the car for free! No payment needed!")
                else:
                    print(f"You rolled a {free_car_roll}. Close, but not quite lucky enough for a free car.")
                    print(f"You'll need to pay the winning bid of ${current_bid}.")
            else:
                print(f"The auction for {car} ended at ${current_bid}. You did not win this time.")


        else:
            print("Invalid car selection.")
    else:
        print("Invalid choice. Please select a number between 1 and 6.")


Auction()
