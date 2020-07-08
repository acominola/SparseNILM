import pandas
import os
import matplotlib.pyplot as plt
import numpy
from libSSHMM import SuperStateHMM, frange
from libFolding import Folding
from libDataLoaders import dataset_loader
import os.path

import sys, json
from statistics import mean
from time import time
from datetime import datetime
from libDataLoaders import dataset_loader
from libFolding import Folding
from libSSHMM import SuperStateHMM
from libAccuracy import Accuracy

# Method 1: Add Gaussian noise overall regardless of appliance being used or not
# Method 2: Add Gaussian noise only when the appliance of interest is being used
# Method 3: Flatten out the consumption of the device when it's being used --> make a rectangular profile
#           Mean of the appliance profile while being used would be remain the same.
# Method 4: Change the mean of the appliance power consumption.
# Method 5: Completely erase an appliance profile (discharged over whole duration)
# Method 6: Flat profile for the whole duration
# Method 7: Flat profile daily: same within a day, but can vary between days
# Method 8: Random flat profile

def main():
    # Modify profile
    displayLength = 1440*2 # The length of profile you want to draw graphs
    usageThreshold = 1 # This threshold is only for modifying the profile (not NILM)
    saveCsv = False # If you want to save the modified profile as a file. Check it if you generate it for the first time.
    applName = 'HPE' # appliance of interest
    applNum = 5 # the number of appliances considered
    method = 1 # Method number

    inputFilePrefix = './datasets/AMPdsR1_1min_A_top'
    inputFileName = inputFilePrefix + str(applNum) + '.csv'

    # Display input profile
    df = pandas.read_csv(inputFileName)
    plt.subplot(2,4,7)
    plt.plot(df.TimeStamp[slice(0,displayLength,1)], df.WHE[slice(0,displayLength,1)])
    plt.subplot(2,4,8)
    plt.plot(df.TimeStamp[slice(0,displayLength,1)], df[applName][slice(0,displayLength,1)])

    # Modify according to the intensity of noise
    test_id = 'sVa_BigO_L05'
    modeldb = 'BigO_L05'
    precision = str(10)
    measure = 'A'
    denoised = 'noisy'
    limit = str(52000)
    algo_name = 'SparseViterbi'
    df_acc = {}

    # plot original profile
    plt.rcParams["font.family"] = "Times New Roman"
    h = plt.subplot(3,1,1)
    plt.plot((df.TimeStamp[slice(0, displayLength, 1)] - df.TimeStamp[0]) / 3600, df[applName][slice(0, displayLength, 1)],'k')
    plt.ylabel('Elec. Cons. (A)')
    df, outputFileName = modifyProfile(inputFileName,applName, usageThreshold, method,0,saveCsv)
    h = plt.subplot(3,1,2)
    plt.plot((df.TimeStamp[slice(0, displayLength, 1)]-df.TimeStamp[0])/3600, df[applName][slice(0, displayLength, 1)]-df.BAT[slice(0, displayLength, 1)],'k')
    h.axes.get_xaxis().set_ticks([])

    plt.subplot(3,1,3)
    plt.plot((df.TimeStamp[slice(0, displayLength, 1)]-df.TimeStamp[0])/3600, df.BAT[slice(0, displayLength, 1)].cumsum()*110*60/3600/1000,'k')
    plt.xlabel('Time (hr)')
    plt.ylabel('Batt. en. (kWh)')

    # run algorithm and stored NDE, MAPE, FSFSCORE in df_acc
    k = 0
    for i in range(7): # methods 1, 2
    #for i in range(0,25,5): # method 4 HPE and CDE
    # for i in [0]: # method 5 (erase an appliance)
    #for i in [0]: # method 4 FRE (is always used so impossible to modify average) & method 7
        k = k + 1
        df, outputFileName = modifyProfile(inputFileName,applName, usageThreshold, method,i,saveCsv)
        plt.subplot(2, 4, k)
        plt.plot(df.TimeStamp[slice(0, displayLength, 1)], df.WHE[slice(0, displayLength, 1)])
        #print('Method ', i, ' batSize: ', calculateBatterySizeWh(df['BAT']), ' Wh')
        print('Method ', i, ' batSize: ', calculateBatterySizeWhDay(df['BAT']), ' Wh')
        dataset = os.path.split(os.path.splitext(outputFileName)[0])[1]
        logFileName = 'logs/'+ test_id + applName + '_m'+str(method) +'_' + str(i) + '.log'
        accFileName = 'logs/acc_'+test_id + applName + '_m'+str(method)+'_'+str(i)+'.csv'
        if not os.path.isfile(accFileName):
            acc_hdr, acc_det = runAlgorithm(test_id, modeldb, dataset, precision, measure, denoised, limit, algo_name, logFileName)
            with open(accFileName,  'w') as file:
                file.write(acc_hdr)
                file.write('\n')
                file.write(acc_det)
        df_acc[k-1] = pandas.read_csv(accFileName)

    # plot metrics vs noise size
    # mean mape vs noise size
    plt.subplot(1,2,1)
    mapeArr = []
    noiseSize = range(k)
    for i in range(k):
        mapeArr.append(df_acc[i]['MAPE'][1:].mean())
    plt.plot(noiseSize, mapeArr)

    # appl mape vs noise size
    plt.subplot(1,2,2)
    mapeArr = []
    noiseSize = range(k)
    for i in range(k):
        mapeArr.append(df_acc[i].loc[df_acc[i]['Item']=='HPE','MAPE'].values[0])
    plt.plot(noiseSize, mapeArr)

    mapeArr = []
    for i in range(k):
        mapeArr.append(df_acc[i].loc[df_acc[i]['Item']=='FRE','MAPE'].values[0])
    plt.plot(noiseSize, mapeArr)

    mapeArr = []
    for i in range(k):
        mapeArr.append(df_acc[i].loc[df_acc[i]['Item']=='CDE','MAPE'].values[0])
    plt.plot(noiseSize, mapeArr)

    mapeArr = []
    for i in range(k):
        mapeArr.append(df_acc[i].loc[df_acc[i]['Item']=='UTE','MAPE'].values[0])
    plt.plot(noiseSize, mapeArr)

    #plotModifiedProfile(df, batteryProfile)
    #print(calculateBatterySizeWh(batteryProfile))
    print(1)
    # end of main


