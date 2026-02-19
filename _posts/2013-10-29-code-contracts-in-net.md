---
hidden: true
title: Code Contracts in .Net
date: 2013-10-29 12:10:00
tags:
    - .Net Framework
    - code contracts
    - invariants
    - postcondition
    - precondition
categories:
    - .net
    - c#
    - programming
permalink: /2013/10/29/code-contracts-in-net
---


Se ne parla da un po’, ormai qualcuno se li è pure dimenticati, ma i code contracts sono sempre lì in attesa di essere utilizzati…già…ma da chi?? Io posso utilizzarli??

La risposta che mi sono dato è: tutti possono utilizzarli…l’importante è tenere a mente alcuni concetti. Per esempio: 

1. cosa sono **preconditions**, **postconditions** ed **invariants**?
    - **Preconditions**: quali sono le condizioni per cui un metodo deve essere chiamato?
    - **Postconditions**: quali condizioni devono verificarsi affinché in uscita da un metodo la sua esecuzione risulti corretta?
    - **Invariants**: quali condizioni non cambiano prima e dopo l’esecuzione di un metodo?

2. Che runtime sto utilizzando? A seconda del runtime che stiamo utilizzando il namespace Contract è incluso in un assembly differente
    - A partire dalla v4 del CLR e Silverlight 4 il namespace Contract è incluso nell’assembly mscorlib.dll
    - per le altre versioni si trova nell’assembly Microsoft.Contracts.dll che potete trovare a seconda della versione del runtime che state utillizzando nel percorso indicato nel capitolo 1 della documentazione ufficiale (reperibile a >> [questo indirizzo](http://research.microsoft.com/en-us/projects/contracts/userdoc.pdf) <<)

Per quanto riguarda le domande al punto 1, rispondendo si ottengono dei **contratti **(clausole) che descrivono quale deve essere il comportamento di un metodo. Per esempio: supponiamo che un mio metodo abbia una postcondition che richiede che una variabile risulti valorizzata con un certo valore, ebbene, se nel momento in cui sto per uscire dal metodo la variabile non rispetta la clausola sono in una situazione di comportamento *anomalo*. 

L’approccio classico prevede che si scrivano prima i contratti, e poi l’implementazione del metodo di turno. *Ma se ci pensiamo bene quale altro approccio prevede un iter simile?* La risposta a mio avviso è TDD a.k.a. Test Driven Development. a.k.a. Scrivi i test per il tuo codice (e se sei sia sviluppatore che tester scrivi i test prima di sviluppare il tuo metodo), e smettila di premere F5 per farlo!!!


Volendo focalizzare la nostra attenzione sulla scrittura di Unit Test, quindi, diventa facile a questo punto intuire che TDD e Code Contracts sono complementari (non contrastanti) tra di loro, per cui, la scrittura dei nostri metodi deve prima di tutto passare per la scrittura dei test e poi per la definizione dei contratti, senza però essere obbligati a testare le condizioni imposte nei Code Contracts. Allo stesso tempo la combinazione di Unit Test e Code Contracts ci permette di avere più chiaro, nel caso un test fallisca, il perché questo stia fallendo, soprattutto nei casi in cui una delle clausole fallisca. Alcuni tool di testing automatico, tipo Pex, traggono vantaggio dai Code Contracts, per eliminare tutte quelle casistiche che non li rispettano, e che quindi risulterebbero *poco interessanti*.

### Ma come si usano i Code Contracts?

Quante volte vi sarà capitato di scrivere qualcosa del tipo:

{% highlight cs %}
public void MyMethod(IList<MyClass> items, int id) 
{
    if (items == null)
       throw new ArgumentNullException("items");
    if (id < 0) 
       throw new ArgumentOutOfRangeException("id")
...
}
{% endhighlight %}

questi controlli sono delle precondition per il vostro metodo, in pratica vi state accertando che la collection sia valorizzata, e che l’id non sia inferiore a zero; semplici controllo che permetteranno al vostro metodo di non “andare in eccezione” per motivi che non avrete preso in considerazione, bensì il vostro metodo in questi casi rilancerà un’eccezione. Con i code contracts potrete scrivere gli stessi controlli in maniera molto semplice e leggibile nel seguente modo:

{% highlight cs %}
public void MyMethod(IList<MyClass> items, int id)
{
    Contract.Requires(items != null);
    Contract.Requires(id >= 0);
    ...
}
{% endhighlight %}

Come potete vedere abbiamo scritto le condizioni negando i controllo che facevamo con l’approccio basato sull’uso dell’if, questo però rende fluida la lettura del nostro codice, quasi come se stessimo scrivendo “è necessario che items sia diverso da null” oppure “è necessario che id sia maggiore o uguale a zero” piuttosto che dover leggere qualcosa del tipo “se items è null solleva un’eccezione” oppure “se id è minore di zero solleva un’eccezione”. Questo codice però è tutt’altro che utilizzabile in produzione così com’è scritto, per poter fare in modo che il compilatore sostituisca la nostra richiesta di utilizzare la classe Contract con la corretta implementazione abbiamo bisogno di un tool chiamato **ccrewriter **che sostanzialmente riscrive il nostro codice prima di compilarlo in modo che esegua, in maniera ottimizzata i check che abbiamo espresso, il tutto senza però richiedere l’utilizzo di meccanismi pesanti (dal punto di vista delle performance) come la reflection.


Ovviamente, essendo un tool a riga di comando, ccrewriter risulta scomodo da utilizzare nella vita di tutti i giorni. Per utilizzare in modo facile e soprattutto comodo i Code Contracts conviene installare un plug-in per Visual Studio, reperibile a >> [questo indirizzo](http://visualstudiogallery.msdn.microsoft.com/1ec7db13-3363-46c9-851f-1ce455f66970) <<. 
Una volta installato, questo plug-in, aggiunge in VS all’interno delle proprietà dei progetti un nuovo tab chiamato Code Contracts 

[![01[1\]](https://i0.wp.com/old.dotnetcampania.org/cfs-file.ashx/__key/CommunityServer.Blogs.Components.WeblogFiles/nezumi.metablogapi/8203.011_5F00_5E8FB0B9.png)](http://sdrv.ms/1euqJcr)

Con queste impostazioni non dovrete specificare istruzioni di precompilazione, o utilizzare il tool, vi basterà modificare le impostazioni nel modo che vi è più congeniale.

Spero che questa rapida panoramica possa essere utile, per chi non lo fa già, ad approcciare i code contracts per l’utilizzo nella vita di tutti i giorni.

La riflessione che mi viene da fare quando penso ai code contracts è: E’ vero non siamo degli artisti, ne dei poeti, ma già scrivere del codice di facile lettura, il quale rende facile capire qual’è il comportamento che ci si aspetta da un metodo ci rende sicuramente la vita molto più semplice.

E.