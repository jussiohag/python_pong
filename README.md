# python_pong

Copilot discussion: 

		https://github.com/copilot/share/c04140a2-01a0-8c93-a911-7609a4596978


## Install instructions
* Install Flask

        pip install flask
        
    or
        
        sudo apt install python3-flask
        
* Run the server


        python3 app.py

* Visit the url in your browser to play Pong!

        http://localhost:5000 


## Install instructions for Dockerized version

How to run:

* Build the image:
		
		docker build -t pong-game .

* Run the container:

		docker run -p 5000:5000 pong-game

* Open in your browser and play!

	http://localhost:5000


