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
1. #### GET USER: https://bizoni-backend-apis.azurewebsites.net/docs#/users/{user_id}
   - [ ] Folosind un id-ul unui user returneaza datele despre acesta.
2. #### POST USER: https://bizoni-backend-apis.azurewebsites.net/docs#/
   - [ ] Creaza un user nou folosind datele trimise, verifica daca email-ul si numele trimise nu se regasesc 
   in baza de date si returneaza toate informatiile despre acesta.
3. #### PUT USER: https://bizoni-backend-apis.azurewebsites.net/docs#/
   - [ ] Actualizeaza informatii despre un user folosind parametrii trimisi, numele utilizatorului nu poate fi schimbat.
4. #### DELETE USER: https://bizoni-backend-apis.azurewebsites.net/docs#/
   - [ ] Se foloseste de id-ul primit si in cazul in care coincide cu al detinatorului, contul va fi sters.


## FORMS:
1. #### GET FORMS: https://bizoni-backend-apis.azurewebsites.net/docs#/users/{user_id}/forms/
   - [ ] Returneaza toate formularele pentru un anumit user.
2. #### GET FORM BY ID: https://bizoni-backend-apis.azurewebsites.net/docs#/users/{user_id}/forms/{form_id}
   - [ ] Returneaza un formular folosind id-ul primit.
3. #### GET FORM BY RQ: https://bizoni-backend-apis.azurewebsites.net/docs#/users/{user_id}/forms/{form_id}/getQR
   - [ ] Folosese codul QR pentru a returna un formular.
4. #### POST FORM: https://bizoni-backend-apis.azurewebsites.net/docs#/users/{user_id}/forms/
   - [ ] Creaza un formular folosind datele trimise.
5. #### PUT FORM: https://bizoni-backend-apis.azurewebsites.net/docs#/users/{user_id}/forms/{form_id}
   - [ ] Actualizeaza informatii despre un formular.
6. #### DELETE FORM: https://bizoni-backend-apis.azurewebsites.net/docs#/users/{user_id}/forms/{form_id}
   - [ ] Sterge un formular folosindu-se de id-ul primit pentru formular si utilizator.

