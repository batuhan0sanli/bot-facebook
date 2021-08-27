# bot-facebook
## Purpose
This repo captures some data from Facebook.

## Dependencies
### Python
You need Python 3 run. You can have multiple Python versions (2.x and 3.x) installed on the same system without problems. In Ubuntu, Mint and Debian you can install Python 3 like this:
```
$ sudo apt-get install python3 python3-pip
```

### Python Modules
bot-facebook depends on a few python modules to do its job. You can automatically installed like this:
```
$ pip install -r requirements.txt
```

### Tesseract
Required for the OCR module.
```
$ apt-get install tesseract-ocr
```


## How to Build / Install and Run
### Clone Repository
To check out and use the latest source code
```
$ git clone https://github.com/batuhan0sanli/bot-facebook
```

### Virtual Environment Setup
To run independently
```
$ sudo apt-get install python3 python3-virtualenv
```
```
$ cd bot-facebook                    # change to your project's directory
$ virtualenv -p python3 env          # create the env folder with a new virtual environment for python3
$ source env/bin/activate            # adjust shell to use binaries inside env as default
$ pip install --upgrade pip          # upgrade the package management tool pip
$ pip install -r requirements.txt    # download and compile a package into local env
```

### Usage
#### Main
```
usage: python main.py [-h] --url URL --month MONTH

optional arguments:
  -h, --help     show this help message and exit
  --url URL
  --month MONTH  YYYYmm
```

#### OCR
```
usage: python OCR.py
```

#### Sum Module
```
usage: sumDOM.py [-h] --dir DIR

optional arguments:
  -h, --help  show this help message and exit
  --dir DIR   must be 'DOM' or 'OCR'
```
## Examples
#### Only one URL
```
$ python main.py --month 202108 --url https://www.facebook.com/EsenyurtBLDYS
```

#### URL List
```
$ python main.py --month 202108 --url urls.lst
```
