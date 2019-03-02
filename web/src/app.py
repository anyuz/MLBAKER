# app.py
import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
import pymongo
import numpy as np
import pandas
import matplotlib.pyplot as plt
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import argparse
import sys

# parsing arguments
parser = argparse.ArgumentParser(description="Web app to visualize model accuracy")
parser.add_argument("--mongodb")
parser.add_argument("--user")
parser.add_argument("--password")
parser.add_argument("--port",type=int)
arg = parser.parse_args(sys.argv[1:])
print (arg.user, arg.mongodb, arg.password)
# main

app = Flask(__name__)

# Set up database connection.
client = pymongo.MongoClient("mongodb://%s:%s@%s"%(arg.user, arg.password, arg.mongodb))
db = client["model"]
mycol = db.accuracy
accuracy = mycol.find({})
accuracydata = []
for x in accuracy:
    accuracydata.append(x['accuracy'])
#print(accuracydata)
accuracyfolddata = []
folddata = db['accuracyround']
accuracyfold = folddata.find({})
for x in accuracyfold:
    accuracyfolddata.append([x['Fold1'], x['Fold2'], x['Fold3'], x['Fold4'], x['Fold5'], x['Fold6'], x['Fold7'], x['Fold8'], x['Fold9'], x['Fold10']])

@app.route('/')
def index():
    ip = request.remote_addr
    return render_template('index.html', user_ip=ip)


@app.route('/modelscompare.png')
def plot_png1():
    fig = create_figure_compare()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure_compare():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title('Models different folds Comparison')
    axis.set_xlabel('folds')
    axis.set_ylabel('RSME Accuracy')
    for i in range(len(accuracyfolddata)):
        xs = range(1, 11)
        ys = accuracyfolddata[i]
        axis.plot(xs, ys)
    return fig

@app.route('/modelsdevelop.png')
def plot_png2():
    fig = create_figure_develop()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure_develop():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title('Models Development with update')
    axis.set_xlabel('Model Version')
    axis.set_ylabel('RSME Accuracy')
    xs = range(1,len(accuracydata)+1)
    ys = accuracydata
    axis.plot(xs, ys,'--')
    return fig

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=arg.port)