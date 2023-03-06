# Back-End
## Back-End-ul echipei Bizonii în concursul Assist Tech Challenge.
 
Aplicația a fost realizată folosind fastAPI, un framework rapid ce folosește Python 3.7+

Aceasta dezvoltă un API care folosește o baza de date a unor utilizatori sunt logați pe
un site de completare automată a unor formulare.

### Comanda pe care o folosim pentru a menține serverul pornit este:
```"uvicorn main:app --reload"```


## Aplicația are 4 funcții principale GET, POST, PUT, DELETE:
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
   - [ ] Folosind un id-ul unui user returnează datele despre acesta. Unele restricții sunt că numele trebuie sa aibă cel puțin 3 litere și un individ nu poate să introducă un cod fiscal.
2. #### POST USER: https://bizoni-backend-apis.azurewebsites.net/
   - [ ] Crează un user nou folosind datele trimise, verifică dacă email-ul și numele trimise nu se regăsesc 
   în baza de date și returnează toate informațiile despre acesta.
3. #### PUT USER: https://bizoni-backend-apis.azurewebsites.net/
   - [ ] Actualizează informații despre un user folosind parametrii trimiși, numele utilizatorului nu poate fi schimbat.
4. #### DELETE USER: https://bizoni-backend-apis.azurewebsites.net/
   - [ ] Se folosește de id-ul primit și in cazul în care coincide cu al deținatorului, contul va fi șters.


## FORMS:
1. #### GET FORMS: https://bizoni-backend-apis.azurewebsites.net/users/{user_id}/forms/
   - [ ] Returnează toate formularele pentru un anumit user.
2. #### GET FORM BY ID: https://bizoni-backend-apis.azurewebsites.net/users/{user_id}/forms/{form_id}
   - [ ] Returnează un formular folosind id-ul primit.
3. #### GET FORM BY QR: https://bizoni-backend-apis.azurewebsites.net/users/{user_id}/forms/{form_id}/getQR
   - [ ] Folosește codul QR pentru a returna un formular.
4. #### POST FORM: https://bizoni-backend-apis.azurewebsites.net/users/{user_id}/forms/
   - [ ] Crează un formular folosind datele trimise.
5. #### PUT FORM: https://bizoni-backend-apis.azurewebsites.net/users/{user_id}/forms/{form_id}
   - [ ] Actualizează informații despre un formular.
6. #### DELETE FORM: https://bizoni-backend-apis.azurewebsites.net/users/{user_id}/forms/{form_id}
   - [ ] Șterge un formular folosindu-se de id-ul primit pentru formular si utilizator.


## Workflow:
- Prima dată când un user intră pe site acesta este direcționat către "home page".
- Acolo acesta are doua opțiuni, înregistrare  sau autentificare. Când prima este aleasă acesta are de completat
câteva câmpuri urmând restricțiile impuse și după ce a introdus toate datele este apelată metoda "POST USER".
- A doua opțiune îi cere acestuia să introducă email-ul și parola iar în urma validării acestora este apelată metoda "GET USER".
După ce este autentificat acesta are acces la informațiile proprii și le poate modifica "PUT USER" sau își poate șterge
contul "DELETE USER".
- Acesta are acum acces la formulare, pentru a le accesa pe cele proprii se va apela metoda "GET FORMS" care va returna toate
formularele ce îi aparțin.
- Pentru a ajunge la unul creat de alt user acesta are nevoie de un link "GET FORM BY ID" sau poate scana un cod QR
"GET FROM BY QR".
- De asemenea un utilizator poate crea un formular "POST FORM" după propriile cerințe pe care ulterior îl poate modifica
"PUT FORM", permițând acestuia să facă un cod QR pentru formularul respectiv, și când nu îi mai este de folos îl poate
șterge "DELETE FORM".
