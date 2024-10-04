import csv

def find_ratios(files_list):
    ratio_dict = {}
    for current in files:
        with open(current, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
                
            for line in csv_reader:
                try:
                    if line[0] == 'L1Bit':
                        continue
                    # Only selecting Prescale 1 L1Seeds
                    if line[2] != '1':
                        continue
                    # Rate cut-off
                    if float(line[3]) < 2000:
                        continue
                    # First file rates will be used as denominator
                    if (files.index(current)==0):
                        ratio_dict[line[1]] = float(line[3])
                    elif (ratio_dict[line[1]] == 0):
                        continue
                    else:
                        ratio_dict[line[1]] = float(line[3])/ratio_dict[line[1]]
                except IndexError:
                    pass

    new_dict = {}
    unchanged_list = []
    list_of_keys = []
    for key, value in ratio_dict.items():
        if value != 0:
            if value == 1:
                unchanged_list.append(key)
            else:
                new_dict[key] = value
                list_of_keys.append(key)
   
    new_dict = dict(sorted(new_dict.items(), key=lambda item:item[1]))
    list_of_keys.sort()    

    for i in list_of_keys:
        print(i)


if __name__ == '__main__':
    
    # Two files - ratio of rates will be calculated for most impacted rates 
    # above cutoff. Ratio = rates file 2 / rates file 1
    files = ['csv_Zeroing/fgbit1_Zeroing_Sp01356_359663_unpacked.csv',
            'csv_Zeroing/fgbit1_Zeroing_Sp01356_359663.csv']

    top_ten_rates = find_ratios(files)



