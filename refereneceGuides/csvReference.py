import csv


# Create csv file
# use csv.writer(file) to write rows
with open(r'.\refereneceGuides\test.csv','w', newline='') as f:
    writer = csv.writer(f)

    writer.writerow([1,2,3])
    writer.writerow([10,29,3])

# read csv file
# csv.reader(file) to read rows
with open(r'.\refereneceGuides\test.csv','r') as f:
    r = csv.reader(f, delimiter=',')

    for row in r:
        print(",".join(row))