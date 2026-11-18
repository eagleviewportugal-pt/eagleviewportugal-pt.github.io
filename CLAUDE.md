
## Línguas (es.html / en.html)
`index.html` é a fonte única. `es.html` e `en.html` são gerados a partir dele com os textos do dicionário `T` já escritos no HTML (para o Google indexar cada língua).
Depois de qualquer alteração a `index.html`, correr sempre: `python3 tools/build_langs.py` e fazer commit dos três ficheiros.
