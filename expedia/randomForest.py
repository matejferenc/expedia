# coding: utf-8
#################################
#      Simple Validation        #
#################################
# contributors:
# ZFTurbo - idea, main part
# Kagglers - tuning, development
# Grzegorz Sionkowski - simple validation


import datetime
import time
from heapq import nlargest
from operator import itemgetter
from collections import defaultdict
from sklearn.ensemble import RandomForestClassifier


# validation ###############
validate = 1  # 1 - validation, 0 - submission
N0 = 10       # total number of parts
N1 = 3        # number of part
#--------------------------

def run_solution():
    start_time = time.time()
    print('Preparing arrays...')
    f = open("../../kaggle/expedia_data/train.csv", "r")
    f.readline()
    best_hotels_od_ulc = defaultdict(lambda: defaultdict(int))
    best_hotels_search_dest = defaultdict(lambda: defaultdict(int))
    best_hotels_search_dest1 = defaultdict(lambda: defaultdict(int))
    best_hotel_country = defaultdict(lambda: defaultdict(int))
    hits = defaultdict(int)
    tp = defaultdict(float)

    popular_hotel_cluster = defaultdict(int)
    total = 0
    
    rf = RandomForestClassifier(n_estimators=100)

    # Calc counts
    while 1:
        line = f.readline().strip()
        total += 1
        if total % 1 == 0:
            print('Read {} lines...'.format(total))
        if line == '':
            break
        if total % 1000 == 0:
            break
        arr = line.split(",")
        book_year = int(arr[0][:4])
        book_month = int(arr[0][5:7])
        user_location_country = arr[3]
        user_location_city = arr[5]
        orig_destination_distance = arr[6]
        user_id = int(arr[7])
        is_package = int(arr[9])
        srch_destination_id = arr[16]
        is_booking = int(arr[18])
        hotel_continent = arr[20]
        hotel_country = arr[21]
        hotel_market = arr[22]
        hotel_cluster = arr[23]
        
        train = [[book_year, book_month, user_location_country, user_location_city,
                 is_package, srch_destination_id,
                 hotel_continent, hotel_country, hotel_market, hotel_cluster]]
        rf.fit(train, [is_booking])

        if validate == 1 and user_id % N0 == N1:
            continue

        append_0 = (book_year - 2012)*12 + book_month
        append_1 = ((book_year - 2012)*12 + (book_month - 12)) *  (3 + 12*is_booking)
        append_2 = 3 + 5.1*is_booking

        if user_location_city != '' and orig_destination_distance != '':
            best_hotels_od_ulc[(user_location_city, orig_destination_distance)][hotel_cluster] += append_0

        if srch_destination_id != '' and hotel_country != '' and hotel_market != '' and book_year != '':
            best_hotels_search_dest[(srch_destination_id, hotel_country, hotel_market, is_package)][hotel_cluster] += append_1

        if srch_destination_id != '':
            best_hotels_search_dest1[srch_destination_id][hotel_cluster] += append_1

        if hotel_country != '':
            best_hotel_country[hotel_country][hotel_cluster] += append_2

        popular_hotel_cluster[hotel_cluster] += 1

    f.close()
    ###########################
    if validate == 1:
        print('Validation...')
        f = open("../../kaggle/expedia_data/train.csv", "r")
    else:
        print('Generate submission...')
        f = open("../../kaggle/expedia_data/test.csv", "r")
    now = datetime.datetime.now()
    path = 'submission_' + str(now.strftime("%Y-%m-%d-%H-%M")) + '.csv'
    out = open(path, "w")
    f.readline()
    total = 0
    totalv = 0
    out.write("id,hotel_cluster\n")
    topclasters = nlargest(5, sorted(popular_hotel_cluster.items()), key=itemgetter(1))

    while 1:
        line = f.readline().strip()
        total += 1
        if total % 1000000 == 0:
            print('Write {} lines...'.format(total))

        if line == '':
            break
        
        if total % 1000 == 0:
            break

        arr = line.split(",")
        if validate == 1:
            book_year = int(arr[0][:4])
            book_month = int(arr[0][5:7])
            user_location_country = arr[3]
            user_location_city = arr[5]
            orig_destination_distance = arr[6]
            user_id = int(arr[7])
            is_package = int(arr[9])
            srch_destination_id = arr[16]
            is_booking = int(arr[18])
            hotel_continent = arr[20]
            hotel_country = arr[21]
            hotel_market = arr[22]
            hotel_cluster = arr[23]
            id = 0
            if user_id % N0 != N1:
                continue
            if is_booking == 0:
                continue
        else:
            id = arr[0]
            user_location_country = arr[4]
            user_location_city = arr[6]
            orig_destination_distance = arr[7]
            user_id = int(arr[8])
            is_package = int(arr[10])
            srch_destination_id = arr[17]
            hotel_continent = arr[19]
            hotel_country = arr[20]
            hotel_market = arr[21]
            is_booking = 1

        totalv += 1
        out.write(str(id) + ',')
        filled = []

        test = [[book_year, book_month, user_location_country, user_location_city,
                 is_package, srch_destination_id,
                 hotel_continent, hotel_country, hotel_market, hotel_cluster]]
        prediction = rf.predict(test)
        
        print(prediction[0])
        filled.append(prediction[0])
        if validate == 1:
            if prediction[0]==hotel_cluster:
                hits[len(filled)] +=1
        

        for i in range(len(topclasters)):
            if len(filled) == 5:
                break
            if topclasters[i][0] in filled:
                continue
            out.write(' ' + topclasters[i][0])
            filled.append(topclasters[i][0])
            if validate == 1:
                if topclasters[i][0]==hotel_cluster:
                    hits[len(filled)] +=1


        out.write("\n")
    out.close()
    print("Completed in %s seconds" % (time.time() - start_time))
    # validation >>>
    scores = 0.0
    classified = 0
    if validate == 1:
        for jj in range(1,6):
            scores +=  hits[jj]*1.0/jj
            tp[jj] = hits[jj]*100.0/totalv
            classified += hits[jj]
        misclassified = totalv-classified
        miscp = misclassified*100.0/totalv
        print("")
        print(" validation")
        print("----------------------------------------------------------------")
        print("position %8d %8d %8d %8d %8d %8d+" % (1,2,3,4,5,6))
        print("hits     %8d %8d %8d %8d %8d %8d " % (hits[1],hits[2],hits[3],hits[4],hits[5],misclassified))
        print("hits[%%]  %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f " % (tp[1],tp[2],tp[3],tp[4],tp[5],miscp))
        print("----------------------------------------------------------------")
        print("MAP@5 = %8.4f " % (scores*1.0/totalv))
    # <<< validation

run_solution()