import re
import numpy

from frameworks import START_TEST, END_TEST

def log_parser(file_path):
    with open(file_path) as f:
         cases_string = f.read()

    case_str_tokens = cases_string.split('\n')
    
    test_info = []
    READ_STRING = False
    for str_token in case_str_tokens:
        if READ_STRING and str_token!=END_TEST and str_token!=START_TEST:
            test_info.append(str_token)
        if str_token == START_TEST:
            READ_STRING = True
        if str_token == END_TEST:
            READ_STRING = False


    
    

#    case_list = re.split(START_TEST + "|" + END_TEST,cases_string)

    #pop last item from the list because extra info not needed at this point
#    case_list.pop()

    results_list = []
    for info in test_info:
        param_info = info.split(" ")[0]
        params = re.findall("\d+",param_info)
        params = (int(params[0]),int(params[1]))
        method_info = info.split(" ")[0]
        method_name=re.findall("\w+",method_info)[0]
        result_info = info.split("...")[1]
#        result_info = re.findall("\w+",result_info)
        if 'ok' in result_info:
            results_list.append((method_name,params,'ok'))
        elif 'FAIL' in result_info:
            results_list.append((method_name,params,'FAIL'))
        elif 'skipped' in result_info:
            results_list.append((method_name,params,'skipped'))
    method_set = list(set([result[0] for result in results_list]))
    index_keys = {}
    for i in range(0,len(method_set)):
        index_keys[method_set[i]] = i

    dimension_1 = max([int(result[1][0]) for result in results_list])+1
    dimension_2 = max([int(result[1][1]) for result in results_list])+1
       
    dimension_3 = len(index_keys)
    matrix = numpy.zeros([dimension_1,dimension_2,dimension_3], dtype=bool)

    for result in results_list:
        method_index = index_keys[result[0]]
        page_1 = result[1][0]
        page_2 = result[1][1]
        value =  (result[2] == 'ok')
        matrix[page_1,page_2,method_index] = value
        if page_1 == 0 or page_2 == 0:
            pass
    return matrix

def matrix_equality(matrix, operators):
    (M, N, total_measurments) = matrix.shape
    result = numpy.zeros([M,N],dtype=bool)
    if total_measurments -1 != len(operators):
        raise TypeError
    operators.insert(0,'or')

    for m in range(0,total_measurments):
        operator = operators.pop()
        if operator == 'or':
             numpy.logical_or(result,matrix[:,:,m],result)
        if operator == 'and':
             numpy.logical_and(result,matrix[:,:,m],result)

    return result

def LCSLength(matrix):
    (M,N) = matrix.shape
    C = numpy.zeros([M,N],dtype=int)

    for i in range(1,M):
        for j in range(1,N):
            if matrix[i,j]:
                C[i,j]=C[i-1,j-1] + 1
            else:
                C[i,j]=max(C[i,j-1], C[i-1,j])
    return C

def backtrack(C,R):
    if C.shape != R.shape:
        raise TypeError
    (m,n) = C.shape

    X=range(1,m+1)
    Y=range(1,n+1)

    return _backtrack(C,m-1,n-1,R)

def _backtrack(C,i,j,R):
    if i == 0 or j == 0:
        return []
    elif R[i,j]:
        return _backtrack(C,i-1,j-1,R) + [i]
    else:
        if C[i,j-1] > C[i-1,j]:
            return _backtrack(C, i, j-1,R)
        else:
            return _backtrack(C, i-1, j,R)


    

    
