from math import sqrt


def error(target, prediction):
    error = []
    for i in range(len(target)):
        error.append(target[i] - prediction[i])

    print("Errors: ", error)
    print(error)

    squaredError = []
    absError = []
    for val in error:
        squaredError.append(val * val)  # target-prediction之差平方
        absError.append(abs(val))  # 误差绝对值

    print("Square Error: ", squaredError)
    print("Absolute Value of Error: ", absError)
    print("MSE = ", sum(squaredError) / len(squaredError))  # 均方误差MSE

    print("RMSE = ", sqrt(sum(squaredError) / len(squaredError)))  # 均方根误差RMSE
    print("MAE = ", sum(absError) / len(absError))  # 平均绝对误差MAE
