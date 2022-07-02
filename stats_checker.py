import math
import datetime
import pandas as pd
import numpy as np



# calculates RMSE between predicted and observed values
def rmseCheck(predicted, observed):
    """ Calculates and returns the root mean square error of the predicted vs observed """
    errorsSquared = list(map(lambda x, y: (x-y)**2, predicted, observed))
    return np.sqrt(np.mean(errorsSquared))

def nmbCheck(predicted, observed):
    """ Calculates and returns the normalized mean bias of the predicted vs observed """
    sumErrors = list(map(lambda x, y: x-y, predicted, observed))
    return 100*sumErrors/sum(observed)

def nmeCheck(predicted, observed):
    """ Calculates and returns the normalized mean error of the predicted vs observed """
    sumAbsErrors = list(map(lambda x, y: math.abs(x-y), predicted, observed))
    return 100*sumAbsErrors/sum(observed)

def getStatistic(predicted, observed, statistic):
    """ Calculates and returns the statistic of the predicted vs observed, specified by statistic """
    if statistic == "RMSE":
        return rmseCheck(predicted, observed)
    elif statistic == "NMB":
        return rmseCheck(predicted, observed)
    elif statistic == "NME":
        return rmseCheck(predicted, observed)   

# calculating RMSE between the predicted and observed values at values above 95% on the observed
def check95(predicted, observed, statistic="RMSE"):
    """ Calculates the specified statistic for all points above the 95th percentile """
    p95 = np.percentile(observed, 95)
    indices = [i for i in range(len(observed)) if observed[i]>=p95  ]

    filteredPredicted = [predicted[i] for i in indices]
    filteredObserved = [observed[i] for i in indices]

    return getStatistic(filteredPredicted, filteredObserved, statistic)


# calculates RMSE in between startTime and endTime (inclusive)
def checkByTime(predicted, observed, datetimes, hour, statistic="RMSE"):
    """ Calculates the specified statistic for all points at the specified hour """
    indices = [i for i in range(len(observed)) if datetimes[i].hour == hour]

    filteredPredicted = [predicted[i] for i in indices]
    filteredObserved = [observed[i] for i in indices]

    return getStatistic(filteredPredicted, filteredObserved, statistic)

def check10Ato4P(predicted, observed, datetimes, statistic="RMSE"):
    """ Calculates the specified statistic for all points between 10am and 4pm """
    indices = [i for i in range(len(observed)) if datetimes[i].hour >= 10 and datetimes[i].hour <= 16]
    filteredPredicted = [predicted[i] for i in indices]
    filteredObserved = [observed[i] for i in indices]
    return getStatistic(filteredPredicted, filteredObserved, statistic)

def check12Ato4A(predicted, observed, datetimes, statistic="RMSE"):
    """ Calculates the specified statistic for all points between 12am and 4am """
    indices = [i for i in range(len(observed)) if datetimes[i].hour <= 4]
    filteredPredicted = [predicted[i] for i in indices]
    filteredObserved = [observed[i] for i in indices]
    return getStatistic(filteredPredicted, filteredObserved, statistic)


# TODO: add other stats
def getStatDF(predictedList, observed, names=None, timestampIndex=None, timesToTest=None, statsList=["RMSE", "NMB", "NME"]):
    """ 
    Generates a dataframe with different statistical values 

    @param: predictList - the list of predictions from different models
    @param: ovserved - 
    @return: a dataframe with the calculated statistics for each model
    """


    rmseList = []
    rmse95List = []

    for pred in predictedList:
        rmseList.append(rmseCheck(pred, observed))
        rmse95List.append(rmse95(pred, observed))

    statDF = pd.DataFrame({'RMSE': rmseList,
                  'RMSE 95%': rmse95List})
  
    if timesToTest is not None:
        for timeToTest in timesToTest:
            rmseByHourList = []

            for pred in predictedList:
                rmseByHourList.append(rmseByTime(pred, observed, timestampIndex, timeToTest))

            statDF["RMSE Hour="+str(timeToTest)] = rmseByHourList

    if names is not None:
        statDF['RF Test'] = names
        statDF.set_index('RF Test', inplace=True)
  
    return statDF