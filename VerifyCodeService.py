import logging
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from models.DbModels import MobileVerifyCode


def check_or_create_verify_code(db: Session, mobile_number: str, ip: str) -> str:
    # 查询是否有未过期的验证码
    now = datetime.now()
    verify_code = db.query(MobileVerifyCode) \
        .filter(MobileVerifyCode.mobile_number == mobile_number) \
        .filter(MobileVerifyCode.is_used == 0) \
        .filter(MobileVerifyCode.expire_at > now) \
        .order_by(MobileVerifyCode.create_time.desc()) \
        .first()

    if verify_code:
        # 如果存在未过期的验证码，则返回该验证码，并打印日志
        logging.warning(f'Found unexpired verify code for {mobile_number}: {verify_code.verify_code}')
        return verify_code.verify_code
    else:
        # 不存在未过期的验证码，则生成新验证码并保存到数据库中
        import random
        verify_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        expire_at = now + timedelta(minutes=5)
        new_verify_code = MobileVerifyCode(
            mobile_number=mobile_number,
            verify_code=verify_code,
            is_used=0,
            verify_ip=ip,
            expire_at=expire_at,
            biz_type=0
        )
        db.add(new_verify_code)
        db.commit()
        logging.info(f'Created new verify code for {mobile_number}: {verify_code}')
        return verify_code


def check_verify_code(db: Session, mobile_number: str, input_code: str) -> bool:
    # 查询最近发送给该手机号的验证码
    verify_code = db.query(MobileVerifyCode) \
        .filter(MobileVerifyCode.mobile_number == mobile_number) \
        .filter(MobileVerifyCode.is_used == 0) \
        .order_by(MobileVerifyCode.create_time.desc()) \
        .first()

    if not verify_code:
        # 未找到验证码
        return False
    elif verify_code.verify_code != input_code:
        # 验证码不匹配
        return False
    else:
        # 标记验证码已使用
        verify_code.is_used = 1
        db.commit()
        return True
