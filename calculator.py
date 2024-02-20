# function definition

def calculate_basic_math(num1 , operator, num2):      
    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        if num1 != 0 and num2 != 0:
            result = num1 / num2
        else:
            result = "The answer is undefined!\nPlease try agane with another number."
      
    else:    
        result = "The operator is not valid!"

    print(result)       


# function call
try: 
    num1 = int(input("Please Enter Number1: "))
    operator = input("Please Enter the operator(+ - * /): ")
    num2 = int(input("Please Enter Number2: "))
except:
    print("Something went wrong!")    
else:
    calculate_basic_math(num1, operator, num2)
