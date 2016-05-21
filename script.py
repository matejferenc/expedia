# coding: utf-8
__author__ = 'Ravi: https://kaggle.com/company'

import datetime
import math
from heapq import nlargest
from operator import itemgetter
from collections import defaultdict

# validation ###############
validate = 1  # 1 - validation, 0 - submission
N0 = 10       # total number of parts
N1 = 2        # number of part
#--------------------------

def r(x):
    if x == '':
        return None
    else:
        return round(float(x),1)

def run_solution():
    print('Preparing arrays...')
    f = open("../../expedia/train.csv", "r")
    f.readline()
    best_hotels_od_ulc = defaultdict(lambda: defaultdict(int))
    best_hotels_search_dest = defaultdict(lambda: defaultdict(int))
    best_hotels_search_dest1 = defaultdict(lambda: defaultdict(int))
    best_hotel_country = defaultdict(lambda: defaultdict(int))
    hits = defaultdict(int)
    tp = defaultdict(float)
    
    best_hotels_ulc_sdi = defaultdict(lambda: defaultdict(int))

    popular_hotel_cluster = defaultdict(int)
    total = 0
    
    distances = {}
    cities = {}
    best_hotels_ulc_uid_sdi = defaultdict(lambda: defaultdict(int))
    


    # Calc counts
    while 1:
        line = f.readline().strip()
        total += 1
        if total % 10000000 == 0:
            print('Read {} lines...'.format(total))
        if line == '':
            break
        arr = line.split(",")
        book_year = int(arr[0][:4])
        book_month = int(arr[0][5:7])
        user_location_city = arr[5]
        orig_destination_distance = arr[6]
        user_id = int(arr[7])
        is_package = int(arr[9])
        srch_destination_id = arr[16]
        is_booking = int(arr[18])
        hotel_country = arr[21]
        hotel_market = arr[22]
        hotel_cluster = arr[23]

        if validate == 1 and user_id % N0 == N1:
            continue

        append_0 = ((book_year - 2012)*12 + (book_month - 12))
        append_1 = append_0 *  (3 + 16*is_booking)
        append_2 = 3 + 5.1*is_booking

        if user_location_city != '' and orig_destination_distance != '':
            best_hotels_od_ulc[(user_location_city, orig_destination_distance)][hotel_cluster] += append_0

        if srch_destination_id != '' and hotel_country != '' and hotel_market != '' and book_year != '':
            best_hotels_search_dest[(srch_destination_id, hotel_country, hotel_market,is_package)][hotel_cluster] += append_1
 
        if srch_destination_id != '':
            best_hotels_search_dest1[srch_destination_id][hotel_cluster] += append_1
 
        if hotel_country != '':
            best_hotel_country[hotel_country][hotel_cluster] += append_2

        popular_hotel_cluster[hotel_cluster] += append_0


    f.close()
    ###########################
    if validate == 1:
        print('Enhancing...')
        f = open("../../expedia/train.csv", "r")
    else:
        print('Generate submission...')
        f = open("../../expedia/test.csv", "r")
    f.readline()
    totalEnhanced = 0

    while 1:
        line = f.readline().strip()
        totalEnhanced += 1
        if total % 1000000 == 0:
            print('Enhanced {} lines...'.format(totalEnhanced))

        if line == '':
            break

        arr = line.split(",")
        if validate == 1:
            user_location_city = arr[5]
            orig_destination_distance = arr[6]
            user_id = int(arr[7])
            srch_destination_id = arr[16]
            if user_id % N0 != N1:
               continue
            if is_booking == 0:
               continue
        else:
            user_location_city = arr[6]
            orig_destination_distance = arr[7]
            user_id = int(arr[8])
            srch_destination_id = arr[17]
            
                
        if orig_destination_distance != '':
            distances[(user_id, srch_destination_id)] = orig_destination_distance
            cities[(user_id, srch_destination_id)] = user_location_city

        if user_location_city != '' and user_id != '' and srch_destination_id != '':
            best_hotels_ulc_uid_sdi[(user_location_city, user_id, srch_destination_id)][hotel_cluster] += 1

    f.close()
    print(best_hotels_ulc_uid_sdi)

    ###########################
    if validate == 1:
        print('Validation...')
        f = open("../../expedia/train.csv", "r")
    else:
        print('Generate submission...')
        f = open("../../expedia/test.csv", "r")
    now = datetime.datetime.now()
    path = 'submission_' + str(now.strftime("%Y-%m-%d-%H-%M")) + '.csv'
    out = open(path, "w")
    f.readline()
    total = 0
    totalv = 0
    out.write("id,hotel_cluster\n")
    topclasters = nlargest(5, sorted(popular_hotel_cluster.items()), key=itemgetter(1))


    tries = 0
    while 1:
        line = f.readline().strip()
        total += 1
        if total % 1000000 == 0:
            print('Write {} lines...'.format(total))

        if line == '':
            break

        arr = line.split(",")
        if validate == 1:
            book_year = int(arr[0][:4])
            book_month = int(arr[0][5:7])
            user_location_city = arr[5]
            orig_destination_distance = arr[6]
            user_id = int(arr[7])
            is_package = int(arr[9])
            srch_destination_id = arr[16]
            is_booking = int(arr[18])
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
            user_location_city = arr[6]
            orig_destination_distance = arr[7]
            user_id = int(arr[8])
            is_package = int(arr[10])
            srch_destination_id = arr[17]
            hotel_country = arr[20]
            hotel_market = arr[21]
            is_booking = 1

        totalv += 1
        out.write(str(id) + ',')
        filled = []
        
        
