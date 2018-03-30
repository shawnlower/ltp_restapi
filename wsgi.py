from ltp.app import create_app
from ltp.settings import Config


config = Config()
app = create_app(__name__, config) 

@app.errorhandler(404)
def do_break(error):
    import pdb; pdb.set_trace()

if __name__ == '__main__':
    app.run()