def trainModel(precision,max_obs,denoised,max_states,folds,ids):
    precision = float(precision)
    max_obs = float(max_obs)
    denoised = denoised == 'denoised'
    max_states = int(max_states)
    folds = int(folds)
    ids = ids.split(',')
    datasets_dir = './datasets/%s.csv'
    logs_dir = './logs/%s.log'
    models_dir = './models/%s.json'

    print()
    sshmms = []
    train_times = []
    folds = Folding(dataset_loader(datasets_dir % dataset, ids, precision, denoised), folds)
    for (fold, priors, testing) in folds:
        del testing
        tm_start = time()

        print()
        print('Creating load PMFs and finding load states...')
        print('\tMax partitions per load =', max_states)
        pmfs = []
        for id in ids:
            pmfs.append(EmpiricalPMF(id, max_obs * precision, list(priors[id])))
            pmfs[-1].quantize(max_states, ε)

        print()
        print('Creating compressed SSHMM...')
        incro = 1 / precision
        sshmm = SuperStateHMM(pmfs, [i for i in frange(0, max_obs + incro, incro)])

        print('\tConverting DataFrame in to obs/hidden lists...')
        obs_id = list(priors)[0]
        obs = list(priors[obs_id])
        hidden = [i for i in priors[ids].to_records(index=False)]

        sshmm.build(obs, hidden)
        sshmms.append(sshmm)

        train_times.append((time() - tm_start) / 60)


def calculateBatterySizeWh(batteryProfile):
    batteryEnergyProfileWh = batteryProfile.cumsum()*60/3600*110 # assumes 100% charging/discharging efficiency
    return batteryEnergyProfileWh.max()-batteryEnergyProfileWh.min()


def calculateBatterySizeWhDay(batteryProfile):
    batteryProfileDayList = numpy.split(batteryProfile, list(range(1440,1440*365,1440)))  # split into multiple dataframes (1 dataframe = 1 day)
    batteryProfileDayList = [x.reset_index() for x in batteryProfileDayList]
    batteryProfileDayList = [x.drop('index', axis=1) for x in batteryProfileDayList]
    batteryProfileDayList = pandas.concat(batteryProfileDayList, axis=1)
    batteryDayCumSumList = batteryProfileDayList.cumsum()
    maxBatteryCapacity =  (batteryDayCumSumList.max() - batteryDayCumSumList.min()).max()
    return maxBatteryCapacity*60*110/3600


