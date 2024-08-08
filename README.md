# takeout-organizer

Another script to organize google photos takeout data.

## Requeriments

```bash
pip3 install simple-file-checksum
```

## Instalation

```bash
# Install requeriments
pip3 install simple-file-checksum
# Download and install `takeout-organizer`
git clone https://github.com/moz667/takeout-organizer.git
# Try execution
python takeout-organizer/src/takeout-organizer.py
```

## Arguments

* `-i <takeout-directory>, --idir=<takeout-directory>`, input directory or the directory where the takeout files are.
* `-o <archive-directory>, --odir=<archive-directory>`, output directory or the directory to archive grouped by year and month the takeout files.
* `--dry_run`, optional, test de execution. Not move files, only show what are going to do.

## Python arguments

By default, the script generates some verbose output, to reduce this, execute python with `-O` argument.

**From the `man python`:**

**-O** Remove  assert statements and any code conditional on the value of __debug__; augment the filename for compiled (bytecode) files by adding .opt-1 before the .pyc extension.

See also [`__debug__`](https://docs.python.org/3/library/constants.html#debug__)

## Samples

```bash
# Simple execution
python takeout-organizer/src/takeout-organizer.py -i samples/takeout -o samples/archive
# Less output execution
python -O takeout-organizer/src/takeout-organizer.py -i samples/takeout -o samples/archive
# Execute test
python takeout-organizer/src/takeout-organizer.py -i samples/takeout -o samples/archive --dry_run
```