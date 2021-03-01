from service import create_app, config

app = create_app(config.DevelopmentConfig)
if __name__ == '__main__':
    app.run(port=9001)