def modifyProfile(inputFileName, applName, usageThreshold, method, noiseSize, save):
    # saves the modified profile as inputFileBase_m#.csv and returns the dataframe of the modified profile
    # and the batteryProfile (pandas dataframe) to achieve that modified profile
    # Assumption: Battery mean current should be zero over the period of time for continued usage.
    # Method 1: Add Gaussian noise overall regardless of appliance being used or not
    # Method 2: Add Gaussian noise only when the appliance of interest is being used
    # Method 3: Flatten out the consumption of the device when it's being used --> make a rectangular profile
    #           Mean of the appliance profile while being used would be remain the same.
    # Method 4: Change the mean of the appliance power consumption.
    # Method 5: Erase an appliance: average out to the whole duration
    # Method 6: Flat profile for the whole duration
    # Method 7: Flat profile every day

    #inputFileName = './datasets/Electricity_P.csv'
    inputFileBase= os.path.splitext(inputFileName)[0]

    if method == 1:
        outputFileName = inputFileBase + '_m1_' + str(noiseSize)+ '.csv'
    elif method == 2:
        outputFileName = inputFileBase + applName + '_m2_' + str(noiseSize) + '.csv'
    elif method == 3:
        outputFileName = inputFileBase + applName + '_m3.csv'
    elif method == 4:
        outputFileName = inputFileBase + applName + '_m4_' + str(noiseSize) + '.csv'
    elif method == 5:
        outputFileName = inputFileBase + '_m5.csv'
    elif method == 6:
        outputFileName = inputFileBase + '_m6.csv'
    elif method == 7:
        outputFileName = inputFileBase + '_m7.csv'
    elif method == 8:
        outputFileName = inputFileBase + '_m8_' + str(noiseSize)+ '.csv'

    if os.path.isfile(outputFileName):
        df = pandas.read_csv(outputFileName)
        return df, outputFileName

    df = pandas.read_csv(inputFileName)
    profileLength = len(df['WHE'])
    startTime = df.TimeStamp[0]
    dayLength = 60*60*24

    # The appliance that we'd like to hide

    if method == 1:
        noise = numpy.random.normal(0,noiseSize,profileLength)
        batteryProfile = noise
        df.WHE = df.WHE + noise
    elif method == 2:
        applUsageLength = len(df[df[applName]>usageThreshold])
        noise = pandas.Series(numpy.random.normal(0,noiseSize,applUsageLength))
        noise.index = df.index[df[applName] > usageThreshold]
        batteryProfile = noise.reindex(range(profileLength),fill_value=0)
        df.WHE.loc[df[applName] > usageThreshold] = df.WHE + noise
    elif method == 3: # Method 3
        applMeanWhileUsed = df.loc[df[applName] > usageThreshold, applName].mean()
        batteryProfile = df[applName].apply(lambda x: x - applMeanWhileUsed if x>usageThreshold else 0) # + is battery discharge
        df.WHE = df.WHE - batteryProfile
    elif method == 4:
        #changeApplMeanBy = noiseSize*5
        changeApplMeanBy = noiseSize
        applMeanWhileUsed = df.loc[df[applName] > usageThreshold, applName].mean()
        batteryProfile = df[applName].apply(lambda x: x - applMeanWhileUsed + changeApplMeanBy if x>usageThreshold else 0) # + is battery discharge
        batteryDischargeSum = batteryProfile.sum()
        batteryChargePavg = batteryDischargeSum / len(df[df[applName]<=usageThreshold])
        batteryProfile.loc[df[applName] <= usageThreshold] = -batteryChargePavg
        df.WHE = df.WHE - batteryProfile
    elif method == 5:
        batteryProfile = df.WHE - df.WHE
        applSum = df[applName].sum()
        batteryProfile = df[applName] - applSum/profileLength
        df.WHE = df.WHE - batteryProfile
    elif method == 6:
        totalAvgPower = df.WHE.mean()
        batteryProfile = df.WHE - totalAvgPower # + is battery discharge
        df.WHE = totalAvgPower
    elif method == 7:
        markers = numpy.zeros(365)
        markers = markers.astype(int)
        for i in range(365): # This is done because there's sometimes missing data. Day length is different
            markers[i] = numpy.argmax(df.TimeStamp >= startTime + dayLength*i)
        dfDayList = numpy.split(df, markers[1:]) # split into multiple dataframes (1 dataframe = 1 day)
        dfDayList = [ x.reset_index() for x in dfDayList]
        dfDayList = pandas.concat(dfDayList, axis = 1)
        dayAvgPList = dfDayList.WHE.mean() # I hope this is faster, but let's see
        batteryProfile = dfDayList.WHE - dayAvgPList
        dfDayList = pandas.concat(numpy.split(dfDayList,365,axis=1,),axis=0)
        dfDayList = dfDayList.reset_index().drop(['level_0', 'index', 'Unnamed: 0'], axis=1)
        dfDayList = dfDayList.dropna()
        #dfDayList = dfDayList.reset_index().drop(['level_0','index'],axis=1)
        for i in range(len(dayAvgPList)): # I couldn't avoid a loop here.
            dfDayList.loc[(dfDayList['TimeStamp']>=startTime+dayLength*i) & (dfDayList['TimeStamp']<startTime+dayLength*(i+1)),'WHE'] = dayAvgPList.values[i]
        batteryProfile = batteryProfile.melt().drop('variable',axis=1)
        batteryProfile = batteryProfile.dropna()
        df = dfDayList
    elif method == 8: # This method is for debug. Doesn't make sense pratcially
        Pval = 30
        batteryProfile = df.WHE - Pval
        df.WHE = Pval

    if save:
        df['BAT'] = batteryProfile
        df.to_csv(outputFileName, index=False)
    return df, outputFileName


