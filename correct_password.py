def check_password(input_password):
 input_password = input("enter your password: ")

correct_password = "secure123"
if input_password == correct_password:
        return True
else:
        return False
