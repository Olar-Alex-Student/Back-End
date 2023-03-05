# Back-End
## Back-End-ul echipei Bizonii în concursul Assist Tech Challenge.
 
Aplicatia a fost realizata folosind fastAPI, un framework rapid ce foloseste Python 3.7+

Aceasta dezvolta un API care foloseste o baza de date a unor utilizatori sunt logati pe
un site de completare automata a unor formulare.

### Comanda pe care o folosim pentru a mentine serverul pornit este:
```"uvicorn main:app --reload"```


## Aplicatia are 4 functii principale GET, POST, PUT, DELETE:
1. ### GET:
   - #### Această comandă HTTP este utilizată pentru a obține informații de la server. În general, cererea este însoțită de un URL și, uneori, de parametri suplimentari care pot fi utilizați pentru a filtra sau sorta datele returnate. Serverul răspunde cu informațiile solicitate, care sunt de obicei afișate într-un browser sau utilizate într-un alt fel de către client.
2. ### POST:
   - #### Această comandă HTTP este utilizată pentru a trimite date către server. De obicei, datele sunt trimise sub forma unui formular completat de utilizator sau prin intermediul unui script care generează automat date. De asemenea, această comandă HTTP poate fi utilizată pentru a crea resurse noi pe server sau pentru a actualiza resurse existente.
3. ### PUT:
   - #### Această comandă HTTP este utilizată pentru a actualiza datele unei resurse existente pe server. De obicei, se utilizează această comandă HTTP pentru a actualiza întreaga resursă, inclusiv datele care nu au fost modificate, în timp ce comanda PATCH este utilizată pentru a actualiza doar o parte din resursă.
4. ### DELETE:
   - #### Această comandă HTTP este utilizată pentru a șterge o resursă de pe server. Aceasta poate fi o imagine, un document, un articol de blog sau orice altceva care a fost creat sau depozitat pe server. Când este trimisă o comandă DELETE, resursa specificată este ștearsă definitiv și nu poate fi recuperată.


## USERS:
1. #### GET USER: https://bizoni-backend-apis.azurewebsites.net/users/{user_id}
   - [ ] Folosind un id-ul unui user returneaza datele despre acesta. Unele restrictii sunt ca numele trebuie sa aiba cel putin 3 litere si un individ nu poate sa introduca un cod fiscal.
2. #### POST USER: https://bizoni-backend-apis.azurewebsites.net/
   - [ ] Creaza un user nou folosind datele trimise, verifica daca email-ul si numele trimise nu se regasesc 
   in baza de date si returneaza toate informatiile despre acesta.
3. #### PUT USER: https://bizoni-backend-apis.azurewebsites.net/
   - [ ] Actualizeaza informatii despre un user folosind parametrii trimisi, numele utilizatorului nu poate fi schimbat.
4. #### DELETE USER: https://bizoni-backend-apis.azurewebsites.net/
   - [ ] Se foloseste de id-ul primit si in cazul in care coincide cu al detinatorului, contul va fi sters.


## FORMS:
1. #### GET FORMS: https://bizoni-backend-apis.azurewebsites.net/users/{user_id}/forms/
   - [ ] Returneaza toate formularele pentru un anumit user.
2. #### GET FORM BY ID: https://bizoni-backend-apis.azurewebsites.net/users/{user_id}/forms/{form_id}
   - [ ] Returneaza un formular folosind id-ul primit.
3. #### GET FORM BY QR: https://bizoni-backend-apis.azurewebsites.net/users/{user_id}/forms/{form_id}/getQR
   - [ ] Folosese codul QR pentru a returna un formular.
4. #### POST FORM: https://bizoni-backend-apis.azurewebsites.net/users/{user_id}/forms/
   - [ ] Creaza un formular folosind datele trimise.
5. #### PUT FORM: https://bizoni-backend-apis.azurewebsites.net/users/{user_id}/forms/{form_id}
   - [ ] Actualizeaza informatii despre un formular.
6. #### DELETE FORM: https://bizoni-backend-apis.azurewebsites.net/users/{user_id}/forms/{form_id}
   - [ ] Sterge un formular folosindu-se de id-ul primit pentru formular si utilizator.


## Workflow:
- Prima data cand un user intra pe site acesta este directionat catre "home page".
- Acolo acesta are doua optiuni, inregistrare  sau autentificare. Cand prima este aleasa acesta are de completat
cateva campuri urmand restrictiile impuse si dupa ce a introdus toate datele este apelata metoda "POST USER".
- A doua optiune ii cere acestuia sa introduca email-ul si parola iar in urma validarii acestora este apelata metoda "GET USER".
Dupa ce este autentificat acesta are acces la informatiile proprii si le poate modifica "PUT USER" sau isi poate sterge
contul "DELETE USER".
- Acesta are acum acces la formulare, pentru a le accesa pe cele proprii se va apela metoda "GET FORMS" care va returna toate
formularele ce ii apartin.
- Pentru a ajunge la unul creea de alt user acesta are nevoie de un link "GET FORM BY ID" sau poate scana un cod QR
"GET FROM BY QR".
- De asemenea un utilizator poate crea un formular "POST FORM" dupa propriile cerinte pe care ulterior il poate modifica
"PUT FORM", permitand acestuia sa faca un cod QR pentru formularul respectiv, si cand nu ii mai este de folos il poate
sterge "DELETE FORM".

