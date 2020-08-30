Richard Sutton's book
Reinforcement learning An introduction second edition 

编程练习题

## P33
n臂赌博机，采样平均和增量式计算的动作-价值方法以及常数步长参数动作价值方法跟踪平稳和非平稳问题。

平稳表示真实的收益值在采样过程中不变化，n臂赌博机的真实值服从一正态分布，期望能够通过采样的方式找到最优的真实值。

非平稳表示真实的收益值在采样过程中变化。

平稳问题对应的代码是Stable.py，非平稳问题对应的代码是Unstable.py

### 平稳问题
![image](https://github.com/Robotics-Zhikai/Reinforcement-Learning/blob/master/Reinforcement%20Learning%20An%20Introduction/P33/image/%E5%B9%B3%E7%A8%B3%20%E4%B8%8D%E5%90%8C%E5%8F%82%E6%95%B0%E5%B9%B3%E5%9D%87%E6%94%B6%E7%9B%8A.png)

这是平稳状态下不同参数的对应训练轮次的估计值的平均值，横坐标是训练迭代轮次，纵坐标是平均收益，平均收益的最大值应该是实际值中的最大值。曲线上的每一点都代表2000次实验的平均值，红色曲线代表随机采样的概率是0.1，最优采样的概率是0.9；蓝色曲线代表随机采样的概率是0.01；黑色曲线代表随机采样的概率是0.

![image](https://github.com/Robotics-Zhikai/Reinforcement-Learning/blob/master/Reinforcement%20Learning%20An%20Introduction/P33/image/%E5%B9%B3%E7%A8%B3%20%E4%B8%8D%E5%90%8C%E5%8F%82%E6%95%B0%E6%9C%80%E4%BC%98%E5%8A%A8%E4%BD%9C%E7%99%BE%E5%88%86%E6%AF%94.png)

这是平稳状态下不同参数的最优动作百分比，百分比是根据每一点2000次实验中正好采到了最优动作所占比例来绘制的。

### 非平稳问题
![image](https://github.com/Robotics-Zhikai/Reinforcement-Learning/blob/master/Reinforcement%20Learning%20An%20Introduction/P33/image/%E9%9D%9E%E5%B9%B3%E7%A8%B3%20%E5%B9%B3%E5%9D%87%E9%87%87%E6%A0%B7%E5%92%8C%E5%B8%B8%E6%95%B0%E6%AD%A5%E9%95%BF%E5%AE%9E%E9%AA%8C%E5%AF%B9%E6%AF%94%20%E5%B9%B3%E5%9D%87%E6%94%B6%E7%9B%8A%E5%92%8C%E6%9C%80%E4%BC%98%E5%8A%A8%E4%BD%9C.png)

这是非平稳状态和平稳状态下不同参数的实验结果对比。

(:,1)表示随机采样跟踪非平稳问题

(:,2)表示常数步长，值为0.1跟踪非平稳问题

(2,:)表示对应的最优动作百分比

同样的，每一点都表示2000次独立的实验的平均值。(1,3)子图表示10臂赌博机，每一次都选真实最优值时的2000次实验对应训练轮次的平均值；

红色代表随机采样概率为0.1，根据估计值贪心采的概率是0.9；绿色代表随机采样概率为0.01；蓝色代表随机采样概率为0，每次都根据估计值贪心的去采。

可以看到，常数步长跟踪非平稳问题相对平均采样来说具有较好的跟踪性能，且随机采样的概率越高，跟踪性能越好，从(2,2)子图可以看出。这是因为指数近因加权平均（常数参数）更容易使得在跟踪变化的参数过程中突出新的变化，因而也更容易得到更优的结果；而随机概率越大，越容易修正估计如果出错的结果。

具体理论上的分析可能要利用随机过程



















