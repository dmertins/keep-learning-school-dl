# keep-learning-school-dl
Keep Learning School courses downloader.

## Development
### TODO
- get course to be downloaded from command line args;
- download all courses by default;

### Known Bugs
- downloaded file output path is not working; all videos are being downloaded in project root directory;

## Requirements
- [Python 3.9+](https://www.python.org/downloads/)
- [geckodriver 0.28.0+](https://github.com/mozilla/geckodriver/releases)

## Environment Setup
To create and activate a python virtual environmnent on Linux:
```bash
$ python -m venv ./venv && source ./venv/bin/activate
```

To create and activate a python virtual environmnent on Windows:
```
\> python -m venv ./venv && venv\Scripts\activate
```

To install the project dependencies:
```bash
(venv) $ pip install -r requirements.txt
```

To deactivate the python virtual environmnent:
```bash
(venv) $ deactivate
```

## Running the project

To download the courses:

```bash
(venv) $ python main.py
```
