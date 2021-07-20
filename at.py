''' Wrapper around subprocess to allow easy use of AT command '''
import os
import re
import sys
import logging
import subprocess
from datetime import datetime

log = logging.getLogger(__name__)

class at():
    def __init__(self):
        self.sudo = False

    def runOsCmd(self, command,cmdin=None):
        if not isinstance(command, list):
            return False
        jobidregex = re.compile(r'job ([0-9]+) at')
        if self.sudo:
            command.insert(0, 'sudo')
        try:
            out = subprocess.Popen(command,
                   stdin=subprocess.PIPE,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)
            if cmdin != None:
                out.stdin.write(cmdin.encode())
            output,errors = out.communicate()
            if output:
                return output.decode('utf-8')
            if output == errors:
                return True
            errors = errors.decode('utf-8')
            jobid = jobidregex.findall(errors)
            if len(jobid) < 1:
                cmdout = ' '.join(command)
                if cmdin:
                    cmdout += " %s" % (cmdin)
                log.error("Error occured running '%s': %s" % (cmdout, errors))
                return False
            return jobid[0]
        except Exception as e:
            log.error("Error occured: %s" % (e))
            return False

    def getJobsList(self, queue='a'):
        # tab between jobid and day of week, 2 spaces between month and day of month if day is single digit
        output = self.runOsCmd(['atq', "-q%s" % (queue)])
        if isinstance(output, bool):
            return []
        output = output.replace('\t', ' ').replace('  ', ' ')
        jobs = {}
        jobqueue = output.split('\n')
        for job in jobqueue:
            if len(job) < 1:
                continue
            job = job.replace('\t', ' ')
            jobid, jobday, jobmonth, jobdate, jobtime, jobyear, jobqueue, jobuser = job.split(' ')
            dts = "%s-%s-%s %s" % (jobyear, jobmonth, jobdate, jobtime)
            dt = datetime.strptime(dts, '%Y-%b-%d %H:%M:%S')
            jobs[jobid] = {
                'dt' : dt,
                'time' : jobtime,
                'day' : jobday,
                'date' : jobdate,
                'month' : dt.month,
                'year' : jobyear,
                'queue' : jobqueue,
                'user' : jobuser
            }
            jobs[jobid]['command'] = self.runOsCmd([ 'at', '-c', jobid]).strip().splitlines()[-1]
        return jobs

    def addJob(self, jobtime, queue, command):
        jobtime = jobtime.split(' ')
        jtime = ':'.join(jobtime[1].split(':')[:2])
        jdate = jobtime[0]
        if '-' in jdate:
            jdate = jdate.split('-')
        if '/' in jdate:
            jdate = jdate.split('/')
        if not isinstance(jdate, list):
            log.error("Garbled date - %s" % (jobtime[1]))
            return False
        jdate = "%s/%s/%s" % (jdate[1], jdate[0], jdate[2])
        status = self.runOsCmd(['at', "%s %s" % (jtime, jdate), "-q%s" % (queue)], cmdin=command)
        if status == False:
            return False
        return status

    def addJobFromFile(self, jobtime, queue, file):
        filecontents = open(file).read()
        jobtime = jobtime.split(' ')
        jtime = ':'.join(jobtime[1].split(':')[:2])
        jdate = jobtime[0]
        if '-' in jdate:
            jdate = jdate.split('-')
        if '/' in jdate:
            jdate = jdate.split('/')
        if not isinstance(jdate, list):
            log.error("Garbled date - %s" % (jobtime[1]))
            return False
        jdate = "%s/%s/%s" % (jdate[1], jdate[0], jdate[2])
        status = self.runOsCmd(['at', "%s %s" % (jtime, jdate), "-q%s" % (queue)], cmdin=filecontents)
        if status == False:
            return False
        return status

    def removeJob(self, jobid):
        if isinstance(jobid, int):
            jobid = "%i" % (jobid)
        status = self.runOsCmd(['atrm', jobid])
        if isinstance(status, bool):
            return False
        return True

    def clearJobs(self, queue):
        jobs = self.getJobsList(queue)
        for job in jobs:
            self.removeJob(job)
        return True
