---
title: Voglio un EventSource tutto per me!!!
date: 2010-05-12T06:56:38+00:00
permalink: /2010/05/12/voglio-un-eventsource-tutto-per-me/
categories:
  - Tech
  - .net
  - c#
tags:
  - .net
  - EventLog
  - Tips
---
Scenario: sono stanco di farmi filtri sul registro degli eventi per avere i messaggi (d&rsquo;errore, di warning, di info&hellip;&hellip; a seconda del trace level) che riguardano la mia applicazione, oggi faccio i capricci come i bambini, e voglio un EventSource tutto per me

Semplice da realizzare, e forse non &egrave; nemmeno da considerare un capriccio,perch&egrave; effettivamente scrivere nell&rsquo;eventlog in un&rsquo;area riservata solo a me mi da la possibilit&agrave; di distinguere facilmente poi eventuali errori in maniera pi&ugrave; efficiente e senza dover ricorrere a dei filtri, che poi dovr&ograve; esportare ed importare, quando passer&ograve; dall&rsquo;ambiente di sviluppo a quello di test, e mi toccher&agrave; rifarlo quando passer&ograve; da test a produzione (no vi prego, io al massimo voglio fare click su &ldquo;publish&rdquo; per andare in produzione)

il codice che potete usare per testare il tutto &egrave;:
{% highlight cs %}
 EventSourceCreationData source = new EventSourceCreationData("test";, "testLogFile");   

 if (!EventLog.Exists("testLogFile"))   
    EventLog.CreateEventSource(source); 
 
 EventInstance inst = new EventInstance(20, 1, EventLogEntryType.Error);   
 EventLog.WriteEvent("test", inst, "messaggio da loggare"); 
 
 //e qui il codice per pulire se non vogliamo lasciare nessuna traccia del nostro log
 
 if (EventLog.SourceExists("test"))   
    EventLog.DeleteEventSource("test"); 
 
 if (EventLog.Exists("testLogFile"))   
    EventLog.Delete("testLogFile");
{% endhighlight %}

<a target="_blank" href="{{ site.url }}/assets/imgs/posts/2055.eventsourceditest_1AE06652.png">
<img height="80" width="488" src="{{ site.url }}/assets/imgs/posts/2055.eventsourceditest_1AE06652.png" alt="eventsource di test" border="0" title="eventsource di test" style="display:inline;border-width:0;" /></a>

&nbsp;

A questo punto (in verit&agrave; l&rsquo;avrei gi&agrave; detto almeno 20 righe fa) perch&eacute; dovrei scegliere di loggare in questo modo e non usare log4net&hellip;e farlo in altri modi: su un file di log, o su un db&hellip;o tanti altri modi. Vi risponder&ograve; parafrasando un noto personaggio&hellip;&rdquo;LA RISPOSTA E&rsquo;&hellip;NON LO SO&rdquo;.
Volendo essere più professionali in realtà è questione di requisiti,  nel senso che ci sono realt&agrave; in cui non &egrave; permesso l&rsquo;uso di librerie sviluppate dall&rsquo;esterno, o situazioni che richiedono una soluzione ad alta personalizzazione, insomma&hellip;ci sono svariati motivi per scegliere di loggare cos&igrave;.

E.