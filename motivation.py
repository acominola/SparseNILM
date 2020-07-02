import pandas
import os
import matplotlib.pyplot as plt
import numpy
from libSSHMM import SuperStateHMM, frange
from libFolding import Folding
from libDataLoaders import dataset_loader


# Method 1: Add Gaussian noise overall regardless of appliance being used or not
# Method 2: Add Gaussian noise only when the appliance of interest is being used
# Method 3: Flatten out the consumption of the device when it's being used --> make a rectangular profile
#           Mean of the appliance profile while being used would be remain the same.
# Method 4: Change the mean of the appliance power consumption.
# Method 5: Prolonging the usage time?
# Method 6: Flat profile for the whole duration
# Method 8: Random flat profile

def main():
    displayLength = 1440*2
    usageThreshold = 1
    saveCsv = False
    applName = 'CDE'
    df = pandas.read_csv('./datasets/AMPdsR1_1min_A_top5.csv')
    plt.subplot(2,4,1)
    plt.plot(df.TimeStamp[slice(0,displayLength,1)], df.WHE[slice(0,displayLength,1)])
    plt.subplot(2,4,6)
    plt.plot(df.TimeStamp[slice(0,displayLength,1)], df[applName][slice(0,displayLength,1)])
    df, batteryProfile = modifyProfile('./datasets/AMPdsR1_1min_A_top5.csv', applName, usageThreshold, 8, True)
    for i in [1,2,3,4,6,7]:
        df, batteryProfile = modifyProfile('./datasets/AMPdsR1_1min_A_top5.csv', applName, usageThreshold, i, saveCsv)
        plt.subplot(2,4,i+1)
        plt.plot(df.TimeStamp[slice(0, displayLength, 1)], df.WHE[slice(0, displayLength, 1)])
        print('Method ', i, ': ',calculateBatterySizeWh(batteryProfile))
    #df, batteryProfile = modifyProfile('./datasets/Electricity_p.csv', applName, usageThreshold, 7, saveCsv)
    #df, batteryProfile = modifyProfile('./datasets/AMPdsR1_1min_A_top5.csv', applName, usageThreshold, 7, saveCsv)
    #plt.subplot(2,4,7)
    #plt.plot(df.TimeStamp,df.WHE)
    #df, batteryProfile = modifyProfile('./datasets/AMPdsR1_1min_A_top5.csv', applName, usageThreshold, 7, saveCsv)

    #plotModifiedProfile(df, batteryProfile)
    #print(calculateBatterySizeWh(batteryProfile))
    print(1)


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


