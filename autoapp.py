# -*- coding: utf-8 -*-
"""Create an application instance."""
from salary.app import create_app

app = create_app()

# 添加下面的语句
if __name__ == '__main__':
    app.run()
