# Run Extremefill2D Simulation in a Docker Instance

## Install Docker

Install Docker and run the Deamon. See
https://docs.docker.com/engine/installation/linux/ubuntulinux/ for
installation details.

    $ sudo service docker start

## Pull the Docker instance

Pull the Docker Instance from Dockerhub

    $ docker pull docker.io/wd15/extremefill2d

## Run the Test Simulation

Run the test simulation.

    $ git clone https://github.com/wd15/extremefill2D-dockerize
    $ cd extremefill2D-dockerize
    $ docker run -i -t -v ${PWD}:/home/main/work wd15/extremefill2d:latest
    # bash setup.sh

## Run Another Simulation

The subdirecties store the parameter files for other simulations. For
example,

    $ docker run -i -t -v ${PWD}:/home/main/work wd15/extremefill2d:latest
    # bash fig4/setup.sh
    # bash fig4/run.sh

## View the Results of the Test Simulation

    $ docker run -i -t -p 8888:8888 -v ${PWD}:/home/main/work wd15/extremefill2d:latest
    # jupyter notebook --ip 0.0.0.0 --no-browser

Open the link to `view.ipynb` in the browser display. Run all the
cells. View the results at http://127.0.0.1:8888.

## View the records with smtweb

    $ docker run -i -t -p 8000:8000 -v ${PWD}:/home/main/work wd15/extremefill2d:latest
    $ smtweb -p 8000 -a -n

View the results at http://127.0.0.1:8000

## Build the Docker instance

Clone this repository and build the instance.

    $ git clone https://github.com/wd15/extremefill2D-dockerize
    $ cd extremefill2D-dockerize
    $ docker build -t wd15/extremefill2d:latest .

## Push the Docker instance

Create the repository in Dockerhub and then push it.

    $ docker login
    $ docker push docker.io/wd15/extremefill2d
