import tokenhandler
with open(f'index.mto', 'r') as f:
    text = f.read()
    result, error = tokenhandler.run(text)

    if error: print(error.as_string())
    else: print(result)