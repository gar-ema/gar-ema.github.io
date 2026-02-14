---
title: Dichiarare l'uso di un metodo (una classe o un'interfaccia…) deprecato
date: 2012-01-27T06:34:51+00:00
permalink: /2012/01/27/dichiarare-luso-di-un-metodo-una-classe-o-uninterfaccia-deprecato/
categories:
  - programming
  - archive
---

  Non so se vi è mai capitato, ma nel caso spero possa esservi utile, di dover dichiarare che non è più consigliato l’utilizzo di una vostra classe o di un vostro metodo a seguito di modifiche al progetto. Qualsiasi sia il vostro caso vi basta decorare il vostro metodo o un’interfaccia o una classe) e decorarla con l’attributo <strong>Obsolete </strong> 
  <br />

  <!--![{{ site.url }}/imgs/posts/8446.Obsolete_70FF811E.png]()-->
<p>
  <a href="{{ site.url }}/assets/imgs/posts/8446.Obsolete_70FF811E.png">
  <img title="Obsolete" border="0" alt="Obsolete" align="left" src="{{ site.url }}/assets/imgs/posts/8446.Obsolete_70FF811E.png" width="383" height="240" />
  </a>
  </p>


Come potete vedere la classe espone 3 costruttori: il primo senza parametri si limita a segnalare un warning nel caso si usi quel metodo, il secondo, oltre al warning visualizza un messaggio, ed il terzo invece indica al compilatore di trattare l’utilizzo del metodo come errore.
spero possa esservi utile in qualche modo per esempio nel caso stiate facendo un pò di refactoring sulla vostra applicazione e vogliate tener traccia di quanto è cambiato nel tempo.

E.