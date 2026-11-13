print("Choose shape: rectangle, circle, triangle") 
shape = input("Enter shape: ") 
if shape == "rectangle": 
 length = float(input("Enter length: ")) 
 width = float(input("Enter width: ")) 
 area = length * width 
elif shape == "circle": 
 radius = float(input("Enter radius: ")) 
 area = 3.14159 * radius * radius 
elif shape == "triangle": 
 base = float(input("Enter base: ")) 
 height = float(input("Enter height: ")) 
 area = 0.5 * base * height 
else: 
 area = "Invalid shape" 
print("Area:", area)
