import pandas
import os
import matplotlib.pyplot as plt
import numpy

inputFileName = './datasets/AMPdsR1_1min_A_top5.csv'
inputFileBase= os.path.splitext(inputFileName)[0]
df = pandas.read_csv(inputFileName)
profileLength = len(df['TimeStamp'])

# The appliance that we'd like to hide
#applName = {'CDE','HPE', 'FRE'}
applName = 'CDE'
usageThreshold = 1.0

plt.subplot(3,1,1)
plt.plot(df['TimeStamp'], df['WHE'])
plt.subplot(3,1,2)
plt.plot(df['TimeStamp'], df[applName])

# Assumption: Battery mean current should be zero over the period of time for continued usage.
# Method 1: Add Gaussian noise overall regardless of appliance being used or not
# Method 2: Add Gaussian noise only when the appliance of interest is being used
# Method 3: Flatten out the consumption of the device when it's being used --> make a rectangular profile
#           Mean of the appliance profile while being used would be remain the same.
# Method 4: Change the mean of the appliance power consumption.
# Method 5: Prolonging the usage time?

method = 4

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

plt.plot(df.TimeStamp.loc[batteryProfile.index], batteryProfile)
plt.subplot(3,1,3)
plt.plot(df.TimeStamp, df.WHE)
df.to_csv(outputFileName, index=False)
