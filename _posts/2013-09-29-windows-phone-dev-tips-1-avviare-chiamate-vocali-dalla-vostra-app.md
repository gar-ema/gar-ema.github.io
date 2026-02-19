---
hidden: true
title: 'Windows Phone Dev Tips #1: Avviare chiamate vocali dalla vostra app'
date: 2013-09-29 04:09:09
tags:
    - windows phone
categories:
    - programming
permalink: /2013/09/29/windows-phone-dev-tips-1-avviare-chiamate-vocali-dalla-vostra-app
---
Può capitare in alcune applicazioni (es: chat con registrazioni basata su numero telefonico) di voler offrire la possibilità di avviare chiamate vocali dall’app stessa . A tal proposito nel SDK per Windows Phone è presente un task ad-hoc.

Tutto quello che avete bisogno di scrivere è:
   
{% highlight cs %}

new PhoneCallTask { PhoneNumber = "003912345678" }.Show();

{% endhighlight %}

per far visualizzare all’utente una richiesta di conferma (per ovvie ragioni, es: Evitare lo spam) per l’avvio della chiamata.

al prossimo tip.

E.