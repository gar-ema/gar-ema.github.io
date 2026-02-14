---
title: Except with linq
date: 2009-10-09 21:10:13
tags:
    - linq
    - Except
    - .net
categories:
    - programming
    - .net
permalink: /2009/10/09/except-with-linq
---

<p>Alcune volte può capitare che abbiate bisogno di vedere quali elementi di una collezione non siano inclusi in un’altra collezione.&#160; (NOT IN)</p>
<p>Per esempio: Il classico libretto universitario</p>
<ul>
  <li>ho una lista di esami da sostenere per quanto riguarda il mio corso di laurea </li>
  <li>ho una lista di esami che ho già sostenuto </li>
  <li><strong>voglio la lista degli esami da sostenere </strong>
  </li>
</ul>
<p>il risultato in codice </p>

{% highlight cs %}

IList<Esame> esami = InQualcheModoRecuperoTuttiGliEsamiDelMioCorsoDiLaurea(); // :-)
IList<Esame&gt; esamiSostenuti = InQualcheModoRecuperoTuttiGliEsamiSostenuti();
var esamiDaSostenere = from r in esami
                       where esamiSostenuti.All(m => m.Id != r.Id)
                       select r;
{% endhighlight %}

<p>et voilà! :-) ho escluso dalla lista, di tutti gli esami, quelli che ho sostenuto</p>
<p>ps: Ovviamente nel mio caso ho previsto che gli esami fossero identificati da un id </p>
<p>pps: Mi scuso per l’indentazione </p>