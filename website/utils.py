import flask
from flask import Flask
import flask_login



class User(flask_login.UserMixin):
    pass






# Our mock database.
users = {
        'georgeha98@gmail.com': {'password': 'hello'},
        'example@gmail.com': {'password': 'test'},
        'tahiya': {'password': 'pass'},


        }


def plot_predictions(data):
    import matplotlib.pyplot as plt
    plt.switch_backend('agg')



    predictions = data['predictions']
    if  str(predictions[0].keys()[0])=='day' or str(predictions[0].keys()[0])=='day':
        day_or_minutes = 'day-'
    else:
        day_or_minutes = 'minute-'
    x_axis = [ day_or_minutes + str( i+1) for i in xrange(len(predictions))]
    y_axis = []

    for value in predictions:
        y_axis.append(value['predicted_price'])

    fig = plt.figure()

    plt.title('Stock prediction')
    plt.plot(x_axis,y_axis)
    plt.ylabel('Stock Price in  $')
    plt.grid(True)
    fig.savefig('static/stock_predictions.png')

   # plt.show()
    return 'stock_predictions.png'
