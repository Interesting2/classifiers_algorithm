import pandas as pd

def read_csv(filename):
    data = pd.read_csv(filename)
    return data.values.tolist()

def write_to_csv(formatted_data):
    # write formatted_data to csv file called pima-folds.csv
    # print(formatted_data)
    # print(len(formatted_data))
    with open('pima-folds.csv', 'w') as f:
       for i in range(len(formatted_data)):
          f.write(str(formatted_data[i])) 

def format_data(stratified_folds):
    counter = 1

    test = 0
    formatted_data = ""
    for each_fold in stratified_folds:
        # print(len(each_fold))
        test += len(each_fold)
        formatted_data += "fold" + str(counter) + "\n"
        for row in each_fold:
            row_to_string = ",".join(list(map(str, row)))
            # print(",".join(row_to_string))
            # print(row_to_string)
            formatted_data += row_to_string + "\n"
        if counter != 10:
            formatted_data += "\n"
        counter += 1
    # print(test)
    write_to_csv(formatted_data)
    

def cross_validation(yes_class, no_class, num_data):
    stratified_folds = stratified_alt(yes_class, no_class, num_data)
    format_data(stratified_folds)
    # print(stratified_folds)
    return stratified_folds
    

def stratified_alt(yes_class, no_class, num_data):
    fold = 10
    print(len(yes_class), len(no_class))
    yes_num = len(yes_class) // fold
    no_num = len(no_class) // fold
    print(yes_num, no_num)

    yes_tracker, no_tracker = 0, 0
    stratified_folds = []
    for i in range(fold):
        each_fold = []

        for yes_row in range(yes_tracker, yes_num + yes_tracker):
            each_fold += [yes_class[yes_row]]
        yes_tracker += yes_num
        for no_row in range(no_tracker, no_num + no_tracker):
            each_fold += [no_class[no_row]]
        no_tracker += no_num
    
        stratified_folds.append(each_fold)
    print(yes_tracker, no_tracker)

    if yes_tracker != len(yes_class):
        for yes_row in range(yes_tracker, len(yes_class)):
            stratified_folds[yes_row % fold].append(yes_class[yes_row])
    if no_tracker != len(no_class):
        for no_row in range(no_tracker, len(no_class)):
            stratified_folds[no_row % fold].append(no_class[no_row])


    for i in stratified_folds:
        print(len(i))
    return stratified_folds


def stratified(yes_class, no_class, num_data):
    stratified_folds = []
    folds = 10
    mixed_data = []
    print(len(yes_class), len(no_class))
    min_length = min(len(yes_class), len(no_class))
    for (yes_row, no_row) in zip(yes_class, no_class):
        mixed_data.append(yes_row)
        mixed_data.append(no_row)


    print(len(mixed_data))
    equal_length = len(mixed_data) // folds
    # print(equal_length)
    
    counter = 0
    for i in range(folds):
        each_fold = []
        for j in range(counter, counter + equal_length):
            each_fold.append(mixed_data[j])
        # print(len(each_fold))
        counter += equal_length
        stratified_folds.append(each_fold)
    
    # print(len(mixed_data), counter)
    remaining = len(mixed_data) - counter

    continue_index = remaining % folds
    for num in range(remaining):
        stratified_folds[num % 10].append(mixed_data[counter + num])

    # for i in stratified_folds:
    #     print(len(i))

    
    tracker = continue_index
    if len(yes_class) == min_length:
        # print(len(no_class))
        # iterate no_class 
        print(min_length, len(no_class))
        for no_row in range(min_length, len(no_class)):
            # add to stratified_folds equally
            stratified_folds[tracker % folds].append(no_class[no_row])
            tracker += 1
    else:
        # iterate yes_class
        # print(len(yes_class))
        for yes_row in range(min_length, len(yes_class)):
            # add to stratified_folds equally
            stratified_folds[tracker % folds].append(yes_class[yes_row])
            tracker += 1
    
    for each_fold in stratified_folds:
        print(len(each_fold))
        # print(each_fold[-1], each_fold[0])
    return stratified_folds



def run(file_path):
    data = read_csv(file_path)
    # print(len(data))
    yes_class = []
    no_class = []
    for i in range(len(data)):
        # split into two sets
        if data[i][-1] == 'yes': yes_class.append(data[i])
        else: no_class.append(data[i])
    return cross_validation(yes_class, no_class, len(data) // 10);

    return 
if __name__ == '__main__':
    print("StratifiedCV: From main")
    run()
    # pass