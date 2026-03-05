import re

file = open("output.txt", "r")
content = file.read()
powers = [str(2 ** i) for i in range(64, -1, -1)]

print("Степень    Значение                 Количество")
for num, value in enumerate(powers[::-1]): 
    count = len(re.findall(value, content))
    print(f"2^{num: <8} {value: <25} {count}")

for p in powers:
    content = re.sub(p, "", content)

outputFile = open("output2.txt", "w")
outputFile.write(content)
file.close()
