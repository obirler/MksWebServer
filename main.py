from flask import render_template, send_from_directory
import config
import dbexecutor
import os
import routes.stockoperations
import routes.useroperations
from preload import preloader
from flask_login import current_user

app = config.app


@app.teardown_appcontext
def shutdown_session(exception=None):
    dbexecutor.session.remove()


@app.route('/')
def hello():
    if dbexecutor.firstTime():
        routes.useroperations.registeradmin()
        preload = preloader.Preloader()
        preload.preLoad()
    return render_template('welcome.html')


@app.route('/test')
def test():
    stocks = dbexecutor.getDepotAllStocks()
    return render_template('test.html', stocks=stocks)


@app.context_processor
def inject_debug():
    return dict(debug=app.debug)


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)
    # app.run()
