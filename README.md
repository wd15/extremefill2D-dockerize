# Run Extremefill2D Simulation in a Docker Instance

This runs figure 4 from
[paper](https://dx.doi.org/10.1149/2.040312jes).

## Install Docker

Install Docker and run the Deamon. See
https://docs.docker.com/engine/installation/linux/ubuntulinux/ for
installation details.

    $ sudo service docker start

## Pull the Docker instance

Pull the Docker Instance from Dockerhub

    $ docker pull docker.io/wd15/extremefill2d

## Test FiPy

Test the build inside the instance.

    $ docker run -i -t wd15/extremefill2d:latest /bin/bash
    $ cd $HOME/extremefill2D/scripts
    $ smt run params_fig4.json totalSteps=20

## Build the Docker instance

Clone this repository and build the instance.

    $ git clone https://github.com/wd15/extremefill2D-dockerize
    $ cd extremefill2D-dockerize
    $ docker build -t wd15/extremefill2d:latest .

## Push the Docker instance

Create the repository in Dockerhub and then push it.

    $ docker login
    $ docker push docker.io/wd15/extremefill2d:latest

## See the Travis CI test of this instance

Not working yet.
