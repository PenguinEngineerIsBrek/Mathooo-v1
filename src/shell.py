import tokenhandler

while True:
    text = input("MATH > ")
    result, error = tokenhandler.run(text)

    if error: print(error.as_string())
    else: print(result)