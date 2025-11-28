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
            
def get_non_empty_string(prompt: str):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            print("Input cannot be empty. Please enter a valid value")
