def get_int(prompt: str):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Enter a valid number!")

def get_float(prompt: str):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Enter valid marks!")
