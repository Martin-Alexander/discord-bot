import os
import csv

variable = []
MEMBERS = csv.reader(open("members.csv"), delimiter=",")

for line in MEMBERS:
  if line[2] != "NULL":
    variable.append(line[1] + ":" + line[2] + ",")

os.system("heroku config:set MESSANGER_NOTIFICATION_GANG=" + "".join(variable))