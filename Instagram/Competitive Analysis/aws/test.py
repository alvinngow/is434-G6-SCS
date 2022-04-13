import json

file_name = '261.json'
with open(file_name, "r") as f:
    data1 = json.load(f)

file_name2 = '1045.json'
with open(file_name2, "r") as f:
    data2 = json.load(f)

file_name3 = '1481.json'
with open(file_name3, "r") as f:
    data3 = json.load(f)

print(len(data1))
print(len(data2))
print(len(data3))

print(len(data1) + len(data2) + len(data3))

# # sample output
# for i in data858[-1]:
#     print(i.get("DetectedText"))
# print(data261[0])