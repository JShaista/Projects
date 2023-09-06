import csv
#Place the csv file in the same location/folder as the script
file = open("earthquakes.csv")
csvreader = csv.reader(file)
next(csvreader)
count = 0
for row in csvreader:
  # convert string to float
  if 4.0<=float(row[4]):
    count = count + 1

print("%d entries have magnitude greater than 4.0" %count)
file.close()