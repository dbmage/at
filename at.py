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
            log.error("Error occured running '%s': %s" % (command, errors))
            return False
        return output
    except:
        return False

def getJobsList(queue):
    # tab between jobid and day of week, 2 spaces between month and day of month if day is single digit
    output = runOsCmd(['atq', "-q%s" % (queue)]).decode('utf-8').replace('\t', ' ').replace('  ', ' ')
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
    return jobs

def addJob(jobtime, queue, command):
    status = runOsCmd(['at', ':'.join(jobtime.split(':')[:2]), "-q%s" % (queue)], cmdin=command)
    if isinstance(status, bool):
        return False
    return status.decode('utf-8').split('\n')[1].split(' ')[1]

def addJobFromFile(jobtime, queue, file):
    filecontents = open(file).read()
    status = runOsCmd(['at', ':'.join(jobtime.split(':')[:2]), "-q%s" % (queue)], cmdin=filecontents)
    if isinstance(status, bool):
        return False
    return status.decode('utf-8').split('\n')[1].split(' ')[1]

def removeJob(jobid):
    status = runOsCmd(['atrm', jobid])
    if isinstance(status, bool):
        return False
    return True

def clearJobs(queue):
    jobs = getJobsList(queue)
    for job in jobs:
        removeJob(job)
