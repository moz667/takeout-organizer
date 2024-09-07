# takeout-organizer

Another script to organize google photos takeout data.

What really do is simple: Take an extracted takeout google photos dir (`-i` argument) and move to a grouped dir estructure (`-o` argument) by year and month of the media (`year/month`).

## What is really doing this script

The script traverses the entire extracted takeout google photos dir (`-i` argument) searching for files (`sample-file.jpg`) and its json data (`sample-file.jpg.json`) and only with the info of the json data, archive this files on the archive directory (`-o` argument)

In addition to any errors that may occur, the process will find duplicates and files with no json data.

If the duplicate is exactly the same, the script will ignore this file leaving it in its folder, and otherwise it will move it to the special folder `duplicates-diferent-checksum` inside the archive directory.

If the file has no data, it will move it to the special folder `no-json-data` inside the archive directory.

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

* `--i=<takeout-directory>, --idir=<takeout-directory>`, input directory or the directory where the takeout files are.
* `--o=<archive-directory>, --odir=<archive-directory>`, output directory or the directory to archive grouped by year and month the takeout files.
* `--dry_run`, optional, test de execution. Not move files, only show what are going to do.

## Python arguments

By default, the script generates some verbose output, to reduce this, execute python with `-O` argument.

**From the `man python`:**

**-O** Remove  assert statements and any code conditional on the value of __debug__; augment the filename for compiled (bytecode) files by adding .opt-1 before the .pyc extension.

See also [`__debug__`](https://docs.python.org/3/library/constants.html#debug__)

## Logs

In addition of the execution output, there are 3 log files on temporary directory (`/tmp` for linux) with the preffix `takeout-organizer` for inventory purposes.

* `takeout-organizer_already-exists_<timestamp>.log`, for files that collide with current archived files
* `takeout-organizer_diferent-checksum_<timestamp>.log`, for files that collide with current archived files **and have a DIFERENT CHECKSUM**
* `takeout-organizer_<timestamp>.log`, for everything else

## Samples

```bash
# Simple execution
python takeout-organizer/src/takeout-organizer.py --i=samples/takeout --o=samples/archive
# Less output execution
python -O takeout-organizer/src/takeout-organizer.py --i=samples/takeout --o=samples/archive
# Execute test
python takeout-organizer/src/takeout-organizer.py --i=samples/takeout --o=samples/archive --dry_run
```