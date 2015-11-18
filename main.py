import subprocess
import os

settings = { 'python-exe': 'python',
             'oer-exports-path': '/home/vagrant/production/oer.exports',
             'print-style': 'ccap-physics',
             'prince-path': '/usr/bin/prince',
             'colllection-path':'/home/vagrant/development/CNX-Inspection/data/col11287_1.1_complete',
             'output-path':'/home/vagrant/development/CNX-Inspection/data/col11287_1.1_complete.pdf',
             'git-hash':'7a0bcc69ce90b5cb15666184c4bd3dde26959aef'
             }


db_connection_string = "dbname=training-data user=qa password=qa host=localhost port=5432"

# get current git commit hash

command = "git rev-parse HEAD"

start_git_hash=subprocess.check_output(command.split(),cwd=settings['oer-exports-path'])

print start_git_hash

# switch to default hash

command = "git checkout {git-hash}".format(**settings)

p=subprocess.Popen(command.split(),cwd=settings['oer-exports-path'])

p.wait()



command = "{python-exe} {oer-exports-path}/collectiondbk2pdf.py -p {prince-path} -d {colllection-path} -s {print-style} {output-path}".format(**settings)

p=subprocess.Popen(command.split(),cwd=settings['oer-exports-path'])

p.wait()


# switch back to original hash

settings['git-hash']=start_git_hash

command = "git checkout {git-hash}".format(**settings)

p=subprocess.Popen(command.split(),cwd=settings['oer-exports-path'])

p.wait()
