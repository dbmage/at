# at
Module for creating and managing AT jobs and queues
https://linux.die.net/man/1/at

# Installation
Clone the repo https://github.com/dbmage/at.git to your "git" area on your machine.
Add the location to your PYTHONPATH environment variable, or (for more advanced users) add to your python library location.

## Usage
```python
import at
atd = at.at()
atd.getJobsList('a') # return any jobs in the 'a' queue
atd.addJob('10:00', 'b', 'echo "Hello world" >> /tmp/myjob.log') # Add job to echo Hello world to a file at 10 am today to queue 'b'
atd.addJobFromFile('23:00', 'c', '/home/user/mycommandfile') # Add job from file /home/user/mycommandfile at 11 pm today to queue 'c'
atd.clearJobs('d') # clear all jobs from queue 'd'
atd.removeJob(2) # clear job number 2. Job numbers (id) are unique. The numbers increment irrelevant of queue
```
### sudo
If the user running the script can use at with sudo, you can tell the module to use sudo.
The sudo flag of the object defaults to False, change it to True to enable using sudo.
If a password is required to run at with sudo, the user will prompted if possible. This will cause headless or cronned scripts to fail.
```import at
atd = at.at()
atd.sudo = True
```


### getJobsList(queue)
#### queue
A single letter, lower and upper are separate queues, see the man page for more explanation.
#### returns
A dictionary containing all jobs from that queue


### addJob(jobtime, queue, command)
#### jobtime
A human datetime or just time (to run the job today).
I.E
Run at 10AM today

```10:00```

Run at 1pm on 20th Dec 2021

```13:00 12/20/2021```
#### queue
A single letter, lower and upper are separate queues, see the man page for more explanation.
#### command
A command that the user adding the job can run.
I.E
/path/to/my/script myinput
#### returns
The output from AT (stating job added for time date) if successful.
False if adding job failed.


### addJobFromFile(jobtime, queue, file)
#### jobtime
A human datetime or just time (to run the job today).
I.E
Run at 10AM today

```10:00```

Run at 1pm on 20th Dec 2021

```13:00 12/20/2021```
#### queue
A single letter, lower and upper are separate queues, see the man page for more explanation.
#### file
A file containing a command/script that can be run.
#### returns
The output from AT (stating job added for time date) if successful.
False if adding job failed.


### removeJob(jobid)
#### jobid
A unique job number, shown when 
#### returns
True is job was successfully removed
False if removal failed


### clearJobs(queue)
#### queue
A single letter, lower and upper are separate queues, see the man page for more explanation.
### returns
Nothing


### runOsCmd(command, cmdin)
#### command
The AT command with params.
I.E

```at -qa 10:00```
#### cmdin
The command AT should at the specified time, can be the contents of file.
Not required for requesting queues or removing jobs.


