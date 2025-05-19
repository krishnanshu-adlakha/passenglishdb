from website import create_app

app = create_app()

if __name__ == "__main__":
    #Use on home network
    #app.run(host="192.168.0.49",debug=True)

    #localhost
    app.run(debug=True)