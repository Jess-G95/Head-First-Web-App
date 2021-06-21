from flask import Flask, render_template, request, escape, session, copy_current_request_context, url_for, redirect, flash
#from flask_user import login_required
import vsearch
from DBcm import UseDatabase, ConnectionError
from checker import check_logged_in
from threading import Thread
from time import sleep

app = Flask(__name__)

app.config['dbconfig'] = { 'host': '127.0.0.1',
                 'user': 'vsearch',
                 'password': 'vsearchpasswd',
                 'database': 'vsearchlogdb', }

@app.route('/login', methods=['GET', 'POST'])
def do_login() -> str: # correct annotation? + add check to see if already logged in
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """SELECT * FROM users WHERE username=%s  AND password=%s"""
            cursor.execute(_SQL, (request.form['username'],
                                  request.form['password'], ))
            account = cursor.fetchone()
        if account:
            session['logged_in'] = True
            session['username'] = request.form['username']
            #flash('Logged in successfully!')
            return redirect(url_for('entry_page'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

@app.route('/logout')
def do_logout() -> str: # correct annotation?
    session.pop('logged_in')
    #return 'You are now logged out.'
    return redirect(url_for('entry_page'))

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """SELECT * FROM users WHERE username=%s"""
            cursor.execute(_SQL, (request.form['username'], ))
            account_exists = cursor.fetchone()
            if account_exists:
                flash('Username already exists')
            elif request.form['username'] or request.form['username'] == '':
                flash('Please enter a username and password.')
            else:
                _SQL = """ insert into users
                        (username, password)
                        values
                        (%s, %s)"""
                cursor.execute(_SQL, (request.form['username'],
                                        request.form['password'],))
                return redirect(url_for('do_login'))
    return render_template('signup.html') 

@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    
    @copy_current_request_context
    def log_request(req: 'flask_request', res: str) -> None:
        sleep(15) # sleep to test delay exception
        with UseDatabase(app.config['dbconfig']) as cursor: # add try/except to all UseDatabase
            _SQL = """ insert into log
                    (phrase, letters, ip, browser_string, results)
                    values
                    (%s, %s, %s, %s, %s)"""
            cursor.execute(_SQL, (req.form['phrase'],
                                  req.form['letters'],
                                  req.remote_addr,
                                  req.user_agent.browser,
                                  res, ))
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results: '
    results = str(vsearch.search_for_letters(phrase, letters))
    try:
        t = Thread(target=log_request, args=(request, results))
        t.start()
    except Exception as err:
        print('****Logging failed with this error: ', str(err))
    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_title=title,
                           the_results=results,)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search4letters on the web!')

@app.route('/viewlog')
#@login_required
@check_logged_in
def view_the_log() -> 'html':
    """Display the contents of the log file as an HTML table"""
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """select phrase, letters, ip, browser_string, results from log"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
        titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
        return render_template('viewlog.html',
                               the_title='View Log',
                               the_row_titles=titles,
                               the_data=contents,)
    except ConnectionError as err:
        print('Is your database switched on? Error: ', str(err))
    except CredentialsError as err:
        print('User-id/Password issues. Error: ', str(err))
    except SQLError as err:
        print('Is your query correct? Error: ', str(err))
    except Exception as err:
        print('Something went wrong: ', str(err))
    return 'Error'

app.secret_key = 'Youwillneverguessmysecretkey'

if __name__ == '__main__':
    app.run(debug=True)
