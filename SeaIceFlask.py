# SeaIceFlask.py - subclass of Flask. This will store some live
# datastructures in the applicaiton context, including Users, 
# notificaitons, Id pools, Db connector pools, etc.
#
# Copyright (c) 2013, Christopher Patton, all rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * The names of contributors may be used to endorse or promote products
#     derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from flask import Flask
import seaice

MAX_CONNECTIONS = 1

## class SeaIceFlask
#
class SeaIceFlask (Flask): 
  
  def __init__(self, import_name, static_path=None, static_url_path=None,
                     static_folder='static', template_folder='templates',
                     instance_path=None, instance_relative_config=False,
                     db_user=None, db_password=None, db_name=None):

    Flask.__init__(self, import_name, static_path, static_url_path, 
                         static_folder, template_folder,
                         instance_path, instance_relative_config)

    # DB connector pool
    self.dbPool = seaice.SeaIceConnectorPool(MAX_CONNECTIONS, db_user, db_password, db_name)
    db_con = self.dbPool.getScoped()

    # Id pools    
    self.userIdPool = seaice.IdPool(db_con, "Users")
    self.termIdPool = seaice.IdPool(db_con, "Terms")
    self.commentIdPool = seaice.IdPool(db_con, "Comments")
     
    # User structures
    self.SeaIceUsers = {}
    for user in db_con.getAllUsers():
      self.SeaIceUsers[user['id']] = seaice.User(user['id'], 
                                    user['first_name'].decode('utf-8'))

    # Load notifcations TODO
    self.notify_con = seaice.NotifyConnector(db_user, db_password, db_name) 
