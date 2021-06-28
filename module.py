import numpy as np
import os
import matplotlib.pyplot as plt
###############################################
#GLOBAL VARIABLES
policyName = []
noHosts = []
noVms = []
totalSimulationTime = []
energyConsumtion = []
noVmMigrations = []
sla = []
slaPerfDegradationMigration = []
slaTimePerActiveHost = []
overallSlaViolation = []
averageSlaViolation = []
noHostShutdown = []
meanTimeBeforeHostShutdown = []
stdDevBeforeHostShutdown = []
meanTimeBeforeVmMigration = []
stdDevBeforeVmMigration = []
##############################################
def stringAfterChar(iString, iChar):
    indexChar = iString.find(iChar)
    return iString[indexChar+2:]
def stringAfterCharTwo(iString, iChar):
    indexChar = iString.find(iChar)
    return iString[indexChar+1:]

def stringBeforeChar(iString, iChar):
    indexChar = iString.find(iChar)
    return iString[:indexChar]

def extractDataFromFile(fileNameWithExtension):
    f = open(fileNameWithExtension, "r")
    listData = []
    inputChar = f.readlines()
    spl_char = ":"
    count = 0
    for line in inputChar:
        lineChar = line.strip()
        # print(lineChar)
        if count == 0:
            listData.append(stringAfterCharTwo(lineChar, "_"))
        elif count > 0 and count < 3 or count == 5 or count == 11:
            listData.append(stringAfterChar(lineChar, spl_char))
        elif count > 5 and count < 11:
            listData.append(stringBeforeChar(stringAfterChar(lineChar, spl_char), "%"))
        elif count == 4:
            listData.append(stringBeforeChar(stringAfterChar(lineChar, spl_char), "kWh"))
        elif count == 3 or count > 11:
            listData.append(stringBeforeChar(stringAfterChar(lineChar, spl_char), "sec")) 
        count += 1
    return listData

def makingPlotPoint(fileList):
    pWorkDir = os.getcwd()
    pathFromExperimentalResult = pWorkDir+"/experimental_results/"
    for i in range(len(fileList)):
        try:
            extractedData = extractDataFromFile(pathFromExperimentalResult + fileList[i])
            policyName.append(extractedData[0])
            noHosts.append(extractedData[1])
            noVms.append(extractedData[2])
            totalSimulationTime.append(extractedData[3])
            energyConsumtion.append(extractedData[4])
            noVmMigrations.append(extractedData[5])
            sla.append(extractedData[6])
            slaPerfDegradationMigration.append(extractedData[7])
            slaTimePerActiveHost.append(extractedData[8])
            overallSlaViolation.append(extractedData[9])
            averageSlaViolation.append(extractedData[10])
            noHostShutdown.append(extractedData[11])
            meanTimeBeforeHostShutdown.append(extractedData[12])
            stdDevBeforeHostShutdown.append(extractedData[13])
            meanTimeBeforeVmMigration.append(extractedData[14])
            stdDevBeforeVmMigration.append(extractedData[15])
        except:
            print("File Not Found in Experimental_result Folder!!")
def makingSavingPlot(xPoint, yPoint, yPointLebel, lebelPlot, filePath = ""):
    xPoint = np.array(xPoint)
    yPoint = list(map(float, yPoint))
    yPoint = np.array(yPoint)
    fig = plt.figure(figsize = (10, 5))
    
    plt.plot(xPoint, yPoint, color='green', linestyle='dashed', linewidth = 3,
             marker='o', markerfacecolor='blue', markersize=12, )

    plt.ylabel(yPointLebel)
    plt.title(lebelPlot)
    # plt.show()
    plt.savefig("{}{}.png".format(filePath, yPointLebel))

def finalPlotSaving(fileLists, folderName):
    yPointLebel = ["Number of Hosts", "Number of VMs", "Total Simulation Time (sec)",
                    "Total Energy Consumption (kWh)", "Number of VM Migrations",
                    "SLA (%)", "SLA Degradation Migration (%)",
                    "SLA Time Per Active Host (%)", "Overall SLA violation (%)",
                    "Average SLA violation (%)", "Number of host shutdowns",
                    "Mean time before a host shutdown (sec)", "StDev time before a host shutdown (sec)",
                    "Mean time before a VM migration (sec)", "StDev time before a VM migration (sec)"]
    makingPlotPoint(fileLists)
    yPoints = [noHosts, noVms, totalSimulationTime, energyConsumtion,
                noVmMigrations, sla, slaPerfDegradationMigration, 
                slaTimePerActiveHost, overallSlaViolation, averageSlaViolation,
                noHostShutdown, meanTimeBeforeHostShutdown, stdDevBeforeHostShutdown,
                meanTimeBeforeVmMigration, stdDevBeforeVmMigration]


    currentDirectory = os.getcwd()
    targetPath = currentDirectory+"/"+folderName+"/"
    
    try:
        os.mkdir(targetPath)
    except:
        print("Folder Already Exist!")
        print("Saving Plots on Existing Folder..........")
    for i in range(len(yPoints)):
        makingSavingPlot(policyName, yPoints[i], yPointLebel[i], "Comparison Graph", targetPath)


def main():
    f = open("result_textfile_list.txt", "r")
    inputFileI = f.read().split('\n')
    fileList = inputFileI[1: -1]
    folderName = inputFileI[0] # write name without any / or \
    # print(fileList, folderName)
    finalPlotSaving(fileList, folderName)
    print("PLOT HAS BEEN SAVED SUCCESSFULLY")


if __name__ == "__main__":
    main()