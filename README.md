# HealthHelper
Code for the HealthHelper project for HackGSU 2022.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/abigailnacional/HealthHelper.git
   ```
2. Navigate to the folder
   ```sh
   cd HealthHelper
   ```
3. Run install.sh by dragging the file into your terminal.

4. Set the environment variable for your Google Cloud Credentials as the path to the json file with said credentials. You must use your own path to the required json. You must reenter this command every time you open a new terminal shell.
   ```sh
   export GOOGLE_APPLICATION_CREDENTIALS=C:\Users\yourUser\credentials-file.json
   ```
   Sometimes the credentials need to be saved this way instead:
   ```sh
   export GOOGLE_APPLICATION_CREDENTIALS="\Users\yourUser\credentials-file.json"
   ```

5. Run the following commands in your terminal.
   ```sh
   export FLASK_ENV=‘development’
   . env/bin/activate
   flask run
   ```

6. Type "localhost:5000" into your browser's URL bar and press enter.

# 401 Response for API Call
1. Run the following command (make sure you have gcloud set up):
   ```sh
   gcloud auth application-default print-access-token
   ```

2. Copy the access token that is returned and paste it in place of the current access token (the string of letters and numbers after BEARER) on line 67 of app.py.

3. Press ctrl-c to stop running Flask and then type
   ```sh
   flask run
   ```
   in order to rerun the app.

# Acknowledgements
Flask boilerplate is from [here](https://github.com/abigailnacional/flask-boilerplate.git).
