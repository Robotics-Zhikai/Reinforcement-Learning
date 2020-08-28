import numpy as np
import time
import matplotlib.pyplot as plt

def GetCurrentXTestReward(average,std,numOfGamble):
    "输入为numOfGamble个真实值average及对应的std，服从正态分布"
    OutPut = []
    # np.random.seed(int(time.time()))
    for i in range(numOfGamble):
        Value = np.random.normal(average[i],std[i],1);
        OutPut.append(Value[0])
    return OutPut

def RandGenerateREALValue(numOfGamble):
    "生成numOfGamble个真实的值,每次调用都一样"
    np.random.seed(0)
    output = np.random.normal(0,1,numOfGamble)
    return output

def ChooseMaxGamble(RandomResult):
    index = RandomResult.index(max(RandomResult))
    return index

def UpdateIndexReward(CurrentKnowReward,ContXGamblesSelectNum,real,std,index):
    "更新对应的index随机值"

    ContXGamblesSelectNum[index] = ContXGamblesSelectNum[index]+1
    # np.random.seed(int(time.time()))
    reward = np.random.normal(real[index],std[index],1)
    # print(reward)
    CurrentKnowReward[index] = CurrentKnowReward[index]+1/ContXGamblesSelectNum[index]*(reward-CurrentKnowReward[index])
    # print(CurrentKnowReward)
    return reward

def Experiment_realNotChange(RealIndex,real,Eststd,numOfGamble,Iteration,RandSeedOffset,tryPar):
    CurrentKnowReward = GetCurrentXTestReward(real,Eststd,numOfGamble)
    #
    # print('InitCurrentKnowReward',CurrentKnowReward)

    ContXGamblesSelectNum = [];
    for i in range(numOfGamble):
        ContXGamblesSelectNum.append(0)

    output = []
    outputRewardRecord = []
    outputRightSelect = []
    # tryPar = 0
    RewardSum = 0
    # plt.figure()
    for i in range(Iteration):
        # print(i)
        # np.random.seed(int(time.time()))
        thisrandom = np.random.random()
        # print(thisrandom)
        if thisrandom<tryPar:
            # print(thisrandom)
            # np.random.seed(int(time.time()))
            index = np.random.randint(0,numOfGamble)
            # print(index)
            if index==RealIndex:
                outputRightSelect.append(1)
            else:
                outputRightSelect.append(0)
            # print(index)
            RewardSum = RewardSum + UpdateIndexReward(CurrentKnowReward,ContXGamblesSelectNum,real,Eststd,index)
        else:
            maxindex = ChooseMaxGamble(CurrentKnowReward)
            if maxindex==RealIndex:
                outputRightSelect.append(1)
            else:
                outputRightSelect.append(0)
            RewardSum = RewardSum + UpdateIndexReward(CurrentKnowReward,ContXGamblesSelectNum,real,Eststd,maxindex)
        outputRewardRecord.append(RewardSum/(i+1))
        # if i%20==0:
        #     plt.scatter(i,RewardSum,alpha=0.6)
    output.append(outputRewardRecord)
    output.append(outputRightSelect)
    return output



numOfGamble = 10
real = RandGenerateREALValue(numOfGamble)

real1 = []
for i in range(len(real)):
    real1.append(real[i])
RealIndex = ChooseMaxGamble(real1) #这是真实的动作
print('real',real)

Eststd = [] #表示由于测量误差在返回测量的值时的标准差
for i in range(numOfGamble):
    Eststd.append(1)


ExperimentTryPars = [0.1,0.01,0]
ColorPlt = ['r','b','k']
for ExperimentTimes in range(len(ExperimentTryPars)):
    Iteration = 1000
    RandSeedOffset = 0
    tryPar = ExperimentTryPars[ExperimentTimes]
    result = []
    for i in range(2000):
        print(i)
        tmp = Experiment_realNotChange(RealIndex,real,Eststd,numOfGamble,Iteration,RandSeedOffset,tryPar)
        result.append(tmp)
        RandSeedOffset = RandSeedOffset+Iteration+2


    AvgRewardInteration = []
    SumRightSelectInteration = []
    for i in range(Iteration):
        AvgRewardInteration_i = 0
        SumRightSelectInteration_i = 0
        for j in range(len(result)):
            AvgRewardInteration_i = AvgRewardInteration_i+result[j][0][i]
            SumRightSelectInteration_i = SumRightSelectInteration_i + result[j][1][i]
        AvgRewardInteration_i = AvgRewardInteration_i/len(result)
        AvgRewardInteration.append(AvgRewardInteration_i)
        SumRightSelectInteration.append(SumRightSelectInteration_i/len(result))
    x = np.arange(len(AvgRewardInteration))
    plt.figure(1)
    plt.plot(x,AvgRewardInteration,ColorPlt[ExperimentTimes])
    plt.figure(2)
    plt.plot(x,SumRightSelectInteration,ColorPlt[ExperimentTimes])






print(AvgRewardInteration[0])
# print('CurrentKnowReward',CurrentKnowReward)
# print('ContXGamblesSelectNum',ContXGamblesSelectNum)
plt.show()

