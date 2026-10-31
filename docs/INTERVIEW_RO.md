# Pregătire pentru interviu — Document Change Monitor

Roluri țintă: RAG Operations / Backend.

## Prezentare de 90 de secunde

1. Explică problema concretă și cine folosește rezultatul.
2. Rulează `make demo` sau fluxul din UI.
3. Arată testul pentru un caz de eșec, apoi explică mecanismul din cod.
4. Spune ce limite are demonstrația și ce ai construi pentru producție.

Decizia de explicat: A document update stores a new revision and replaces the current searchable text in one transaction. Search reads only active current versions; historical text stays in a separate revision table.

## Cinci întrebări

1. Cum eviți citarea unei versiuni vechi?
2. Ce face update-ul atomic?
3. Cum tratezi ștergerea?
4. De ce păstrezi hash și versiune?
5. Cum sincronizezi un vector index extern?

## Exercițiu înainte de a aplica

Add an asynchronous embedding index with version fences and content-source polling.

Alege o parte mică a acestei modificări, implementeaz-o personal, adaugă un test care verifică comportamentul și descrie rezultatul într-un commit real. Nu declara că ai înțeles sau construit singur o parte pe care nu o poți explica.

## Checklist personal

- [ ] Pot porni proiectul dintr-un checkout curat.
- [ ] Pot urmări cererea până la rezultatul salvat.
- [ ] Pot explica diferența dintre fixture și model local.
- [ ] Pot demonstra un eșec și recuperarea lui.
- [ ] Am făcut o modificare proprie și o pot explica în engleză.

Aceste puncte necesită review-ul tău; nu au fost bifate automat.
