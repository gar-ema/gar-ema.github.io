---
hidden: true
title: DevCamp un breve resoconto
date: 2014-02-09 11:02:54
tags:
    - Microsoft dev camp
    - push notifications
    - windows 8
categories:
    - events
permalink: /2014/02/09/devcamp-un-breve-resoconto
---
Venedì scorso insieme ad Antonio, Mauro, Tino e Salvatore ho preso parte ai Microsoft Dev Camp 2014 a Napoli. Nel pomeriggio di questa giornata abbiamo tenuto delle mini sessioni tecniche su varie tematiche:

  * Antonio ci ha parlato di come usare i Mobile Services di Azure in una Windows store app 
  * Mauro di come lavorare con i file e le cartelle in Windows Phone 8 
  * io ho parlato di push notification “home made” per Windows Store App 
  * Tino ci ha parlato di sviluppo di giochi per windows phone 8 con Unity 3d 

Durante la mia mini-sessione ho illustrato come poter inviare push notification senza vincolarsi ai Mobile Services di Azure ed approfitto di questo post per fare un piccolo recap e poi gettare le basi per tutti quegli aspetti che non ho potuto trattare durante la sessione per ovvi vincoli di tempo

<iframe src="//www.slideshare.net/slideshow/embed_code/key/1wEpcSmsZ76Dkh" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/emagar83/push-notifications-31008655" title="Push notifications" target="_blank">Push notifications</a> </strong> from <strong><a target="_blank" href="//www.slideshare.net/emagar83">Emanuele Garofalo</a></strong> </div>


## Perché?

Scopo cardine delle push notification è fornire all’utente un’esperienza sempre più coinvolgente, partendo dall’aggiornamento costante delle informazioni. Queste informazioni ovviamente sono contenute anche nell’applicazione, ma le notifiche ci permettono di informare l’utente anche quando la nostra app non è in foreground. Esistono 4 tipi di notifiche push: 

  1. Tile 
  2. Badge 
  3. Toast 
  4. Raw (tipologia di notifica che non ho avuto il tempo di spiegare purtroppo, ma ci rifaremo nei prossimi post). 

Le Ti_le_ notifications sono quelle notifiche che aggiornano la tile della nostra app sullo start screen

Le B_adge_ notification ci permettono di aggiornare la nostra tile nello start screen e nel lock screen (in questo caso non si parla più di tile ma di badge) per comunicare in maniera rapida delle informazioni all’utente, ad esempio: numero di novità presenti nell’app oppure diverse iconcine (Glyph) che ci permettono di informare l’utente circa lo stato dell’applicazione (una panoramica la trovate qui: [http://msdn.microsoft.com/en-us/library/windows/apps/hh779719.aspx][1])

le _Toast_ notification (argomento su cui ho concentrato la mia demo) sono le notifiche che appaiono in alto a destra. Tra le notifiche le toast sono le più invasive e per questo motivo è richiesto che siano utilizzate in situazioni in cui sono effettivamente utili

le **_Raw_ (**che ho potuto trattare veramente poco venerdì scorso)**&#160;**sono notifiche a “corpo libero” (stringhe per intenderci) e vengono utilizzate per due scopi principali:

  * Invio di informazioni “generiche”: gestendo l’evento **PushNotificationReceived** del **NotificationChannel** recuperato per l’app; 
  * Trigger per Background Tasks: gestito in modo implicito dal sistema operativo (ovviamente da configurare nel vostro manifest) per avviare un vostro background task 

## Come?

l’invio di push notification segue un iter ben definito fatto di 6 passi (il sesto 

  1. L’app richiede un **NotificationChannel** alla Notification Client Platform tramite il metodo statico **CreatePushNotificationChannelForApplicationAsync** della classe **PushNotificationChannelManager** 
  2. la _Notification Client Platform_ contatta il _Windows Notification Service_ (WNS) e richiede un notification channel 
  3. Il notification channel ricevuto viene passato all’applicazione che provvede a contattare un “nostro” servizio web che lo salva associandolo all’utente/device 
  4. Quando richiesto il  della nostra applicazione contatta il WNS (con una richiesta post) ed invia le informazioni inerenti la nostra notifica 
  5. il WNS invia la notifica al Notification Client Platform che a seconda dei casi la gestisce
  6. La notifica viene gestita:
  1. Nel caso la nostra app sia in foreground e avessimo sottoscritto l’evento **PushNotificationReceived** questo verrebbe eseguito (con la stessa dinamica di un routed event) 
  2. nel caso la nostra app non sia in esecuzione sarà il sistema operativo a gestire la notifica, che a fronte della tipologia produrrà degli effetti differenti

Durante questo iter noi, in quanto sviluppatori, possiamo intervenire solo in 4 punti:

  1. Richiesta del notification channel 
  2. Registrazione/salvataggio del notification channel 
  3. invio della notifica al WNS 
  4. Gestione della notifica sul device 

Al fine di semplificare l’invio di push notification anche “on promise” all’interno della demo ho usato una piccola libreria che ho iniziato a sviluppare di recente (reperibile al link: [https://pushhelper.codeplex.com/][2])&#160; per semplificarmi e standardizzare i passi che compio nell’invio di push notification. In questo modo, con poche righe di codice invio delle notifiche verso windows 8.1 

All’interno del progetto oltre alla libreria ci sono anche il servizio ed il client di demo per poter testare l’invio di una tile ed una toast notification. Unici accorgimenti da seguire:

  1. valorizzare il tag identity nel manifest dell’applicazione client con i dati di un’app che dovete registrare sul dev center ([https://appdev.microsoft.com/StorePortals][3]) 
      * una volta creata l’app potete comodamente associare i dati facendo click sul progetto e dal dialog reperibile nel menù al percorso [_project –> store –> Associate app with the store]_ potete avviare una procedura di associazione “automatica” 
  2. richiedere il sid e la secret key per accedere al WNS relativi all’app che avete appena creato (saranno necessari per loggarvi sul WNS) 

Spero di riuscire, lavoro permettendo, a fare una serie di post (in breve termine) sull’argomento sperando che siano utili.

Stay tuned.

 [1]: http://msdn.microsoft.com/en-us/library/windows/apps/hh779719.aspx "http://msdn.microsoft.com/en-us/library/windows/apps/hh779719.aspx"
 [2]: https://pushhelper.codeplex.com/ "https://pushhelper.codeplex.com/"
 [3]: https://appdev.microsoft.com/StorePortals "https://appdev.microsoft.com/StorePortals"