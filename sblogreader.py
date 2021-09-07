import re
import datetime
def processData(filelist):
    mt1 = {}
    for file in filelist:
        mt2 = {}
        mt3 = {}
        mt4 = {}
        fi = open(file,"r")
        data = fi.read().split("Statistics:\n")
        data_properties = data[0]
        data_statistics = data[1]
        #print(data_statistics)
        mt2["DATE"] = data_properties.splitlines()[0].split('\t')[1]       
        for line3 in data_properties.strip().splitlines()[5:]:
            if 'Statistics' not in line3:
                elems = line3.strip().split(':')
                mt3[elems[0]] = elems[1]
        #solve for statistics
        count = 0
        for line in data_statistics.splitlines():
            if line != "" or "===" not in line:               
                if "total" in line or "X" in line or "tracked" in line:
                    for key in line.split("\t"):
                        mt4[key] = []
                else:
                    keys = [*mt4]
                    elems = line.split("\t")
                    for i in range(len(keys)):
                        if keys[i] == "integrated" or keys[i] == "tracked":
                            mt4[keys[i]].append(bool(int(elems[i])))
                        else:
                            mt4[keys[i]].append(elems[i])
            else:
                continue
            mt2["Properties"] = mt3
            mt2["Statistics"] = mt4
            mt1[file] = mt2           
    return mt1


#processData(['sblog/0.log'])

import math

def processDataGT(filelist,gt):
    data = processData(filelist)
    file_gt = open(gt,"r")
    gt_1 = file_gt.readlines()
    list_std =gt_1[0].split(" ")
    X,Y,Z = [],[],[]
    for line in gt_1:
        line2 = line.strip().split(" ")
        X.append(int(line2[1])-int(list_std[1]))
        Y.append(int(line2[2])-int(list_std[2]))
        Z.append(float(line2[3])-float(list_std[3]))
        break
    for line in gt_1[1:]:
        line3 = line.strip("\t").split(" ")
        X.append(float(line3[1])-float(list_std[1]))
        Y.append(float(line3[2])-float(list_std[2]))
        Z.append(float(line3[3])-float(list_std[3]))
    for file in filelist:
        euclidean = []
        Stat_X = data[file]["Statistics"]["X"]
        Stat_Y = data[file]["Statistics"]["Y"]
        Stat_Z = data[file]["Statistics"]["Z"]
        mod_X = [float(x)-float(Stat_X[0]) for x in Stat_X]
        mod_Y = [float(y)-float(Stat_Y[0])for y in Stat_Y]
        mod_Z = [float(z)-float(Stat_Z[0])for z in Stat_Z]       
        for i in range(len(mod_X)):
            euclidean.append(math.sqrt((X[i]-mod_X[i])**2 + (Y[i]-mod_Y[i])**2 + (Z[i]-mod_Z[i])**2 ))
        data[file]["Statistics"]["ATE"] = euclidean
    return data



#processDataGT(['sblog/0.log','sblog/1.log'],"livingRoom2.gt.freiburg")
from operator import itemgetter
import numpy as np
import statistics
def ExtractData(raw_data):
    stat_list = [(x,len(raw_data[x]["Statistics"].keys())) for x in raw_data.keys()]
    max_stat_file = max(stat_list,key=itemgetter(1))[0]
    main_dict = {"filename":[],
    "compute-size-ratio":[],
    "icp-threshold":[],
    "mu":[],
    "integration-rate":[],
    "tracking-rate":[],
    "pyramid-levels":[],
    "volume-resolution":[]}    
    for key in list(raw_data[max_stat_file]["Statistics"].keys()):
        main_dict[key+"_min"] = []
        main_dict[key+"_max"] = []
        main_dict[key+"_mean"] = []
        main_dict[key+"_sum"] = []
        main_dict[key+"_median"] = []
    for file in raw_data.keys():
        #for properties
        main_dict["filename"].append(file)
        main_dict["compute-size-ratio"].append(raw_data[file]["Properties"]["compute-size-ratio"])
        main_dict["icp-threshold"].append(raw_data[file]["Properties"]["icp-threshold"])
        main_dict["mu"].append(raw_data[file]["Properties"]["mu"])
        main_dict["integration-rate"].append(raw_data[file]["Properties"]["integration-rate"])
        main_dict["tracking-rate"].append(raw_data[file]["Properties"]["tracking-rate"])
        main_dict["pyramid-levels"].append(raw_data[file]["Properties"]["pyramid-levels"])
        main_dict["volume-resolution"].append(raw_data[file]["Properties"]["volume-resolution"])
        for key in list(raw_data[file]["Statistics"].keys()):
            #for statistics
            main_dict[key+"_min"].append(min([float(x) for x in raw_data[file]["Statistics"][key]]))
            main_dict[key+"_max"].append(max([float(x) for x in raw_data[file]["Statistics"][key]]))
            main_dict[key+"_mean"].append(statistics.mean([float(x) for x in raw_data[file]["Statistics"][key]]))
            main_dict[key+"_sum"].append(sum([float(x) for x in raw_data[file]["Statistics"][key]]))
            main_dict[key+"_median"].append(statistics.median([float(x) for x in raw_data[file]["Statistics"][key]]))
    return main_dict

#ExtractData(processDataGT(['sblog/0.log','sblog/1.log',],"livingRoom2.gt.freiburg"))




