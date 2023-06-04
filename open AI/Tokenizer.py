import tiktoken
encoding = tiktoken.get_encoding("p50k_base")
print(encoding.encode('Hello World!'))