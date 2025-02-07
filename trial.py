import csv

def append_file(writer, headers, data):
    file_exists = False
    try:
        with open(writer, 'r') as csvfile:
            file_exists = bool(csvfile.readline())
    except FileNotFoundError:
        pass
    
    with open(writer, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        if not file_exists:
            csv_writer.writerow(headers)
        csv_writer.writerow(data)
        
append_file("new.csv", ["One", "Two", "Three"], [1,2,3])
append_file("new.csv", ["One", "Two", "Three"], [1,2,3])
append_file("new.csv", ["One", "Two", "Three"], [1,2,3])
append_file("new.csv", ["One", "Two", "Three"], [1,2,3])