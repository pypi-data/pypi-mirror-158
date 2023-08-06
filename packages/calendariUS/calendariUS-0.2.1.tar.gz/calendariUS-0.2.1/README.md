# calendariUS

Generate calendar for Help Desk shifts


## Install

You can install the current release from [PyPI](https://pypi.org/)

```
pip install calendariUS
```

or you can also build `calendariUS` from source

```
git clone https://gitlab.hpc.cineca.it/sorland/calendarius.git

cd calendarius
python setup.py install
```

In any case, the creation of a virtual environment is recommended.


## Usage

To generate Help Desk shifts to stdout

```
calendarius -s YYYY-MMM-DD -e YYYY-MM-DD  list of names
```

To save result to a ics file

```
calendarius -s YYYY-MMM-DD -e YYYY-MM-DD  -i file.ics list of names
```


To print statistics on shifts

```
calendarius -s YYYY-MMM-DD -e YYYY-MM-DD  --stats  list of names
```


Example of usage:

```
calendarius -s 1970-01-01 -e 1970-01-31 -i guide.ics Zaphod Ford Trillian Arthur Slartibartflast Marvin "Deep Thought" --stats
```


## Disclaimer

`calendariUS` developers take no responsibility for the disadvantageous distribution of shifts.

