import pandas
import os
import matplotlib.pyplot as plt
import numpy


def main():
    df, batteryProfile = modifyProfile('./datasets/Electricity_p.csv', 'CDE', 0.1, 7, False)
    plotModifiedProfile(df, batteryProfile)
    print(calculateBatterySizeWh(batteryProfile))
    print(1)



def calculateBatterySizeWh(batteryProfile):
    batteryEnergyProfileWh = batteryProfile.cumsum()*60/3600 # assumes 100% charging/discharging efficiency
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
    startTime = df.UNIX_TS[0]
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
        df.WHE.loc[df[applName] > usageThreshold] = noise
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
        dfDayList = numpy.array_split(df, 60*24) # split into multiple dataframes (1 dataframe = 1 day)
        dfDayList = [ x.reset_index() for x in dfDayList]
        dfDayList = pandas.concat(dfDayList, axis = 1)
        dayAvgPList = dfDayList.WHE.mean()
        batteryProfile = dfDayList.WHE - dayAvgPList
        dfDayList = pandas.concat(numpy.split(dfDayList,60*24,axis=1,),axis=0)
        dfDayList = dfDayList.reset_index().drop(['level_0','index'],axis=1)
        for i in range(len(dayAvgPList)):
            dfDayList.loc[(dfDayList['UNIX_TS']>=startTime+dayLength*i) & (dfDayList['UNIX_TS']<startTime+dayLength*(i+1)),'WHE'] = dayAvgPList.values[i]
        batteryProfile = batteryProfile.melt().drop('variable',axis=1)

    if save:
        df.to_csv(outputFileName, index=False)
    return df, batteryProfile


def plotModifiedProfile(df, batteryProfile):
    plt.subplot(2,1,1)
    plt.plot(df.UNIX_TS, df.WHE)
    plt.plot(df.UNIX_TS, batteryProfile)
    plt.subplot(2,1,2)
    plt.plot(df.UNIX_TS, batteryProfile.cumsum()*60/3600/1000)


if __name__ == '__main__':
    main()


