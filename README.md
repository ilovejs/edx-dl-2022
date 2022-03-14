# edx-dl

## 0. Motivation

I was using `https://github.com/coursera-dl/edx-dl` to backup some courses I want to learn but delayed due to 1000+ reasons. However seems this project is no longer maintained. So I spend a few hours to write a small tool.

This script is usable but I don't have time to do more test, and I have no plan to maintain this project. However it is straightforward to update because it is just 200 lines of code.

### Result
----------

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

[antinucleon](https://github.com/antinucleon)

[repo](github.com/antinucleon/edx-dl)

kaggle master: https://bingxu.io/20200724/about.html

## docs selenium 

well, now we use latest api.
