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

def EqualGenerateREALValue(numOfGamble,value):
    output = []
    for i in range(numOfGamble):
        output.append(value)
    return output

def ChooseMaxGamble(RandomResult):
    tmp = []
    for i in range(len(RandomResult)):
        tmp.append(RandomResult[i])
    index = tmp.index(max(tmp))
    return index

def UpdateIndexRewardAVG(CurrentKnowReward,ContXGamblesSelectNum,real,std,index):
    "更新对应的index估计值 通过采样平均和增量式计算动作价值方法"

    ContXGamblesSelectNum[index] = ContXGamblesSelectNum[index]+1
    # np.random.seed(int(time.time()))
    reward = np.random.normal(real[index],std[index],1)
    reward = reward[0]
    # print(reward)
    CurrentKnowReward[index] = CurrentKnowReward[index]+1/ContXGamblesSelectNum[index]*(reward-CurrentKnowReward[index])
    # print(CurrentKnowReward)
    return reward

def UpdateIndexRewardConstant(CurrentKnowReward,real,std,index,Alpha):
    "更新对应的index估计值 通过常数计算动作价值方法"

    # np.random.seed(int(time.time()))
    reward = np.random.normal(real[index],std[index],1)
    reward = reward[0]
    # print(reward)
    CurrentKnowReward[index] = CurrentKnowReward[index]+Alpha*(reward-CurrentKnowReward[index])
    # print(CurrentKnowReward)
    return reward

def CopyList(list):
    out = []
    for i in range(len(list)):
        out.append(list[i])
    return out

def Experiment_realChange(CallTimes,real,Eststd,numOfGamble,Iteration,tryPar):
    "CallTimes是调用的次数"
    CurrentKnowRewardAvg = GetCurrentXTestReward(real,Eststd,numOfGamble)
    CurrentKnowRewardConstant = CopyList(CurrentKnowRewardAvg)


    # real1 = []
    # for i in range(len(real)):
    #     real1.append(real[i])
    RealIndex = ChooseMaxGamble(real) #这是真实的最大动作
    #
    # print('InitCurrentKnowReward',CurrentKnowReward)

    ContXGamblesSelectNum = [];
    for i in range(numOfGamble):
        ContXGamblesSelectNum.append(0)


    outputRewardRecordAvg = []
    outputRewardRecordConstant = []
    outputRewardRecordReal = []

    outputRightSelectAvg = []
    outputRightSelectConstant = []
    # tryPar = 0
    RewardSumAVG = 0
    RewardSumConstant=0
    RewardSumReal = 0 #真实的最优动作的和
    # plt.figure()
    noise = np.random.normal(0,0.01,len(real)*Iteration)
    for i in range(Iteration):
        # print(i)
        RewardSumReal = RewardSumReal + real[RealIndex]
        thisrandom = np.random.random()
        # print(thisrandom)
        if thisrandom<tryPar:
            # print(thisrandom)
            # np.random.seed(int(time.time()))
            index = np.random.randint(0,numOfGamble)
            # print(index)
            if index==RealIndex:
                outputRightSelectAvg.append(1)
                outputRightSelectConstant.append(1)
            else:
                outputRightSelectAvg.append(0)
                outputRightSelectConstant.append(1)
            # print(index)
            RewardSumAVG = RewardSumAVG + UpdateIndexRewardAVG(CurrentKnowRewardAvg,ContXGamblesSelectNum,real,Eststd,index)
            RewardSumConstant = RewardSumConstant + UpdateIndexRewardConstant(CurrentKnowRewardConstant,real,Eststd,index,0.1)
        else:
            maxindexAvg = ChooseMaxGamble(CurrentKnowRewardAvg)
            maxindexConstant = ChooseMaxGamble(CurrentKnowRewardConstant)
            if maxindexAvg==RealIndex:
                outputRightSelectAvg.append(1)
            else:
                outputRightSelectAvg.append(0)
            if maxindexConstant==RealIndex:
                outputRightSelectConstant.append(1)
            else:
                outputRightSelectConstant.append(0)
            RewardSumAVG = RewardSumAVG + UpdateIndexRewardAVG(CurrentKnowRewardAvg,ContXGamblesSelectNum,real,Eststd,maxindexAvg)
            RewardSumConstant = RewardSumConstant + UpdateIndexRewardConstant(CurrentKnowRewardConstant,real,Eststd,maxindexConstant,0.1)
        outputRewardRecordAvg.append(RewardSumAVG/(i+1))
        outputRewardRecordConstant.append(RewardSumConstant/(i+1))
        outputRewardRecordReal.append(RewardSumReal/(i+1))

        addNoise2realValue(real,noise[(i)*len(real):(i+1)*len(real)])
        # real1 = []
        # for i in range(len(real)):
        #     real1.append(real[i])
        # np.random.seed(int(time.time()))
        RealIndex = ChooseMaxGamble(real) #这是真实的最大动作
        # print(RealIndex)
        # if i%20==0:
        #     plt.scatter(i,RewardSum,alpha=0.6)

    for i in range(Iteration):
        AvgRewardInterationAvg[i] = AvgRewardInterationAvg[i]+1/CallTimes*(outputRewardRecordAvg[i]-AvgRewardInterationAvg[i])
        SumRightSelectInterationAvg[i] = SumRightSelectInterationAvg[i]+1/CallTimes*(outputRightSelectAvg[i]-SumRightSelectInterationAvg[i])
        AvgRewardInterationConstant[i] = AvgRewardInterationConstant[i]+1/CallTimes*(outputRewardRecordConstant[i]-AvgRewardInterationConstant[i])
        SumRightSelectInterationConstant[i] = SumRightSelectInterationConstant[i]+1/CallTimes*(outputRightSelectConstant[i]-SumRightSelectInterationConstant[i])
        AvgRewardInterationReal[i] = AvgRewardInterationReal[i]+1/CallTimes*(outputRewardRecordReal[i]-AvgRewardInterationReal[i])

    # output.append(outputRewardRecordAvg)
    # output.append(outputRewardRecordConstant)
    # output.append(outputRightSelectAvg)
    # output.append(outputRightSelectConstant)
    # output.append(outputRewardRecordReal)
    return

