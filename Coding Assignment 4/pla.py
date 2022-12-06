import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import csv


# def createSampleData():
#     samples = np.array([[2, -2], [4.5, -3.5], [1, 1], [-1, -2]])
#     labels = [-1, -1, 1, 1]
#     return samples, labels

def getData():
    filename = "./data1.csv"
    df = pd.read_csv(filename, header=None, names=['x', 'y', 'label'])
    # print(df)
    sample_list = []
    label_list = []
    for row_index, row in df.iterrows():
        sample_list.append([row['x'], row['y']])
        label_list.append(row['label'])
    # print(sample_list, label_list)
    samples = np.array(sample_list)
    return samples, label_list


def save_csv(w, b):
    with open("results1.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([w[0][0], w[1][0], b])
    return


# Train perceptron model
class Perceptron:
    def __init__(self, x, y, a=1):
        self.x = x
        self.y = y
        self.w = np.zeros((x.shape[1], 1))  # default setting weights, w1=w2=0
        self.b = 0
        self.a = 1  # learning rate
        self.numsamples = self.x.shape[0]
        self.numfeatures = self.x.shape[1]

    def sign(self, w, b, x):
        y = np.dot(x, w) + b
        return int(y)

    def update(self, label_i, data_i):
        tmp = label_i * self.a * data_i
        tmp = tmp.reshape(self.w.shape)
        # update w and b
        self.w = tmp + self.w
        self.b = self.b + label_i * self.a

    def train(self):
        isFind = False
        while not isFind:
            count = 0
            save_csv(self.w, self.b)
            for i in range(self.numsamples):
                tmpY = self.sign(self.w, self.b, self.x[i, :])
                if tmpY * self.y[i] <= 0:  # if it's wrong classification point
                    print('wrong classification point is:', self.x[i, :], ', current w and b: ', self.w, self.b)
                    count += 1
                    self.update(self.y[i], self.x[i, :])
            if count == 0:
                print('w and b after final training: ', self.w, self.b)
                isFind = True
        return self.w, self.b


def main():
    '''YOUR CODE GOES HERE'''

    # plot
    class Picture:
        def __init__(self, data, w, b, labels):
            self.b = b
            self.w = w
            plt.figure(1)
            plt.title('Perceptron Learning Algorithm (PLA)', size=14)
            plt.xlabel('x0 - axis', size=14)
            plt.ylabel('x1 - axis', size=14)

            xData = np.linspace(0, 17, 100)
            yData = self.expression(xData)
            plt.plot(xData, yData, color='r', label='sample data')

            for i in range(len(data)):
                # print(labels[i])
                if labels[i] >= 0:
                    plt.scatter(data[i][0], data[i][1], s=50)
                else:
                    plt.scatter(data[i][0], data[i][1], s=50, marker='x')

            plt.savefig('pla_fig.png', dpi=75)

        def expression(self, x):
            y = (-self.b - self.w[0] * x) / self.w[
                1]  # here, x0 and x1 are two axis. x1 is independent variable, x2 is dependent variable.
            return y

        def Show(self):
            plt.show()

    samples, labels = getData()  # load in csv file

    myperceptron = Perceptron(x=samples, y=labels)
    weights, bias = myperceptron.train()
    Picture = Picture(samples, weights, bias, labels)
    Picture.Show()


if __name__ == "__main__":
    """DO NOT MODIFY"""
    main()
