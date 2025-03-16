from controllers import create_app

app = create_app()

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=3030, debug=True)
    from waitress import serve
    serve(app, host="0.0.0.0", port=3030)
    # ssl_context=("certs/cert.pem", "certs/key.pem")
    # url_scheme="https", ssl_context=("certs/cert.pem", "certs/key.pem")
