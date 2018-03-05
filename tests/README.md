Testing
--------

Install prerequisites

    virtualenv .env -p python3 --clear && . .env/bin/activate
    pip install -r tests/requirements.txt


Run unit tests

    pytest


Run functional tests

     python message_lengths.py

Open client.html in the browser and refresh consequently until all test cases pass.