def modifyProfile(inputFileName, applName, usageThreshold, method, save):
    # saves the modified profile as inputFileBase_m#.csv and returns the dataframe of the modified profile
    # and the batteryProfile (pandas dataframe) to achieve that modified profile
    # Assumption: Battery mean current should be zero over the period of time for continued usage.
    # Method 1: Add Gaussian noise overall regardless of appliance being used or not
    # Method 2: Add Gaussian noise only when the appliance of interest is being used
    # Method 3: Flatten out the consumption of the device when it's being used --> make a rectangular profile
    #           Mean of the appliance profile while being used would be remain the same.
    # Method 4: Change the mean of the appliance power consumption.
    # Method 5: Prolonging the usage time?
    # Method 6: Flat profile for the whole duration
    # Method 7: Flat profile every day

    #inputFileName = './datasets/Electricity_P.csv'
    inputFileBase= os.path.splitext(inputFileName)[0]
    df = pandas.read_csv(inputFileName)
    profileLength = len(df['WHE'])
    #startTime = df.UNIX_TS[0]
    startTime = df.TimeStamp[0]
    dayLength = 60*60*24

    # The appliance that we'd like to hide
    #applName = {'CDE','HPE', 'FRE'}
    #applName = 'CDE'
    #usageThreshold = 1.0

    #plt.subplot(2,1,1)
    #plt.plot(df['UNIX_TS'], df['WHE'])
    #plt.plot(df['UNIX_TS'], df[applName])

    if method == 1:
        outputFileName = inputFileBase + '_m1.csv'
        noise = numpy.random.normal(0,5,profileLength)
        batteryProfile = noise
        df.WHE = df.WHE + noise
    elif method == 2:
        outputFileName = inputFileBase + '_m2.csv'
        applUsageLength = len(df[df[applName]>usageThreshold])
        noise = pandas.Series(numpy.random.normal(0,5,applUsageLength))
        noise.index = df.index[df[applName] > usageThreshold]
        batteryProfile = noise.reindex(range(profileLength),fill_value=0)
        df.WHE.loc[df[applName] > usageThreshold] = df.WHE + noise
        #df.loc[]
    elif method == 3: # Method 3
        outputFileName = inputFileBase+'_m3.csv'
        applMeanWhileUsed = df.loc[df[applName] > usageThreshold, applName].mean()
        batteryProfile = df[applName].apply(lambda x: x - applMeanWhileUsed if x>usageThreshold else 0) # + is battery discharge
        df.WHE = df.WHE - batteryProfile
    elif method == 4:
        outputFileName = inputFileBase + '_m4.csv'
        changeApplMeanBy = 5
        applMeanWhileUsed = df.loc[df[applName] > usageThreshold, applName].mean()
        batteryProfile = df[applName].apply(lambda x: x - applMeanWhileUsed + changeApplMeanBy if x>usageThreshold else 0) # + is battery discharge
        batteryDischargeSum = batteryProfile.sum()
        batteryChargePavg = batteryDischargeSum / len(df[df[applName]<=usageThreshold])
        batteryProfile.loc[df[applName] <= usageThreshold] = -batteryChargePavg
        batterySum = batteryProfile.sum()
        df.WHE = df.WHE - batteryProfile
    elif method == 5:
        outputFileName = inputFileBase + '_m5.csv'
    elif method == 6:
        outputFileName = inputFileBase + '_m6.csv'
        totalAvgPower = df.WHE.mean()
        batteryProfile = df.WHE - totalAvgPower # + is battery discharge
        df.WHE = totalAvgPower
    elif method == 7:
        outputFileName = inputFileBase + '_m7.csv'
        markers = numpy.zeros(365)
        markers = markers.astype(int)
        for i in range(365):
            markers[i] = numpy.argmax(df.TimeStamp >= startTime + dayLength*i)
        dfDayList = numpy.split(df, markers[1:]) # split into multiple dataframes (1 dataframe = 1 day)
        dfDayList = [ x.reset_index() for x in dfDayList]
        dfDayList = pandas.concat(dfDayList, axis = 1)
        dayAvgPList = dfDayList.WHE.mean()
        batteryProfile = dfDayList.WHE - dayAvgPList
        dfDayList = pandas.concat(numpy.split(dfDayList,365,axis=1,),axis=0)
        dfDayList = dfDayList.reset_index().drop(['level_0', 'index', 'Unnamed: 0'], axis=1)
        dfDayList = dfDayList.dropna()
        #dfDayList = dfDayList.reset_index().drop(['level_0','index'],axis=1)
        for i in range(len(dayAvgPList)):
            dfDayList.loc[(dfDayList['TimeStamp']>=startTime+dayLength*i) & (dfDayList['TimeStamp']<startTime+dayLength*(i+1)),'WHE'] = dayAvgPList.values[i]
        batteryProfile = batteryProfile.melt().drop('variable',axis=1)
        batteryProfile = batteryProfile.dropna()
        df = dfDayList
    elif method == 8:
        outputFileName = inputFileBase + '_m8.csv'
        Pval = 25
        batteryProfile = df.WHE - Pval
        df.WHE = Pval

    if save:
        df.to_csv(outputFileName, index=False)
    return df, batteryProfile


def plotModifiedProfile(df, batteryProfile):
    plt.subplot(2,1,1)
    #plt.plot(df.UNIX_TS, df.WHE)
    #plt.plot(df.UNIX_TS, batteryProfile)
    plt.plot(df.TimeStamp, df.WHE)
    plt.plot(df.TimeStamp, batteryProfile)
    plt.subplot(2,1,2)
    #plt.plot(df.UNIX_TS, batteryProfile.cumsum()*60/3600/1000)
    plt.plot(df.TimeStamp, batteryProfile.cumsum()*60/3600/1000)


if __name__ == '__main__':
    main()



