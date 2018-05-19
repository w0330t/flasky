from flask import Flask, request, make_response, redirect, abort
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def index():
    # return 'Hello World!'

    # 返回UserAgent
    # user_agent = request.headers.get('User-Agent')
    # return '<p>Your browser is %s</p>' % user_agent

    # 返回状态码
    # return '<h1>Bad Request</h1>', 400

    # 返回对象并设置cookie
    # response = make_response('<h1>This document carries a cookie!</h1>')
    # response.set_cookie('answer', '42')
    # return response

    # 重定向
    return redirect('http://baidu.com')

@app.route('/user/<id>')
def get_user(id):
    '''特殊的响应'''
    # user = load_user(id)
    user = None
    if not user:
        print('1111111111')
        abort(404)
    return '<h1>Hello, %s</h1>' %user


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s</h1>' %name

if __name__ == '__main__':
    # app.run()
    manager.run()