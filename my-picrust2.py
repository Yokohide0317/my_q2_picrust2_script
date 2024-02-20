#!/usr/bin/env python
import logging

from pathlib import Path
import subprocess
import argparse



class MY_PICRUST2:

    def __init__(self, _args, logger = None) -> None:

        self.logger = logger
        self.table_path = Path(_args.table) #Path("../qiime2_output/merged-table-dada2.qza")
        self.repseq_path = Path(_args.repseq)#Path("../qiime2_output/merged-rep-seqs.qza")
        self.output_path = Path(_args.output) #Path("./my-picrust2-output")
        self.num_threads = int(_args.threads) #1
        self.tmp_dir = Path("./my-picrust2-tmp")


        self.fasta_file = self.tmp_dir / "dna-sequences.fasta"
        self.biom_file = self.tmp_dir / "feature-table.biom"

        # Prep
        self.prep_before_run()
        return

    def prep_before_run(self):
        if self.logger:
            self.logger.info(f"Checking files existance..")

        self.check_exit(self.table_path)
        print(f"TABLE.qza... OK: {self.table_path}")
        self.check_exit(self.repseq_path)
        print(f"REPSEQ.qza... OK: {self.repseq_path}")

#        if not self.output_path.exists():
#            self.output_path.mkdir()
#            print(f"Creating output directory: {self.output_path}")
#        else:
#            print(f"Output directory exists: {self.output_path}")

        if not self.tmp_dir.exists():
            self.tmp_dir.mkdir()
            print(f"Creating temp directory: {self.tmp_dir}")
        else:
            print(f"Temp directory exists: {self.tmp_dir}")

        print("Ready to Go")
        return

    def check_exit(self, _path: Path):
        if not _path.exists():
            raise FileNotFoundError(f"{_path} does not exist")
        return True

    def call_cmd(self, cmd: str):
        if self.logger:
            self.logger.info(f">: {cmd}")
        subprocess.run(cmd, shell=True)


    def prep_from_q2(self):
        # ready the input files
        cmd = f"qiime tools export --input-path {str(self.table_path)} --output-path {str(self.tmp_dir)}"
        self.call_cmd(cmd)

        cmd = f"qiime tools export --input-path {str(self.repseq_path)} --output-path {str(self.tmp_dir)}"
        self.call_cmd(cmd)

    def exec_picrust2(self):
        cmd = f"picrust2_pipeline.py -s {str(self.fasta_file)} -i {str(self.biom_file)} -o {str(self.output_path)} -p {str(self.num_threads)}"
        self.call_cmd(cmd)

if __name__ == "__main__":
    logger = logging.getLogger("my-picrust2")
    logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description="Run picrust2")
    parser.add_argument("-t", "--table", type=Path, help="Path to the feature table")
    parser.add_argument("-r", "--repseq", type=Path, help="Path to the representative sequences")
    parser.add_argument("-o", "--output", type=Path, help="Path to the output directory", default="./my-picrust2-output")
    parser.add_argument("-p", "--threads", type=int, help="Number of threads to use", default=1)

    args = parser.parse_args()
    my_pi = MY_PICRUST2(args)
    my_pi.prep_from_q2()
    my_pi.exec_picrust2()