#         distanceFound = False
#         if orig_destination_distance == '':
#             if (user_id, srch_destination_id) in distances:
#                 orig_destination_distance = distances[(user_id, srch_destination_id)]
#                 user_location_city = cities[(user_id, srch_destination_id)]
#                 distanceFound = True
#  
#  
#         s1 = (user_location_city, orig_destination_distance)
#         if s1 in best_hotels_od_ulc:
#             d = best_hotels_od_ulc[s1]
#             topitems = nlargest(5, sorted(d.items()), key=itemgetter(1))
#             for i in range(len(topitems)):
#                 if len(filled) == 5:
#                     break
#                 if topitems[i][0] in filled:
#                     continue
#                 out.write(' ' + topitems[i][0])
#                 filled.append(topitems[i][0])
#                 if validate == 1:
#                     if topitems[i][0]==hotel_cluster:
#                       hits[len(filled)] +=1
#                     if distanceFound:
#                         print('HIT with distance')
#         
#  
#         s2 = (srch_destination_id, hotel_country, hotel_market,is_package)
#         if s2 in best_hotels_search_dest:
#             d = best_hotels_search_dest[s2]
#             topitems = nlargest(5, d.items(), key=itemgetter(1))
#             for i in range(len(topitems)):
#                 if len(filled) == 5:
#                     break
#                 if topitems[i][0] in filled:
#                     continue
#                 out.write(' ' + topitems[i][0])
#                 filled.append(topitems[i][0])
#                 if validate == 1:
#                    if topitems[i][0]==hotel_cluster:
#                       hits[len(filled)] +=1
#                         
#   
#         if srch_destination_id in best_hotels_search_dest1:
#             d = best_hotels_search_dest1[srch_destination_id]
#             topitems = nlargest(5, d.items(), key=itemgetter(1))
#             for i in range(len(topitems)):
#                 if len(filled) == 5:
#                     break
#                 if topitems[i][0] in filled:
#                     continue
#                 out.write(' ' + topitems[i][0])
#                 filled.append(topitems[i][0])
#                 if validate == 1:
#                    if topitems[i][0]==hotel_cluster:
#                       hits[len(filled)] +=1
#   
#         if hotel_country in best_hotel_country:
#             d = best_hotel_country[hotel_country]
#             topitems = nlargest(5, d.items(), key=itemgetter(1))
#             for i in range(len(topitems)):
#                 if len(filled) == 5:
#                     break
#                 if topitems[i][0] in filled:
#                     continue
#                 out.write(' ' + topitems[i][0])
#                 filled.append(topitems[i][0])
#                 if validate == 1:
#                    if topitems[i][0]==hotel_cluster:
#                       hits[len(filled)] +=1
# 
#         
#         for i in range(len(topclasters)):
#             if len(filled) == 5:
#                     break
#             if topclasters[i][0] in filled:
#                 continue
#             out.write(' ' + topclasters[i][0])
#             filled.append(topclasters[i][0])
#             if validate == 1:
#                 if topclasters[i][0]==hotel_cluster:
#                     hits[len(filled)] +=1

        s3 = (user_location_city, user_id, srch_destination_id)
        if orig_destination_distance == '' and s3 in best_hotels_ulc_uid_sdi:
            d = best_hotels_ulc_uid_sdi[s3]
            topitems = nlargest(5, sorted(d.items()), key=itemgetter(1))
            for i in range(len(topitems)):
                if len(filled) == 5:
                    break
                if topitems[i][0] in filled:
                    continue
                out.write(' ' + topitems[i][0])
                filled.append(topitems[i][0])
                tries += 1
                if validate == 1:
                    if topitems[i][0]==hotel_cluster:
                        hits[len(filled)] +=1


        out.write("\n")
    out.close()
    print('Completed!')
    print('tries {}'.format(tries))
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