def addNoise2realValue(real,noise):
    for i in range(len(real)):
        ramd = noise[i]
        real[i] = real[i] + ramd
        # print(ramd)
    return

numOfGamble = 10
# real = RandGenerateREALValue(numOfGamble)
real = EqualGenerateREALValue(numOfGamble,0)

print('real',real)

Eststd = [] #表示由于测量误差在返回测量的值时的标准差
for i in range(numOfGamble):
    Eststd.append(1)


ExperimentTryPars = [0.1,0.01,0]
ColorPlt = ['r','g','b']
rewardmaxstore = []
rewardminstore = []
for ExperimentTimes in range(len(ExperimentTryPars)):
    Iteration = 10000
    tryPar = ExperimentTryPars[ExperimentTimes]
    result = []


    AvgRewardInterationAvg = [0]*Iteration
    SumRightSelectInterationAvg = [0]*Iteration
    AvgRewardInterationConstant = [0]*Iteration
    SumRightSelectInterationConstant = [0]*Iteration
    AvgRewardInterationReal = [0]*Iteration
    for i in range(2000):
        print(i)
        Experiment_realChange(i+1,real,Eststd,numOfGamble,Iteration,tryPar)
        real = EqualGenerateREALValue(numOfGamble,0)




    # for i in range(Iteration):
    #     AvgRewardInteration_iAvg = 0
    #     SumRightSelectInteration_iAvg = 0
    #     for j in range(len(result)):
    #         AvgRewardInteration_iAvg = AvgRewardInteration_iAvg+result[j][0][i]
    #         SumRightSelectInteration_iAvg = SumRightSelectInteration_iAvg + result[j][2][i]
    #     AvgRewardInteration_iAvg = AvgRewardInteration_iAvg/len(result)
    #     AvgRewardInterationAvg.append(AvgRewardInteration_iAvg)
    #     SumRightSelectInterationAvg.append(SumRightSelectInteration_iAvg/len(result))
    #
    #
    # for i in range(Iteration):
    #     AvgRewardInteration_iConstant = 0
    #     SumRightSelectInteration_iConstant = 0
    #     for j in range(len(result)):
    #         AvgRewardInteration_iConstant = AvgRewardInteration_iConstant+result[j][1][i]
    #         SumRightSelectInteration_iConstant = SumRightSelectInteration_iConstant + result[j][3][i]
    #     AvgRewardInteration_iConstant = AvgRewardInteration_iConstant/len(result)
    #     AvgRewardInterationConstant.append(AvgRewardInteration_iConstant)
    #     SumRightSelectInterationConstant.append(SumRightSelectInteration_iConstant/len(result))
    #
    #
    # for i in range(Iteration):
    #     AvgRewardInteration_iReal = 0
    #     for j in range(len(result)):
    #         AvgRewardInteration_iReal = AvgRewardInteration_iReal+result[j][4][i]
    #     AvgRewardInteration_iReal = AvgRewardInteration_iReal/len(result)
    #     AvgRewardInterationReal.append(AvgRewardInteration_iReal)

    print('beginPlot')
    x = np.arange(len(AvgRewardInterationAvg))

    RewardMax = []
    RewardMax.append(max(AvgRewardInterationAvg))
    RewardMax.append(max(AvgRewardInterationConstant))
    RewardMax.append(max(AvgRewardInterationReal))
    RewardMax = max(RewardMax)
    rewardmaxstore.append(RewardMax)

    RewardMin = []
    RewardMin.append(min(AvgRewardInterationAvg))
    RewardMin.append(min(AvgRewardInterationConstant))
    RewardMin.append(min(AvgRewardInterationReal))
    RewardMin = min(RewardMin)
    rewardminstore.append(RewardMin)

    plt.figure(1)
    plt.subplot(231)
    plt.plot(x,AvgRewardInterationAvg,ColorPlt[ExperimentTimes])
    plt.ylim(min(rewardminstore),max(rewardmaxstore))
    plt.subplot(234)
    plt.plot(x,SumRightSelectInterationAvg,ColorPlt[ExperimentTimes])
    plt.ylim(-0.1,1.1)
    plt.subplot(232)
    plt.plot(x,AvgRewardInterationConstant,ColorPlt[ExperimentTimes])
    plt.ylim(min(rewardminstore),max(rewardmaxstore))
    plt.subplot(235)
    plt.plot(x,SumRightSelectInterationConstant,ColorPlt[ExperimentTimes])
    plt.ylim(-0.1,1.1)
    plt.subplot(233)
    plt.plot(x,AvgRewardInterationReal,ColorPlt[ExperimentTimes])
    plt.ylim(min(rewardminstore),max(rewardmaxstore))
    plt.figure(2)
    plt.plot(x,AvgRewardInterationReal,ColorPlt[ExperimentTimes])
    plt.figure(3)
    plt.plot(x,SumRightSelectInterationAvg,ColorPlt[ExperimentTimes])
    plt.figure(4)
    plt.plot(x,SumRightSelectInterationConstant,ColorPlt[ExperimentTimes])




# print('CurrentKnowReward',CurrentKnowReward)
# print('ContXGamblesSelectNum',ContXGamblesSelectNum)
plt.show()

