# Summary

This is an automated tool for generating questions in MoodleXML format.

## How to execute?

Make sure that src path is in the `PYTHONPATH`. Execute the following from the root directory:

    export PYTHONPATH=$(pwd)/src:$PYTHONPATH

Install the requirements. Execute the following from the root directory:

    pip install --upgrade -r requirements.txt

To see how an example works, change the working directory to `test/` and execute:

    python3 ./run_all.py
