<center>
<h1>[Università degli Studi di Firenze - UNIFI] Tesi sulla Creazione di un Sito Web per la Generazione di Poltrone e Divani utilizzando ControlLoRA Versione 3 di HighCWu</h1>
</center>

---

## Scopo del progetto

L’obiettivo di questo progetto di tesi è la progettazione e lo sviluppo di un **sito web dedicato alla modifica e personalizzazione di poltrone e divani**, con l’intento di rendere il processo di design più semplice ed efficace per l’utente.

Il sistema è pensato principalmente per **professionisti e appassionati di design e progettazione**, come designer industriali, grafici, architetti e ingegneri.

Questi utenti possiedono competenze tecniche avanzate, ma cercano strumenti che supportino la creatività e velocizzino lo sviluppo dei loro progetti. Il sito permette di **esplorare rapidamente diverse alternative progettuali**, sfruttando modelli generativi capaci di creare molteplici varianti dello stesso divano o poltrona utilizzando materiali e tessuti differenti.

---

## Note

In questo repository sono implementate tutte le funzionalità **backend** dell’applicazione Django, inclusi:
- le **views**
- i **templates**
- i **task Celery**

La generazione delle immagini e il training dei modelli avviene invece su un **server esterno** eseguito in un pod di **Runpod**, al quale l’app Django invia richieste tramite una **coda di lavori gestita da Redis e Celery**.

---

## Architettura
<a href="https://ibb.co/3mZ00cQN"><img src="https://i.ibb.co/jkXLLDsM/Architettura-App-Web.png" alt="Architettura-App-Web" border="0"></a>

---

## Avvio del WebSite

Segui questi passaggi per avviare il sito:

1. **Avviare il server Django**
    -  Apri il terminale e digita:
   ```bash
   cd CouchCraft_AI
   python manage.py runserver

2. **Avviare il Celery Worker**
    - Apri un altro terminale e digita:

   ```bash
   cd CouchCraft_AI
   celery -A CouchCraft_AI worker --pool=solo -l info

3. Per accedere al sito recarsi a: <a href="http://localhost8000"> http://localhost8000 </a>

---

## Licenza e Crediti

<ul>
  <li>Fonte: il progetto è ispirato al codice <a href="https://github.com/HighCWu/control-lora-v3"> HighCWu/control-lora-v3 </a> </li>
  <li>Backend AI: <a href="https://github.com/Novalynne/Tesi-CtrLora"> Novalynne/Tesi-CtrLora </a></li>
  <li>Modelli: <a href="https://huggingface.co/HighCWu/control-lora-v3">[Models]</a> | <a href="https://huggingface.co/spaces/HighCWu/control-lora-v3">[Spaces]</a></li>
</ul>

Maintainer: Martina Schirone (7074808) — Università degli Studi di Firenze