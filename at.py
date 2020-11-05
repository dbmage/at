''' Wrapper around subprocess to allow easy use of AT command '''
import os
import sys
import logging
import subprocess

log = logging.getLogger(__name__)

def runOsCmd(command,cmdin=None):
    if not isinstance(command, list):
        return False
    try:
        out = subprocess.Popen(command,
               stdin=subprocess.PIPE,
               stdout=subprocess.PIPE,
               stderr=subprocess.PIPE)
        if cmdin != None:
            out.stdin.write(cmdin.encode())
        output,errors = out.communicate()
        if errors:
            cmdout = ' '.join(command)
            if cmdin:
                cmdout += " %s" % (cmdin)
            log.error("Error occured running '%s': %s" % (cmdout, errors.decode('utf-8')))
            return False
        return output.decode('utf-8')
    except:
        return False

def getJobsList(queue='a'):
    # tab between jobid and day of week, 2 spaces between month and day of month if day is single digit
    output = runOsCmd(['atq', "-q%s" % (queue)]).replace('\t', ' ').replace('  ', ' ')
    jobs = {}
    jobqueue = output.split('\n')
    for job in jobqueue:
        if len(job) < 1:
            continue
        job = job.replace('\t', ' ')
        jobid, jobday, jobmonth, jobdate, jobtime, jobyear, jobqueue, jobuser = job.split(' ')
        jobs[jobid] = {
            'time' : jobtime,
            'day' : jobday,
            'date' : jobdate,
            'month' : jobmonth,
            'year' : jobyear,
            'queue' : jobqueue,
            'user' : jobuser
        }
        jobs[jobid]['command'] = runOsCmd([ 'at', '-c', jobid]).strip().splitlines()[-1]
    return jobs

def addJob(jobtime, queue, command):
    status = runOsCmd(['at', ':'.join(jobtime.split(':')[:2]), "-q%s" % (queue)], cmdin=command)
    if isinstance(status, bool):
        return False
    return status.split('\n')[1].split(' ')[1]

def addJobFromFile(jobtime, queue, file):
    filecontents = open(file).read()
    status = runOsCmd(['at', ':'.join(jobtime.split(':')[:2]), "-q%s" % (queue)], cmdin=filecontents)
    if isinstance(status, bool):
        return False
    return status.split('\n')[1].split(' ')[1]

def removeJob(jobid):
    if isinstance(jobid, int):
        jobid = "%i" % (jobid)
    status = runOsCmd(['atrm', jobid])
    if isinstance(status, bool):
        return False
    return True

def clearJobs(queue):
    jobs = getJobsList(queue)
    for job in jobs:
        removeJob(job)
