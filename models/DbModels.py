from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, String, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserInfo(Base):
    __tablename__ = 'user_info'

    user_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键自增')
    user_account = Column(String(50), nullable=False, default='', comment='用户账号，QQ')
    region = Column(String(50), nullable=False, default='+86', comment='地区')
    mobile_number = Column(String(50), nullable=False, default='', comment='手机号')
    create_time = Column(DateTime, nullable=False, comment='创建时间', server_default='CURRENT_TIMESTAMP')
    update_time = Column(
        DateTime,
        nullable=False,
        comment='更新时间',
        server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
    )
    status = Column(Integer, nullable=False, default=1, comment='用户状态，0 - 不可用， 1 - 未激活， 2 - 已激活')

    idx_user_account_mobile_number_status = Index('idx_user_account_mobile_number_status', user_account, mobile_number,
                                                  status)


class MobileVerifyCode(Base):
    __tablename__ = 'mobile_verify_code'

    code_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键')
    mobile_number = Column(String(50), nullable=False, comment='验证码接收号码')
    verify_code = Column(String(32), nullable=False, comment='验证码')
    is_used = Column(Integer, nullable=False, default=0, comment='是否使用 0 否 1 是')
    verify_ip = Column(String(32), nullable=False, comment='核销IP，方便识别一些机器人账号')
    expire_at = Column(DateTime, nullable=False, comment='验证码过期时间')
    biz_type = Column(Integer, nullable=False, default=0, comment='当前业务')
    create_time = Column(DateTime, nullable=False, comment='创建时间', server_default='CURRENT_TIMESTAMP')
    update_time = Column(
        DateTime,
        nullable=False,
        comment='更新时间',
        server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
    )
