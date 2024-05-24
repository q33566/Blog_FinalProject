from flask import Flask,redirect,url_for,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy.exc import IntegrityError
from flask import flash
import re

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# db = SQLAlchemy()
# db.init_app(app)
class thaha:
    hi = 'll'