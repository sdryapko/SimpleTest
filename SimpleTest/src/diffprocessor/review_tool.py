#!/usr/bin/env python
import os
import sys
import shutil

git_ignore_fname = '.gitignore'
git_dname = '.git'
upload_tool_fname = 'upload.py'
my_fname = os.path.basename(__file__)
config_fname = 'rt.config'
issue_hack_fname = 'issue.txt'
sys_files = {git_ignore_fname, git_dname, upload_tool_fname, my_fname, config_fname, issue_hack_fname}
reviewer = 'ys.minsk.kolesov@gmail.com'

def write_config(source_name, revision, issue):
    f = open(config_fname, 'w')
    f.write(source_name + '\n')
    f.write(revision + '\n')
    f.write(issue + '\n')
    f.close()

def read_config():
    f = open(config_fname)
    source_name = f.readline().strip()
    revision = f.readline().strip()
    issue = f.readline().strip()
    return (source_name, revision, issue)

def get_revisions(source_name):
    from subprocess import Popen, PIPE
    output = Popen(["git", "log", source_name], stdout=PIPE).communicate()[0]

    result = []
    for line in output.split('\n'):
        if line.startswith('commit'):
            tokens = line.split()
            if len(tokens) != 2:
                continue

            result.append(tokens[1])
    return result

def resend_review():
    (source_name, revision, issue) = read_config()

    os.system('git add %s' % source_name)
    os.system('git commit -m "another try"')

    revs = get_revisions(source_name)
    os.system('python upload.py -i %s --rev=%s:%s' % (issue, revision, revs[0]))

    print 'I hope, issue with id %s was updated. Go to http://codereview.appspot.com/%s, check everything and click Publish+Mail comments' % (issue, issue)
    write_config(source_name, revs[0], issue)

def check_pre_create_state():
    if not os.path.exists(upload_tool_fname):
        print "Error: file %s doesn't exist" % upload_tool_fname
        exit(1)

def get_source_file():
    files = set(os.listdir(os.getcwd()))
    left_files = files - sys_files

    if len(left_files) == 0:
        print 'Error: no source file found. It must have name not in %s' % sys_files
        exit(1)
    if len(left_files) != 1:
        print 'Error: there are too many candidates for being source file. Must be unique. Have %s' % left_files
        exit(1)

    return list(left_files)[0]

def empty_file(fname):
    open(fname, 'w').write('\n')

def write_config(source_name, revision, issue):
    f = open(config_fname, 'w')
    f.write(source_name + '\n')
    f.write(revision + '\n')
    f.write(issue + '\n')
    f.close()

def get_revisions(source_name):
    from subprocess import Popen, PIPE
    output = Popen(["git", "log", source_name], stdout=PIPE).communicate()[0]

    result = []
    for line in output.split('\n'):
        if line.startswith('commit'):
            tokens = line.split()
            if len(tokens) != 2:
                continue

            result.append(tokens[1])
    return result


def create_review():
    check_pre_create_state()

    source_name = get_source_file()
    print 'Info: detected source file: %s' % source_name

    backup_name = source_name + '.bak'
    shutil.move(source_name, backup_name)
    empty_file(source_name)

    os.system('git init')
    os.system('git add %s' % source_name)
    os.system('git commit -m "init"')

    shutil.move(backup_name, source_name)
    os.system('git commit -a -m "written code"')

    revs = get_revisions(source_name)
    os.system('python upload.py --reviewers %s --private --rev=%s:%s' % (reviewer, revs[1], revs[0]))

    if not os.path.exists(issue_hack_fname):
        print 'Issue hack is not found. You aborted issue or maybe you use original upload.py. Use kolesov93 version in order to use this tool'
        exit(1)

    issue = open(issue_hack_fname).readline().strip()
    os.remove(issue_hack_fname)

    write_config(source_name, revs[0], issue)
    print 'Issue with id %s was created. Go to http://codereview.appspot.com/%s, fill name of issue and click Publish+Mail comments' % (issue, issue)

def main():
    if os.path.exists(config_fname):
        resend_review()
    else:
        create_review()

if __name__ == '__main__':
    main()

