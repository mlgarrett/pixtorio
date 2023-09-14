# Piχtorio
A pixel art blueprint generator for Factorio!

Try the live site at [pixtor.io](https://pixtor.io)!

Community contributions to this tool are welcomed and encouraged! The code isn't that complicated, and there is lots of room for improvement.

## Development Setup
To set up your system for development of this software, you will first need to install Python (recommended >=3.10) and you will also want to be able to set up Python virtual environments. These requirements are outside the scope of this guide.

Once you have Python and the ability to create a virtual environment, take the following steps:

1. Clone this repository to your computer:
```
git clone https://github.com/mlgarrett/pixtorio.git
```

2. Enter the repository directory:
```
cd pixtorio
```

3. Create a new virtual environment called `venv`:
```
python3 -m venv venv
```

4. Activate the virtual environment:
On Linux:
```
source venv/bin/activate
```
On Windows:
```
.\venv\Scripts\activate
```
5. Install the dependencies:
```
pip install -r requirements.txt
```

All done! You can run the app on a local Flask server by issuing the following command:
```
python3 driver.py
```
and the app can be accessed through your web browser at `127.0.0.1:5000`.