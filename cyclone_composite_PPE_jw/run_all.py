import subprocess
#wd='/glade/scratch/dtmccoy/'
wd=''
for i in range(0,1):#263): ## writes a .sh file specifying the submission
    lines = ['#!/bin/bash',
    '#PBS -A WYOM0176',
    '#PBS -l walltime=02:00:00',
    '#PBS -q casper',
    '#PBS -l select=1:ncpus=4','python composite_PPE_member_mfd.py '+str(i)] ## specifies the file I want to run with
    ##input specified by 'i' (in this case the ensemble member)
    with open(wd+'ppe_sub'+str(i)+'.sh', 'w') as f:
        f.write('\n'.join(lines))
    subprocess.call('qsub ' + wd+'ppe_sub'+str(i)+'.sh',shell=True) ## submit the written file to queue
