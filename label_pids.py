import pandas as pd

df = pd.read_feather('data/logs.ft')
fields = ['UtcTime', 'ProcessId', 'EventID', 'User', 'Image', 'ImageLoaded', 'CommandLine',
            'ParentImage', 'ParentCommandLine', 'DestinationPort', 'Protocol', 'QueryName', 'TargetFilename', 'TargetObject', 'raw']
newdf = df[fields]

# drop all records where ProcessId in NaN (happens for WMI events, cannot classify [TODO: think how to overcome and add to dataset])
newdf = newdf[~newdf.ProcessId.isna()]

# drop EventID 5 - ProcessTerminated as not valuable
newdf.drop(newdf[newdf.EventID == '5'].index, inplace=True)

for name, df in newdf.groupby('ProcessId'):
    pp = ["\n|||   PID: ", name,'\n', df.Image.unique()[0]]
    print(''.join(pp))
    print('\n'.join([x for x in df.CommandLine.unique() if x is not None]))
    print('\n'.join([x for x in df.ParentCommandLine.unique() if x is not None]))
    print()
    a = input()
    if 'm' in a:
        with open('pid_malicious.lst','a') as f:
            f.write(name+'\n')
    else:
        with open('pid_valid.lst','a') as f:
            f.write(name+'\n')