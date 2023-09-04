#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import app
from log import initLog

logging = initLog('wechat.log','runserver')

if __name__ == '__main__':
    app.run(debug=True,port=8000,host='0.0.0.0')

application = app
