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

## Run the Simulations

Run the test simulation.

    $ mkdir /data/docker
    $ docker run -i -t -v /data/docker:/home/main/data wd15/extremefill2d:latest

This will set up `.smt` and `.git` directories in `/data/docker` and
run a small test simulation with the results in `/data/docker/Data`.

To run subsequent simulations use.

    $ docker run -i -t -v /data/docker:/home/main/data wd15/extremefill2d:latest /bin/bash
    $ smt run -t my_sim params_fig4.json totalSteps=10

for instance. To initalize the data directory again use

    $ docker run -i -t -v /data/docker:/home/main/data wd15/extremefill2d:latest /bin/bash
    $ \rm -rf .git .smt *
    $ bash $HOME/run.sh /home/main/data

## View the Results of the Test Simulation

    $ docker run -i -t -p 8888:8888 -v /data/docker:/home/main/data wd15/extremefill2d:latest /bin/bash
    $ jupyter notebook --ip 0.0.0.0 --no-browser

Open the link to the browser display in the ouput. Run all the cells

## Build the Docker instance

Clone this repository and build the instance.

    $ git clone https://github.com/wd15/extremefill2D-dockerize
    $ cd extremefill2D-dockerize
    $ docker build -t wd15/extremefill2d:latest .

## Push the Docker instance

Create the repository in Dockerhub and then push it.

    $ docker login
    $ docker push docker.io/wd15/extremefill2d

## See the Travis CI test of this instance

Not working yet.
