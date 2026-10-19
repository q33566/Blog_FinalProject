from personalBlog import create_app

app = create_app()

if __name__ == '__main__':
    app.run(port=6002, debug=True)
