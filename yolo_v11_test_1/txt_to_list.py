txt_file = 'curation_1_8_only_a4.txt'

with open(txt_file, 'r', encoding='UTF-8') as f:
    lines = f.readlines()

for i in lines:
    line = i.split('=>')[-1]
    line_strip = line.strip()
    print(line_strip)