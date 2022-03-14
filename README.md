# edx-dl

## 0. Motivation

Continue on previous old [repo](github.com/antinucleon/edx-dl) by [antinucleon](https://github.com/antinucleon)

Unlink `https://github.com/coursera-dl/edx-dl`, this codebase is <300 lines. Less time to tinker. 

Also, can visually cheat. So, it's more adaptive to future changes (russia ban).

Imagine you right click the element to copy xpath. Rather than, stratch ur head to debug into a maze, which might fail anywhere anytime...(of course)

## Result
----------

spent a few hours to get it working

1. download course BEM1105x
    video
    slides
    quzz snapshot is not perfect (cutoff)

2. seperate folder as Unit

3. full automation

## OS

Linux, Ubuntu (see below)
Python virtual env (optional)

## 1. Usage

- Edit homebrew locatoin on Linux 
    If you are on Mac or aria2c is already in PATH, change accordingly.
    default `/home/linuxbrew/.linuxbrew/bin/aria2c`) due to pycharm can't find PATH

- Download `chromedriver` and put it into `./bin`

- Install aria2

- Run `pip install -r requirements.txt`

- Rename `settings.sample.yaml` to `settings.yaml`

- Edit `settings.yaml` to have your credentials. Don't share your password.

- Run `python edx-dl.py`, input user name, password, and course url (eg: `https://learning.edx.org/course/course-v1:CaltechX+BEM1105x+3T2020/home`)

- Wait for a while for chrome to open up

## 2. Remark
- Headless mode may be buggy due to lacking wait for some loadings. However I am lazy to make it correct. 

## first author

kaggle master: https://bingxu.io/20200724/about.html

## docs selenium 

well, now we use latest api.
