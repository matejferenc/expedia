import datetime
import time
from heapq import nlargest
from operator import itemgetter
from collections import defaultdict
import math

# validation ###############
validate = 1  # 1 - validation, 0 - submission
N0 = 10       # total number of parts
N1 = 2        # number of part
#--------------------------


def rmsle(p, a):
    if len(p) != len(a):
        raise Exception('lengths of lists do not match in rmsle')
    n = len(p)
    sum = 0
    for i in range(0, n - 1):
        sum += (math.log(p[i] + 1) - math.log(a[i] + 1)) ** 2
    return math.sqrt(sum / n)

def run_solution():
    start_time = time.time()
    print('Preparing...')
    f = open("../../bimbo/train.csv", "r")
    f.readline()
    hits = defaultdict(int)
    total = 0
    
    p = []
    a = []

    # Calc counts
    while 1:
        line = f.readline().strip()
        total += 1
        if total % 10000000 == 0:
            print('Read {} lines...'.format(total))
        if line == '':
            break
        arr = line.split(",")
        if validate == 1:
            semana = int(arr[0])
            agencia_id = arr[1]
            canal_id = arr[2]
            ruta_sak = arr[3]
            cliente_id = int(arr[4])
            producto_id = arr[5]
            venta_uni_hoy = int(arr[6])
            venta_hoy = arr[7]
            dev_uni_proxima = arr[8]
            dev_proxima = arr[9]
            demanda_uni_equil = int(arr[10])
        
        if validate == 1 and cliente_id % N0 == N1:
            continue

    f.close()
    ###########################

    
    
    if validate == 1:
        print('Validation...')
        f = open("../../bimbo/train.csv", "r")
    else:
        print('Generate submission...')
        f = open("../../bimbo/test.csv", "r")
    now = datetime.datetime.now()
    path = 'submission_' + str(now.strftime("%Y-%m-%d-%H-%M")) + '.csv'
    out = open(path, "w")
    f.readline()
    total = 0
    totalv = 0
    out.write("id,Demanda_uni_equil\n")

    while 1:
        line = f.readline().strip()
        total += 1
        if total % 1000000 == 0:
            print('Write {} lines...'.format(total))

        if line == '':
            break

        arr = line.split(",")
        if validate == 1:
            semana = int(arr[0])
            agencia_id = arr[1]
            canal_id = arr[2]
            ruta_sak = arr[3]
            cliente_id = int(arr[4])
            producto_id = arr[5]
            venta_uni_hoy = int(arr[6])
            venta_hoy = arr[7]
            dev_uni_proxima = int(arr[8])
            dev_proxima = arr[9]
            demanda_uni_equil = int(arr[10])
            if cliente_id % N0 != N1:
                continue
            a.append(demanda_uni_equil)
            p.append(venta_uni_hoy - dev_uni_proxima)
        else:
            id = int(arr[0])
            semana = int(arr[1])
            agencia_id = arr[2]
            canal_id = arr[3]
            ruta_sak = arr[4]
            cliente_id = arr[5]
            producto_id = arr[6]


        
#         out.write(str(id) + ',')


        out.write("\n")
    out.close()
    print("Completed in %s seconds" % (time.time() - start_time))
    # validation >>>
    scores = 0.0
    classified = 0
    if validate == 1:
        print("")
        print(" validation")
        print("----------------------------------------------------------------")
        print("RMSLE = %8.4f " % (rmsle(p, a)))
    # <<< validation

run_solution()