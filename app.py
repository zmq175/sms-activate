import logging

from flask import Flask, render_template

from datetime import datetime, timedelta

from flask import Flask, request, jsonify
from sqlalchemy.orm import Session

import MySQL
from models.DbModels import UserInfo, MobileVerifyCode
from SmsUtils import send_verify_code

app = Flask(__name__)

# 定义验证码有效期为5分钟
VERIFY_CODE_EXPIRE_TIME = 5 * 60
# 定义发送验证码的间隔时间为60秒
SEND_VERIFY_CODE_INTERVAL = 60
db = MySQL.session


@app.route('/api/get_verify_code', methods=['POST'])
def get_verify_code():
    # 获取请求参数
    account = request.json.get('account')
    mobile_number = request.json.get('mobile_number')

    # 查询用户是否存在，如果不存在则创建用户
    user = db.query(UserInfo).filter(UserInfo.user_account == account).first()
    if not user:
        user = UserInfo(user_account=account)
        db.add(user)
        db.commit()

    # 判断距离上次发送短信的时间是否超过60秒
    last_sent_time = db.query(MobileVerifyCode.update_time).filter(
        MobileVerifyCode.mobile_number == mobile_number
    ).order_by(MobileVerifyCode.update_time.desc()).first()
    now = datetime.now()
    if last_sent_time is not None:
        last_sent_time = last_sent_time[0].replace(tzinfo=None)
    if last_sent_time is not None and (now - last_sent_time).total_seconds() < SEND_VERIFY_CODE_INTERVAL:
        return jsonify({'error': '发送验证码太频繁，请稍后再试'})

    # 判断当前用户是否有未过期的验证码
    last_verify_code = db.query(MobileVerifyCode.verify_code, MobileVerifyCode.update_time).filter(
        MobileVerifyCode.mobile_number == mobile_number
    ).order_by(MobileVerifyCode.update_time.desc()).first()
    if last_verify_code is not None and (now - last_verify_code.update_time).total_seconds() < VERIFY_CODE_EXPIRE_TIME:
        return jsonify({'error': '您的验证码还未过期，请勿重复获取'})

    # 发送验证码
    user_ip = request.remote_addr
    send_verify_code(mobile_number=mobile_number, ip=user_ip)

    return jsonify({'message': 'OK'})


@app.route('/api/validate_code', methods=['POST'])
def validate_code():
    account = request.json.get('account')
    mobile_number = request.json.get('mobile_number')
    code = request.json.get("code")
    verify_code = db.query(MobileVerifyCode).filter(MobileVerifyCode.mobile_number == mobile_number,
                                                    MobileVerifyCode.is_used == 0) \
        .order_by(MobileVerifyCode.update_time.desc()).first()
    if verify_code.verify_code != code:
        return jsonify({'succeed': False, 'message': 'OK'})
    verify_code.is_used = True
    user = db.query(UserInfo).filter(UserInfo.user_account == account).first()
    user.mobile_number = mobile_number
    user.status = 2
    db.commit()
    return jsonify({'succeed': True, 'message': 'OK'})


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(Exception)
def handle_exception(error):
    logging.exception(str(error))
    response = jsonify({'error': str(error)})
    response.status_code = 500
    return response


if __name__ == '__main__':
    app.run()
