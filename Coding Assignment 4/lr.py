import csv

import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt

def main():
    """
    YOUR CODE GOES HERE
    Implement Linear Regression using Gradient Descent, with varying alpha values and numbers of iterations.
    Write to an output csv file the outcome betas for each (alpha, iteration #) setting.
    Please run the file as follows: python3 lr.py data2.csv, results2.csv
    """
    def save_csv(alpha, num_iter, b_0, b_age, b_weight):
        with open("results2.csv", "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([alpha, num_iter, b_0, b_age, b_weight])
        csvfile.close()
        return

    def linear_regression(alpha):
        # Getting data
        data = genfromtxt(r"data2.csv", delimiter=",")
        x_data = data[:, :-1]  # col, row
        y_data = data[:, -1]  # col, row

        # Data Preparation and Normalization

        mean1 = np.mean(data[:, 0])
        mean2 = np.mean(data[:, 1])
        var1 = np.var(data[:, 0])
        var2 = np.var(data[:, 1])
        # a = list(data[:, 0])
        # b = list(data[:, 1])
        # a.extend(b) # combine a and b together
        # mean = np.mean(a)
        # var = np.var(b)

        x_data[:, 0] = (x_data[:, 0] - mean1) / var1
        x_data[:, 1] = (x_data[:, 1] - mean2) / var2
        # x_data = (x_data - mean) / var

        # 学习率 learning rate
        lr = alpha

        # 参数 bias = theta
        theta_0 = 0
        theta_1 = 0
        theta_2 = 0

        # 最大迭代次数 iteration number
        num_iter = 100

        # 最小二乘法 Using the least square method to compute error
        def calculate_error(theta_0, theta_1, theta_2, x_data, y_data):
            totalError = 0
            for i in range(0, len(x_data)):
                totalError += (y_data[i] - (theta_1 * x_data[i, 0] + theta_2 * x_data[i, 1] + theta_0)) ** 2
            return totalError / float(len(x_data))

        def gradient_descent(x_data, y_data, theta_0, theta_1, theta_2, lr, num_iter):
            # 计算总数据量 Calculate total data size
            m = float(len(x_data))

            # iteration
            for i in range(num_iter):
                theta_0_grad = 0
                theta_1_grad = 0
                theta_2_grad = 0

                # 计算梯度总和再求平均 Calculate using the formula
                for j in range(0, len(x_data)):
                    theta_0_grad += -(1 / (2 * m)) * (
                                y_data[j] - (theta_1 * x_data[j, 0] + theta_2 * x_data[j, 1] + theta_0))
                    theta_1_grad += -(1 / (2 * m)) * x_data[j, 0] * (
                                y_data[j] - (theta_1 * x_data[j, 0] + theta_2 * x_data[j, 1] + theta_0))
                    theta_2_grad += -(1 / (2 * m)) * x_data[j, 0] * (
                                y_data[j] - (theta_1 * x_data[j, 0] + theta_2 * x_data[j, 1] + theta_0))

                # 更新参数 Update betas
                theta_0 = theta_0 - (lr * theta_0_grad)
                theta_1 = theta_1 - (lr * theta_1_grad)
                theta_2 = theta_2 - (lr * theta_2_grad)
            return theta_0, theta_1, theta_2

        print('\nAlpha = ',alpha ,', staring error = {3}'.format(theta_0, theta_1, theta_2,
                                                                                    calculate_error(theta_0, theta_1,
                                                                                                  theta_2, x_data,
                                                                                                  y_data)))
        theta_0, theta_1, theta_2 = gradient_descent(x_data, y_data, theta_0, theta_1, theta_2, lr, num_iter)  # 开始建模
        print('After 100 iterations, bias = {1}, b_age = {2}, b_weight = {3}, final error = {4}'.format(num_iter, theta_0, theta_1, theta_2,
                                                                             calculate_error(theta_0, theta_1, theta_2,
                                                                                           x_data, y_data)))

        # save CSV
        save_csv(alpha, num_iter, theta_0, theta_1, theta_2)

        # make 3d plot
        ax = plt.figure().add_subplot(111, projection="3d")
        ax.scatter(x_data[:, 0], x_data[:, 1], y_data, c='r', marker='o', s=50)  # 点为红色三角形 s代表点的大小
        x0 = x_data[:, 0]
        x1 = x_data[:, 1]

        # Generate mesh grid matrix
        x0, x1 = np.meshgrid(x0, x1)
        z = theta_0 + x0 * theta_1 + x1 * theta_2

        ax.plot_surface(x0, x1, z)

        # set axis
        ax.set_xlabel('Normalized Age (years)')
        ax.set_ylabel("Normalized Weight (kg) ")
        ax.set_zlabel('Height (m)')
        ax.title.set_text("alpha = " + str(alpha))
        plt.show()

    print('Running linear regression with gradient descend, with different alphas...')
    linear_regression(0.001)
    linear_regression(0.005)
    linear_regression(0.01)
    linear_regression(0.05)
    linear_regression(0.1)
    linear_regression(0.5)
    linear_regression(1)
    linear_regression(5)
    linear_regression(10)

    '''
    We can find that when num_iter = 100, alpha = 0.5 or 1 gives minimum final error,
    So I choose alpha = 0.75 as my choice for the tenth alpha value.
    '''
    linear_regression(0.75)


if __name__ == "__main__":
    main()