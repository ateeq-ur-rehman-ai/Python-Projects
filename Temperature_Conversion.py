def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit
    
def fahrenheit_to_celsius(fahrenheit):
    celsius = (fahrenheit - 32) * 5/9
    return celsius 
    
def temp():
    print("--------TEMPERATURE CONVERSION--------")
    print("-----xx-----xx-----xx-----")
    
    while True:
        print("CHOOSE AN OPTION: ")
        print("1. CELSIUS TO FAHRENHEIT: ")
        print("2. FAHRENHEIT TO CELSIUS: ")
        print("3. STOP: ")
        option = input("Enter option (1, 2, 3): ")
        
        if option == "1":
            celsius = float(input("Enter temperature in Celsius: ")) 
            fahrenheit = celsius_to_fahrenheit(celsius)
            print(f"{celsius:.2f} Celsius is equal to {fahrenheit:.2f} Fahrenheit")
        elif option == "2":
            fahrenheit = float(input("Enter temperature in Fahrenheit: ")) 
            celsius = fahrenheit_to_celsius(fahrenheit)
            print(f"{fahrenheit:.2f} Fahrenheit is equal to {celsius:.2f} Celsius")
        elif option == "3":
            print('STOP')
            break
        else:
            print("PLEASE TRY AGAIN: ")

temp()