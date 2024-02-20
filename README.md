# my_q2_picrust2_script

## Help
```
usage: my-picrust2.py [-h] [-t TABLE] [-r REPSEQ] [-o OUTPUT] [-p THREADS]

Run picrust2

optional arguments:
  -h, --help            show this help message and exit
  -t TABLE, --table TABLE
                        Path to the feature table
  -r REPSEQ, --repseq REPSEQ
                        Path to the representative sequences
  -o OUTPUT, --output OUTPUT
                        Path to the output directory
  -p THREADS, --threads THREADS
                        Number of threads to use
```

## Example:
```shell
./my-picrust2.py -t table.qza -r rep-seqs.qza -p 6
```
