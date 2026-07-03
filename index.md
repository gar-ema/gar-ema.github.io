---
layout: single
author_profile: true
title: "Unhandled Exception"
excerpt: "Solution Architect &amp; Community Speaker"
---

Ciao! Sono **Emanuele Garofalo**, Solution Architect e appassionato di tecnologia. Partecipo alla community
tecnica come speaker, organizzatore e, ogni tanto, semplice sostenitore di eventi che meritano visibilità.
Qui sotto trovi i miei prossimi appuntamenti, quelli passati e i vecchi articoli del blog.

[Scopri di più su di me →](/about/){: .btn .btn--inverse }

{% assign today = site.time | date: '%Y-%m-%d' %}
{% assign upcoming_talks = site.data.talks | where_exp: "t", "t.date == nil or t.date >= today" %}
{% assign past_talks = site.data.talks | where_exp: "t", "t.date != nil and t.date < today" %}
{% assign past_talks_recent = past_talks | slice: 0, 3 %}

## Prossimi eventi

{% include events-list.html talks=upcoming_talks empty_text="Nessun evento in programma al momento — torna a trovarmi presto!" %}

## Eventi passati

{% include events-list.html talks=past_talks_recent empty_text="Ancora nessun evento passato registrato." %}

[Vedi tutti i talk →](/talks/){: .btn .btn--inverse }

## Blog

Ho scritto diversi articoli tecnici nel corso degli anni, principalmente su .NET, C# e architettura software.
Sono archiviati ma sempre disponibili.

[Vai al blog →](/old-articles/){: .btn .btn--primary }
