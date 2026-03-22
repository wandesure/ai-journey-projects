with open('sample.txt','r',encoding='utf-8') as file:
    content = file.read()

print('File contents:')
print(content)
print(f'\nTotal characters:{len(content)}')