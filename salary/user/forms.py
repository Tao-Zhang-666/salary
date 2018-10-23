# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length

from .models import User, Dept


class RegisterForm(FlaskForm):
    """Register form."""
    employee = StringField('工号',
                           validators=[DataRequired(), Length(min=5, max=10)])
    username = StringField('姓名',
                           validators=[DataRequired(), Length(min=3, max=10)])
    dept_id = SelectField('部门', coerce=int)

    password = PasswordField('密码',
                             validators=[DataRequired(), Length(min=6, max=10)])
    confirm = PasswordField('密码',
                            [DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None
        self.dept_id.choices = [(dept.id, dept.name) for dept in Dept.query.all()]

    # choices需要一个列表里面包含数个键值对应的元组
    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(employee=self.employee.data).first()
        if user:
            self.employee.errors.append('Employee already registered')
            return False
        return True
