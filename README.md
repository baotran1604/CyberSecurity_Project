# Study Notes

Study Notes is a small Django app for keeping track of what you read. Give a note a title, write down what you want to remember, and find it later by searching your notebook. Each account has its own notes and sign-in history. SQLite keeps them on your computer when you stop the server.

This course project has five backend security examples. You can try each one with the code as it is, uncomment its fix, and repeat the same steps. The screenshots below show what happened with fictional accounts.

## Run the app

Install [Python 3.13](https://www.python.org/downloads/) and open a terminal in the folder that contains `manage.py`. On Debian or Ubuntu, if creating the virtual environment gives you an `ensurepip` error, install the matching Python venv package first.

**Windows (PowerShell)**

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe init_local.py
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

**Linux or macOS**

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python init_local.py
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Open [Study Notes on your computer](http://127.0.0.1:8000/), choose **Create an account**, then sign in and save a note. The setup script creates a local key the first time you run it. Later runs keep that key. To stop the server, press Ctrl+C. To start it again, repeat the last command for your system.

## Try the five examples

Each fix has a numbered comment beside it. After you uncomment a fix, restart the server so you know you're running the new code. You can try these in any order.

### 1. The staff package list leaves things out

Suppose a security notice mentions `sqlparse`. A staff member looking at this app's package list would see only Django, even though Django also installs `sqlparse` and `asgiref`. That makes the list unreliable when someone needs to check which versions are installed. OWASP includes missing information about indirect dependencies under **A06, Vulnerable and Outdated Components**. The issue here is the incomplete list. [OWASP A06](https://top10.owasp.org/2021/A06_2021-Vulnerable_and_Outdated_Components/)

1. Create a staff account. On Windows run `.\.venv\Scripts\python.exe manage.py createsuperuser`. On Linux or macOS run `.venv/bin/python manage.py createsuperuser`. Pick your own username and password.
2. Sign in with that account and open **Account → Python package inventory**. Compare the one-row list with the output of `.venv/bin/python -m pip list` (Windows: `.\.venv\Scripts\python.exe -m pip list`).
3. Under **Fix 1**, uncomment the line that reads all the installed distributions. Refresh the page after restarting. The extra packages now have their own rows and version numbers. Your exact package count can differ.

[Inventory code](notes/reports.py) · [Before](screenshots/flaw-1-before-1.png) · [After](screenshots/flaw-1-after-1.png)

### 2. A restart breaks a saved note’s receipt

When you save a note, Django stores a short verification value alongside it. This value, an HMAC, depends on the note's ID, owner, title, text, and a secret key. The app checks it again when you open the note. The problem is that the original settings pick a fresh key every time the server starts. This is a key-management issue under **A02, Cryptographic Failures**. [OWASP A02](https://top10.owasp.org/2021/A02_2021-Cryptographic_Failures/)

Save a new note and look at **Save receipt**. It says the note matches. Restart the server and refresh the same page. You can still read every word, but the receipt check fails.

Uncomment **Fix 2** in the settings, restart, and save a **new note**. Restart once more and open that new note. Its receipt now checks out because the app uses the saved local secret. The old receipt still needs the key that was lost.

[Key settings](config/settings.py) · [Receipt code](notes/models.py) · [At first save](screenshots/flaw-2-before-1.png) · [After restarting with the original settings](screenshots/flaw-2-before-2.png) · [After the fix and a restart](screenshots/flaw-2-after-1.png)

### 3. One study guide ships without a checksum

Open **Guides**. You can read *Reading Plan*, but *Weekly Review* won't open. Both text files are present. What's missing is the approved SHA-256 checksum for *Weekly Review*. Without it, the reader has nothing to compare that file against. This is the project's **A08, Software and Data Integrity Failures**, example. It assumes you trust the installed app and its list of approved checksums. [OWASP A08](https://top10.owasp.org/2021/A08_2021-Software_and_Data_Integrity_Failures/)

Uncomment the *Weekly Review* entry under **Fix 3**, restart, and open **Guides** again. You should now see the guide's text. The expected checksum is recorded separately from the file, so a later change to the text will cause a mismatch.

[Guide reader and checksums](notes/reports.py) · [Guide files](notes/guides/) · [Before](screenshots/flaw-3-before-1.png) · [After](screenshots/flaw-3-after-1.png)

### 4. A long passphrase gets turned away

Try creating an account with an unused username and a passphrase between 64 and 128 characters. Even when both password fields match, the form rejects it. The backend has a 48-character limit. Someone using a password manager or a long phrase has to choose something shorter. OWASP's **A07, Identification and Authentication Failures**, guidance covers password length, and NIST recommends supporting a maximum of at least 64 characters. [OWASP A07](https://top10.owasp.org/2021/A07_2021-Identification_and_Authentication_Failures/) · [NIST password guidance](https://pages.nist.gov/800-63-4/sp800-63b.html#passwordver)

Uncomment the 128-character limit under **Fix 4** and restart. Register with the same username and passphrase, then use them to sign in. **Account** shows the username you just registered. Django's other password checks still run.

[Registration form](notes/forms.py) · [Registration error](screenshots/flaw-4-before-1.png) · [Signed in after the fix](screenshots/flaw-4-after-1.png)

### 5. The history misses a sign-out

With a fresh account, sign in, sign out, then sign in again. Open **Activity**. You'll see two sign-ins in a row. Django ended the first session, but someone reading the history has no way to tell when you signed out. That's the gap in this **A09, Security Logging and Monitoring Failures**, example. [OWASP A09](https://top10.owasp.org/2021/A09_2021-Security_Logging_and_Monitoring_Failures/)

Uncomment both lines under **Fix 5** and remove the `pass` below them. Restart and repeat the sign-out and sign-in. This time **Activity** shows the sign-out between the two sign-ins. Earlier missing events can't be filled in.

[Sign-out handler](notes/signals.py) · [Before](screenshots/flaw-5-before-1.png) · [After](screenshots/flaw-5-after-1.png)

## Run the tests

From the project folder, run `.\.venv\Scripts\python.exe manage.py test` on Windows or `.venv/bin/python manage.py test` on Linux or macOS. The eight tests use a temporary database, so your own notebook stays separate. [Test cases](notes/tests.py)
