# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin

from salary.database import Column, Model, SurrogatePK, db, reference_col, relationship
from salary.extensions import bcrypt


class Dept(SurrogatePK, Model):
    """A dept of the app."""
    __tablename__ = 'depts'
    name = Column(db.String(80), unique=True, nullable=False)

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Dept({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    employee = Column(db.String(10), unique=True, nullable=False)   # 工号
    username = Column(db.String(10), nullable=False)                # 姓名
    #: The hashed password
    password = Column(db.Binary(128), nullable=True)                # 密码
    dept_id = reference_col('depts', nullable=True)                 # 部门
    dept = relationship('Dept', backref='users')

    # rank = Column(db.String(10), nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, employee, username, dept_id, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, employee=employee, username=username, dept_id=dept_id, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({employee!r})>'.format(employee=self.employee)
