from flask_sqlalchemy import SQLAlchemy

from flask import Flask,render_template,request

db = SQLAlchemy()



class Train(db.Model):
    __tablename__= "Train" #Train là tên bảng
    train_id = db.Column(db.Integer, primary_key=True) 
    Start = db.Column(db.String(500), nullable=False)
    Stop = db.Column(db.String(500), nullable=False)
    Start_time = db.Column(db.String(20), nullable=False)
    Time_arrival = db.Column(db.String(20), nullable=False)
class Stop(db.Model):
    __tablename__= "Stop" #Stop là tên bảng
    stop_id = db.Column(db.Integer)
    stop_name = db.Column(db.String(500), primary_key=True)

class train_stop(db.Model):
    __tablename__= "train_stop" #train_stoplà tên bảng
    train_id = db.Column(db.Integer, primary_key=True)
    stop_id = db.Column(db.Integer, primary_key=True)
