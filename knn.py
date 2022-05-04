import pandas as pd
import StratifiedCV as scv
# all_training_data = []

def read_csv(filename):
  # returns an array
  data = pd.read_csv(filename, header=None)
  return data.values.tolist()

def check_data_type():
  pass

def calc_dist(training_data, test_row):
#   print(cfs)
  dist = []
  for index, row in enumerate(training_data):
    euclidean = 0
    for i in range(len(test_row) -1):    # remember to change back to len(test_row)
    #   print(test_row[i], row[i])
      
    #   check_data_type(test_row[i])
      diff = (float(test_row[i]) - float(row[i])) ** 2
      euclidean += diff
    euclidean = euclidean ** 0.5
    dist += [(euclidean, index)]
  return dist

def predict(dist_array, k, training_data):
  k_nearest_neighbour = get_k_nearest(dist_array, training_data, k)
  check_class = {"no": 0, "yes": 0}
  for neighbour in k_nearest_neighbour:
    check_class[neighbour[-1]] += 1
  #print(check_class)
  return 'no' if check_class['no'] > check_class['yes'] else 'yes'

def get_k_nearest(dist_array, training_data, k):
  # find the k nearest neighbour
  sorted_dist = sorted(dist_array, key=lambda x: x[0]) # sort by the distance
  #print(sorted_dist)
  k_nearest = sorted_dist[ : k]
  neighbours = []
  for neighbour in k_nearest:
    neighbours += [training_data[neighbour[1]]]
  #print(neighbours)
  return neighbours
    
def check_accuracy(target_output, testing_data):
    correct = 0
    for i in range(len(target_output)):
        if target_output[i] == testing_data[i][-1]: correct += 1
    # print(correct / len(target_output))
    return correct * 100 / len(target_output)


def classify_nn(file_path, k):
    stratified_folds = scv.run(file_path)
    # print(stratified_folds)
    # print(cfs)
  
    # for each fold
    folds = len(stratified_folds)
    total_accuracy = 0
    for fold in stratified_folds:
        testing_data = fold
        # rest of the folds
        training_data = []
        for each_fold in stratified_folds:
            if each_fold != fold:
                training_data += each_fold
        
        output = []
        # print(len(testing_data))
        for row in testing_data:
            # print(row)
            dist = calc_dist(training_data, row)
            output += [predict(dist, k, training_data)]#
        
        accuracy = check_accuracy(output, testing_data)
        # print(output)
        # print(accuracy)
        total_accuracy += accuracy
    
    # average total_accuracy
    total_accuracy /= folds
    # print(total_accuracy)
    return round(total_accuracy, 2)
        # print(output)
    # print(output)
    # return output
  

if __name__ == '__main__':
    print(classify_nn("pima.csv", 1))
    print(classify_nn("pima.csv", 5))

    print(classify_nn("pima-CFS.csv", 1))
    print(classify_nn("pima-CFS.csv", 5))