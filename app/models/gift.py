from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Gift(Base):
    """
    软删除 互联网行业 分析用户行为
    """
    id = Column(Integer, primary_key=True)
    user = relationship('User')  # relationship函数表明引用关系
    uid = Column(Integer, ForeignKey('user.id'))  # 模型user的id号 user小写是因为取的是上一行user变量名字 自动创建外键关系
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)
