from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort, jsonify


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+cymysql://root:yanghaa@127.0.0.1:3306/demo?charset=utf8'

# 设置每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Role(db.Model):
    # 定义表名
    __tablename__ = 'roles'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # us = db.relationship('User', backref='role')

    # repr()方法显示一个可读字符串
    def __repr__(self):
        return 'Role:%s' % self.name


# 测试数据暂时存放
tasks = []


@app.route('/add_task/', methods=['POST'])
def add_task():
    if not request.json or 'id' not in request.json or 'info' not in request.json:
        abort(400)
    task = {
        'id': request.json['id'],
        'info': request.json['info']
    }
    tasks.append(task)
    return jsonify(tasks)


@app.route('/get_task/', methods=['GET'])
def get_task():
    if not request.args or 'id' not in request.args:
        # 没有指定id则返回全部
        return jsonify(tasks)
    else:
        task_id = request.args['id']
        task = list(filter(lambda t: t['id'] == int(task_id), tasks))
        return jsonify(task) if task else jsonify({'result': 'not found'})


@app.route('/db_search/', methods=['GET'])
def db_search():
    if not request.args or 'name' not in request.args:
        return jsonify({'error': 'args=none'})
    else:
        # search_id = request.args['id']
        search_name = request.args['name']
        user_role = Role.query.filter_by(name=search_name).first()
        return jsonify({'id': user_role.id, 'name': user_role.name}) if user_role else jsonify({'result': 'not found'})


@app.route('/db_insert/', methods=['POST'])
def db_insert():
    if not request.json or 'name' not in request.json:
        return jsonify({'error': 'date error'})
    else:
        username = request.json['name']
        role_temp = Role(name=username)
        db.session.add(role_temp)
        db.session.commit()
        role_result = Role.query.filter_by(name=username).first()
        return jsonify({'id': role_result.id, 'name': role_result.name, 'message': 'success'})
        # return jsonify({'message':'success'})


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    ro1 = Role(name='admin')
    ro2 = Role(name='user')
    db.session.add_all([ro1, ro2])
    db.session.commit()
    # import pdb
    # pdb.set_trace()
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    app.run(host="0.0.0.0", debug=True)
