# Open Network Services Automation

#####################
# Local environment #
#####################

# Run on Local env
scripts/local/./run.sh

# Stop local env
scripts/local/./stop.sh


#####################
# Dev environment   #
#####################

# Build containers
docker-compose up --build

# Just start
docker-compose up --no-recreate

