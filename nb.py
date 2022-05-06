import pandas as pd
import math
import StratifiedCV as scv

def read_csv(filename):
  # returns an array
  data = pd.read_csv(filename, header=None)
  return data.values.tolist()

def calc_mean(training_data):
  mean_list = []
  for i in range(len(training_data[0]) - 1):
    mean_list.append([0, 0])   # storing [mean yes, mean no]

  #print(mean_list)
  mean_count = 0
  for training_row in training_data:
    if training_row[-1] == 'yes': mean_count += 1
    for index, training_col in enumerate(training_row):
      #print(index, training_col)
      if index == len(training_row) -1: break
      
      if training_row[-1] == 'yes': 
        mean_list[index][0] += float(training_col)
      elif training_row[-1] == 'no':
        mean_list[index][1] += float(training_col)
    #print(mean_list)
  #print(mean_count)
  #print(mean_list)
  for mean in mean_list:
    mean[0] /= mean_count
    mean[1] /= (len(training_data) - mean_count)
  mean_list.append(mean_count)
  return mean_list
      
def calc_std(mean_list, training_data):
  
  std_list = []
  std_count = 0
  for i in range(len(training_data[0]) - 1):
    std_list.append([0, 0])   # storing [std yes, std no]
  
  for training_row in training_data:
    if training_row[-1] == 'yes': std_count += 1
    for index, training_col in enumerate(training_row):
      if index == len(training_row) -1: break
      
      if training_row[-1] == 'yes': 
        std_list[index][0] += ((float(training_col) - mean_list[index][0]) ** 2)
      elif training_row[-1] == 'no':
        std_list[index][1] += ((float(training_col) - mean_list[index][1]) ** 2)
  
  for std in std_list:
    std[0] = (std[0] / (std_count - 1)) ** 0.5
    std[1] = (std[1] / (len(training_data) - (std_count - 1))) ** 0.5
    
  return std_list
  

def calc_pdf(mean, std, test_col):
  pdf_formula_1 = 1 / (std * ((2 * math.pi) ** 0.5))
  #print(pdf_formula_1)
  pdf_formula_2 = (((float(test_col) - mean) ** 2) / (2 * (std ** 2))) * -1
  #print(pdf_formula_2)
  pdf = float(pdf_formula_1 * math.pow(math.e, pdf_formula_2))
  return pdf
  
def predict(test_row, training_data, mean_list, std_list):

  pdf_yes = mean_list[-1] / len(training_data)
  pdf_no = (len(training_data) - mean_list[-1]) / len(training_data)
  for index, test_col in enumerate(test_row):
    if index == len(test_row) -1: break
    mean_yes, mean_no, std_yes, std_no = mean_list[index][0], mean_list[index][1], std_list[index][0], std_list[index][1]

    pdf_yes *= calc_pdf(mean_yes, std_yes, test_col)
    pdf_no *= calc_pdf(mean_no, std_no, test_col)
  #print(pdf_yes, pdf_no)
  return 'no' if pdf_no > pdf_yes else 'yes'
    

def check_accuracy(target_output, testing_data):
    correct = 0
    for i in range(len(target_output)):
        if target_output[i] == testing_data[i][-1]: correct += 1
    # print(correct / len(target_output))
    return correct * 100 / len(target_output) 
    


def confusion_matrix(output, testing_data):
  # print(output)
  tp, tn, fp, fn = 0, 0, 0, 0
  for i in range(len(output)):
    if output[i] == testing_data[i][-1] and output[i] == 'yes':
      tp += 1
    elif output[i] == testing_data[i][-1] and output[i] == 'no':
      tn += 1
    elif output[i] != testing_data[i][-1] and output[i] == 'yes':
      fn += 1
    elif output[i] != testing_data[i][-1] and output[i] == 'no':
      fp += 1
  return (tp, tn, fp, fn)

def calc_performance(tp, tn, fp, fn):

  precision = round(tp / (tp + fp) * 100, 2)
  recall = round(tp / (tp + fn) * 100, 2)
  f1 = round(2 * precision * recall / (precision + recall), 2)
  print(f'Precision: {precision}, Recall: {recall}, F1: {f1}')
  
def classify_nb(file_path):
    stratified_folds = scv.run(file_path)
    # print(stratified_folds)
    # print(cfs)
    tp, tn, fp, fn = 0, 0, 0, 0
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
        
        mean_list = calc_mean(training_data)
        # print(mean_list)
        # print()
        std_list = calc_std(mean_list, training_data)
        # print(std_list)
        output = []
        # print(len(testing_data))
        for row in testing_data:
            output += [predict(row, training_data, mean_list, std_list)]
        accuracy = check_accuracy(output, testing_data)
        matrix = confusion_matrix(output, testing_data)
        tp += matrix[0]
        tn += matrix[1]
        fp += matrix[2]
        fn += matrix[3]
            
            
        

        # print(output)
        # print(accuracy)
        total_accuracy += accuracy
    
    # average total_accuracy
    total_accuracy /= folds
    print(f'True positive: {tp}, True negative: {tn}, False positive: {fp}, False negative: {fn}')
    calc_performance(tp, tn, fp, fn)
    return round(total_accuracy, 2)

if __name__ == "__main__":
  #p = [[0, 0]] * 3
  #print(p)
  #p[0][1] = 1
  #print(p)
  print("NB without CFS")
  print(classify_nb("pima.csv"))
  print()
  print("NB with CFS")
  print(classify_nb("pima-CFS.csv"))