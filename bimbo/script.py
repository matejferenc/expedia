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
        try:
            sum += (math.log(p[i] + 1) - math.log(a[i] + 1)) ** 2
        except ValueError:
            print p[i]
            print a[i]
            print (math.log(p[i] + 1) - math.log(a[i] + 1))
            print (math.log(p[i] + 1) - math.log(a[i] + 1)) ** 2
    return math.sqrt(sum / n)

def run_solution():
    start_time = time.time()
    print('Preparing...')
    f = open("../../bimbo/train.csv", "r")
    f.readline()
    hits = defaultdict(int)
    total = 0
    estimated = 0
    notEstimated = 0
    
    p = []
    a = []
    
    client_product_count = defaultdict(lambda: defaultdict(int))

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
            producto_id = int(arr[5])
            venta_uni_hoy = int(arr[6])
            venta_hoy = arr[7]
            dev_uni_proxima = arr[8]
            dev_proxima = arr[9]
            demanda_uni_equil = int(arr[10])
        
        if validate == 1 and total % N0 == N1:
            continue
        
        client_product_count[(cliente_id, producto_id)][semana] += demanda_uni_equil

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
            producto_id = int(arr[5])
            venta_uni_hoy = int(arr[6])
            venta_hoy = arr[7]
            dev_uni_proxima = int(arr[8])
            dev_proxima = arr[9]
            demanda_uni_equil = int(arr[10])
            if total % N0 != N1:
                continue
            a.append(demanda_uni_equil)
#             p.append(math.fabs(venta_uni_hoy - dev_uni_proxima))
#             if venta_uni_hoy - dev_uni_proxima < 0:
#                 print "venta_uni_hoy - dev_uni_proxima < 0"
        else:
            id = int(arr[0])
            semana = int(arr[1])
            agencia_id = arr[2]
            canal_id = arr[3]
            ruta_sak = arr[4]
            cliente_id = arr[5]
            producto_id = arr[6]

            
        if (cliente_id, producto_id) in client_product_count:
            counts = client_product_count[(cliente_id, producto_id)]
            n = len(counts)
            sum = 0
            for i in range(0, n - 1):
                sum += counts[i]
            p.append(sum / n)
            estimated += 1
        else:
            p.append(0)
            notEstimated += 1

        
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
        print("estimated: %f" % (estimated))
        print("not estimated: %f" % (notEstimated))
    # <<< validation

run_solution()