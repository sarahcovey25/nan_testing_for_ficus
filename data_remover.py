import random
import datetime
import pandas as pd

def removePoints(df, colToRemove, pointsToRemove):
    """ 
    copies the dataframe and removes points in [pointsToRemove, colToRemove]

    @param: df - the dataframe to copy and remove points from
    @param: colToRemove - the name of the column from which to remove data (ex: 'Ozone')
    @return: a new dataframe with the points in pointsToRemove replaced with NaN
    """

    newDF = df.copy()

    for dt in pointsToRemove:
        newDF.loc[dt, colToRemove] = float("NaN")

    return newDF

def makeRemovedAtTime(df, colToRemove, hourToRemove, enddate=None, percentPoints=100, numPoints = None):
    """
    copies the dataframe and removes points at a specific hour in a specified column

    @param df - the dataframe to copy and remove points from
    @param: colToRemove - the name of the column from which to remove data (ex: 'Ozone')
    @param: hourToRemove - the hour of day to remove points at
    @param enddate - the day after the last date that can be removed (default: last element in dataframe + 1 hour)
    @param percentPoints - the percentage of removable points to be removed (default: 100)
    @param numPoints - the absolute number of points to remove. if specified, overrides percentPoints. (default: None)
    @return: a new dataframe with data at a specified time removed from randomly selected days before enddate
    """
    if enddate is None:
        enddate = df.iloc[-1].name + pd.Timedelta(hours=1)
    allPointsAtTime = list(filter(lambda dt: dt.hour == hourToRemove and dt<enddate , df.index))
    if numPoints is None:
        numPoints = round(len(allPointsAtTime)*percentPoints/100.0)
    pointsToRemove = random.sample(allPointsAtTime, numPoints)

    newDF = removePoints(df, colToRemove, pointsToRemove)
    return (newDF, pointsToRemove)


## TODO: figure out whats going on this this
def getAdjacentPoints(df, colToRemove, startPoint, numPoints, hourChange=1, dayChange=0):
    timeChange = datetime.timedelta(hours=hourChange, days=dayChange)
    pointsToRemove = [startPoint + timeChange*i for i in range(0, numPoints)]

    # newDF = removePoints(df, colToRemove, pointsToRemove)
    return pointsToRemove

# assumes time per cycle is greater than cycleLength
# if hoursPercycle and daysPerCycle remain unchanged, will set cycle time to one day
# TODO: docstring this
def removePointsInPattern(df, colToRemove, startPoint, cycleLength, numCycles=1, hoursPerCycle=0, daysPerCycle=0):

    if hoursPerCycle == 0 and daysPerCycle == 0:
        daysPerCycle = 1

    pointsToRemove = []
    for i in range(cycleLength):
        pointsToRemove += getAdjacentPoints(df, colToRemove, startPoint + datetime.timedelta(hours=1)*i, 
                            numCycles, hourChange=hoursPerCycle, dayChange=daysPerCycle)

    newDF = removePoints(df, colToRemove, pointsToRemove)
    return newDF


# assumes all missing timestamps in comparisonDF are also in df
# TODO: docstring this
def removeByDataframe(df, colToRemove, comparisonDF, timeshift=None):
    pointsToRemove = comparisonDF.loc[comparisonDF[colToRemove].isna()].index
    if timeshift is not None:
        pointsToRemove = list(map(lambda timestamp: timestamp+timeshift, pointsToRemove))
    return removePoints(df, colToRemove, pointsToRemove)