# Run Extremefill2D Simulation in a Docker Instance

## Install Docker

Install Docker and run the Deamon. See
https://docs.docker.com/engine/installation/linux/ubuntulinux/ for
installation details.

    $ sudo service docker start

## Run the Simulations

Run the test simulation.

    $ mkdir /data/docker
    $ docker run -i -t -v /data/docker:/home/main/data wd15/extremefill2d:fig4

This will set up `.smt` and `.git` directories in `/data/docker` and
run a small test simulation with the results in `/data/docker/Data`.

To run subsequent simulations use.

    $ docker run -i -t -v /data/docker:/home/main/data wd15/extremefill2d:latest /bin/bash
    $ smt run -t my_sim params.json totalSteps=10

for instance. To initalize the data directory again use

    $ docker run -i -t -v /data/docker:/home/main/data wd15/extremefill2d:fig4 /bin/bash
    $ \rm -rf .git .smt *
    $ bash $HOME/extremefill2D/scripts/setup.sh /home/main/data

and then run lots of simulations,

    $ bash run.sh

## View the Results of the Test Simulation

    $ docker run -i -t -p 8888:8888 -v /data/docker:/home/main/data wd15/extremefill2d:fig4 /bin/bash
    $ jupyter notebook --ip 0.0.0.0 --no-browser

Open the link to the browser display in the ouput. Run all the cells

## Build the Docker instance

Clone this repository and build the instance.

    $ git clone https://github.com/wd15/extremefill2D-dockerize
    $ cd extremefill2D-dockerize/fig4
    $ docker build --no-cache -t wd15/extremefill2d:fig4 .

Run with `--no-cache` so that the `run.sh`, `params.json` and
`view.ipynb` are always update.
