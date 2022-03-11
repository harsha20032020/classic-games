my_file = open("list.txt", "r")
content = my_file.read()
character_list=[]
timestamp_list=[]
# 1st word of each line to be inserted to character_list and the 2nd word of each line to be inserted to timestamp_list
for line in content.splitlines():
    character_list.append(line.split()[0])
    timestamp_list.append(line.split()[1])

print(timestamp_list[2])
