from hello import hello

def test_hello(x):
  return f"hello {x}" == hello(x)
