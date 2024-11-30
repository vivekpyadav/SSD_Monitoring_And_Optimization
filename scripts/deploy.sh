#!/bin/bash

echo "|[ Deploy script ]|"


echo """Choose Where to Deploy:
        
        - Remotly (1)
        - Locally (2)"""

read option

if [ "$option" == "1" ]; then
    
# Define the remote server (if deploying remotely)
    echo Enter the your server IP
    read REMOTE_SERVER
    echo Enter your username
    read REMOTE_USER
    echo Enter the path to deploy
    read REMOTE_PATH


    echo "Setting up environment..."

    # Clone the repository.
    # git clone https://your_repository_url.git
    
    echo "Deploying project to remote server..."
    scp -r ./ $REMOTE_USER@$REMOTE_SERVER:$REMOTE_PATH
    ssh $REMOTE_USER@$REMOTE_SERVER "cd $REMOTE_PATH && pip install -r requirements.txt"
elif [ "$option" == "2" ]; then

    # Install Python dependencies
    echo "Installing Python dependencies..."
    pip install -r requirements.txt

    echo "Deploying locally..."
    # Add any local-specific deployment steps here
    echo "Local deployment complete."

else
    echo invalid input
fi

# Set up logging directory
mkdir -p logs

echo "----X-----X-----"