def plotModifiedProfile(df):
    batteryProfile = df['BAT']
    plt.subplot(2,1,1)
    #plt.plot(df.UNIX_TS, df.WHE)
    #plt.plot(df.UNIX_TS, batteryProfile)
    plt.plot(df.TimeStamp, df.WHE)
    plt.plot(df.TimeStamp, batteryProfile)
    plt.subplot(2,1,2)
    #plt.plot(df.UNIX_TS, batteryProfile.cumsum()*60/3600/1000)
    plt.plot(df.TimeStamp, batteryProfile.cumsum()*60/3600/1000)

def runAlgorithm(test_id, modeldb, dataset, precision, measure, denoised, limit, algo_name, logFileName):
    original_stdout = sys.stdout
    with open(logFileName, 'w') as file:
        sys.stdout = file
        print()
        print(
            '----------------------------------------------------------------------------------------------------------------')
        print(
            'Test & Evaluate the Sparse Viterbi Algorithm with Saved SSHMMs  --  Copyright (C) 2013-2015, by Stephen Makonin.')
        print(
            '----------------------------------------------------------------------------------------------------------------')
        print()
        print('Start Time = ', datetime.now(), '(local time)')
        print()
        precision = float(precision)
        denoised = denoised == 'denoised'
        limit = limit.lower()
        if limit.isdigit():
            limit = int(limit)
        disagg_algo = getattr(__import__('algo_' + algo_name, fromlist=['disagg_algo']), 'disagg_algo')
        print('Using disaggregation algorithm disagg_algo() from %s.' % ('algo_' + algo_name + '.py'))

        datasets_dir = './datasets/%s.csv'
        logs_dir = './logs/%s.log'
        models_dir = './models/%s.json'

        print()
        print('Loading saved model %s from JSON storage (%s)...' % (modeldb, models_dir % modeldb))
        fp = open(models_dir % modeldb, 'r')
        jdata = json.load(fp)
        fp.close()
        folds = len(jdata)
        print('\tModel set for %d-fold cross-validation.' % folds)
        print('\tLoading JSON data into SSHMM objects...')
        sshmms = []
        for data in jdata:
            sshmm = SuperStateHMM()
            sshmm._fromdict(data)
            sshmms.append(sshmm)
        del jdata
        labels = sshmms[0].labels
        print('\tModel lables are: ', labels)

        print()
        print('Testing %s algorithm load disagg...' % algo_name)
        acc = Accuracy(len(labels), folds)
        test_times = []
        indv_tm_sum = 0.0
        indv_count = 0
        y_noise = 0.0
        y_total = 0.0
        calc_done = [0, 0]
        calc_total = [0, 0]
        unexpected_event = 0
        adapted_event = 0
        adapted_errors = 0
        multi_switches_count = 0

        print()
        folds = Folding(dataset_loader(datasets_dir % dataset, labels, precision, denoised), folds)
        for (fold, priors, testing) in folds:
            del priors
            tm_start = time()

            sshmm = sshmms[fold]
            obs_id = list(testing)[0]
            obs = list(testing[obs_id])
            hidden = [i for i in testing[labels].to_records(index=False)]

            print()
            print('Begin evaluation testing on observations, compare against ground truth...')
            print()
            pbar = ''
            pbar_incro = len(testing) // 20
            for i in range(1, len(obs)):
                multi_switches_count += (sum([i != j for (i, j) in list(zip(hidden[i - 1], hidden[i]))]) > 1)

                y0 = obs[i - 1]
                y1 = obs[i]

                start = time()
                (p, k, Pt, cdone, ctotal) = disagg_algo(sshmm, [y0, y1])
                elapsed = (time() - start)

                s_est = sshmm.detangle_k(k)
                y_est = sshmm.y_estimate(s_est, breakdown=True)

                y_true = hidden[i]
                s_true = sshmm.obs_to_bins(y_true)

                acc.classification_result(fold, s_est, s_true, sshmm.Km)
                acc.measurement_result(fold, y_est, y_true)

                calc_done[0] += cdone[0]
                calc_done[1] += cdone[1]
                calc_total[0] += ctotal[0]
                calc_total[1] += ctotal[1]

                if p == 0.0:
                    unexpected_event += 1

                indv_tm_sum += elapsed
                indv_count += 1

                y_noise += round(y1 - sum(y_true), 1)
                y_total += y1

                if not i % pbar_incro or i == 1:
                    pbar += '='  # if i > 1 else ''
                    disagg_rate = float(indv_tm_sum) / float(indv_count)
                    print('\r\tCompleted %2d/%2d: [%-20s], Disagg rate: %12.6f sec/sample ' % (
                    fold + 1, folds.folds, pbar[:20], disagg_rate), end='', flush=True)
                    sys.stdout.flush()

                if limit != 'all' and i >= limit:
                    print('\n\n *** LIMIT SET: Only testing %d obs. Testing ends now!' % limit)
                    break;

            test_times.append((time() - tm_start) / 60)

            if limit != 'all' and i >= limit:
                break;

        print()
        print()
        print('Evaluation and accuracy testing complete:')
        disagg_rate = indv_tm_sum / indv_count
        print('\tTest Time was', round(sum(test_times), 2), ' min (avg ', round(sum(test_times) / len(test_times), 2),
              ' min/fold).')
        if calc_total[0] > 0 and calc_total[1] > 0:
            print('\tOptimization (Time) - Viterbi Part 1:', round((calc_total[0] - calc_done[0]) / calc_total[0] * 100, 2),
                  '% saved, ', format(calc_done[0], ',d'), 'calculations (average', round(calc_done[0] / indv_count, 1),
                  'calculations each time)')
            print('\tOptimization (Time) - Viterbi Part 2:', round((calc_total[1] - calc_done[1]) / calc_total[1] * 100, 2),
                  '% saved, ', format(calc_done[1], ',d'), 'calculations (average', round(calc_done[1] / indv_count, 1),
                  'calculations each time)')
        else:
            print('\tOptimization (Time): NOT BEING TRACKED!')
        print('\tUnexpected events =', unexpected_event, ', Multiple switch events =', multi_switches_count,
              ', Adapted events =', adapted_event, '(errors =', adapted_errors, ')')

        acc.print(test_id, labels, measure)

        report = []
        report.append(['Test ID', test_id])
        report.append(['Run Date', datetime.now()])
        report.append(['Dataset', dataset])
        report.append(['Precision', precision])
        report.append(['Denoised?', denoised])
        report.append(['Model Noise?', ('UNE' in labels)])
        report.append(['Limit', limit])
        report.append(['Algorithm', algo_name])
        report.append(['Folds', folds.folds])
        report.append(['Measure', measure])
        report.append(['Tests', indv_count])
        report.append(['Total Calc Vp1', calc_total[0]])
        report.append(['Actual Calc Vp1', calc_done[0]])
        report.append(['Total Calc Vp2', calc_total[1]])
        report.append(['Actual Calc Vp2', calc_done[1]])
        report.append(['Test Time', round(sum(test_times), 2)])
        report.append(['Avg Time/Fold', round(sum(test_times) / len(test_times), 2)])
        report.append(['Disagg Time', '{0:.10f}'.format(disagg_rate)])
        report.append(['Unexpected', unexpected_event])
        report.append(['Adapted', adapted_event])
        report.append(['Adapted Errors', adapted_errors])
        report.append(['Mult-Switches', multi_switches_count])
        report.append(['Noise', round(y_noise / y_total, 4)])

        print()
        print('-------------------------------- CSV REPORTING --------------------------------')
        print()
        print(','.join([c[0] for c in report]))
        print(','.join([str(c[1]) for c in report]))
        print()
        (acc_hdr, acc_det) = acc.csv(test_id, labels, measure)
        print(acc_hdr)
        print(acc_det)
        print()
        print('-------------------------------- ------------- --------------------------------')

        print()
        print('End Time = ', datetime.now(), '(local time)')
        print()
        print('DONE!!!')
        print()
        sys.stdout = original_stdout
        return acc_hdr, acc_det

if __name__ == '__main__':
    main()



