from flask import render_template
import config
import dbexecutor
import routes.stockoperations
import routes.useroperations
from preload import testdata

app = config.app


@app.teardown_appcontext
def shutdown_session(exception=None):
    dbexecutor.session.remove()


@app.route('/')
def hello():
    if dbexecutor.firstTime():
        routes.useroperations.registeradmin()
        test = testdata.TestData()
        test.preLoadData()
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
    # app.run(debug=True)
    app.run()