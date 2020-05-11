# Tempo

<img alt="Tempo icon" align="right" height="256" src="https://kotano.github.io/Tempo/docs/sources/logo.png"/>

Tempo is a task-management application that tracks your tasks / goals and evenly distributes work on them. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
See deployment for notes on how to deploy the project on a live system.


### Prerequisites

To start working on project you first need to download [__kivy__](https://github.com/kivy/kivy) framework.

The simpliest way to do this is to use Anaconda.
> ### On windows
>Install Kivy using Anaconda:  
>Using your Anaconda virtual environment type following command into the console.  
>```
>conda install kivy -c conda-forge
>```
>
If you are using different platform, please refer to [kivy download page](https://kivy.org/#download).


### Installing

A step by step series of examples that tell you how to get a development env running.

The installation of Tempo is pretty simple, and it doesn`t require any additional skills. But in case if you have difficulties running the application, here are the instructions.

Step 1: Clone Tempo repository from GitHub

```
git clone https://github.com/kotano/Tempo.git
```

Step 2: Running the app

Make sure you have installed kivy before launch.

```
python .../Tempo/main.py
```
After executing this command, you will see the main application window.
<img alt="Main application window" align="" height="300" src="./docs/sources/main_window.png"/>

## Running the tests

For this project we use PyTest to automatically test our systems.

### Running tests

```
make test
``` 
or  
```
projectdir$ pytest
``` 

### And coding style tests

We use flake8 for code linting

```
make lint
```
or
```
projectdir$ flake8
```

## Built With

* [kivy](https://kivy.org) - GUI framework


## Team

* **Arslan Hudaygulyyev** - *Main developer* - [kotano](https://github.com/kotano)
* **Elizabeth Aleksandrova** - *Tester* - [eliz0106](https://github.com/eliz0106)
* **David Naumov** - *Project Manager*
* **Anastasiya Yesareva** - *Analitics*

## Website

<https://kotano.github.io/Tempo>