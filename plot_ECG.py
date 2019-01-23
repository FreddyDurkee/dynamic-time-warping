import wfdb

record = wfdb.rdrecord('16265', pb_dir='nsrdb/')
wfdb.plot_wfdb(record=record, title='Record 16265 from Physionet NSRDB')