import web

paths = (
    '/hello/(.*)', 'hello',
    '/justonews', 'ws',
)
app = web.application(paths, globals())

class hello:
    def GET(self, name):
        if not name:
            name = 'world'
        return 'Hello, ' + name + '!'

class ws:
    def GET(self):
        return 'Darkside'

if __name__ == "__main__":
    app.run()
