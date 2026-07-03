---
title: "Talks"
permalink: /talks/
author_profile: true
---

Le mie presentazioni come speaker, e gli eventi a cui partecipo, aiuto a organizzare o a cui va solo di dare visibilità.

{% assign today = site.time | date: '%Y-%m-%d' %}
{% assign upcoming_talks = site.data.talks | where_exp: "t", "t.date == nil or t.date >= today" %}
{% assign past_talks = site.data.talks | where_exp: "t", "t.date != nil and t.date < today" %}

## Prossimi eventi

{% include events-list.html talks=upcoming_talks empty_text="Nessun evento in programma al momento." %}

## Eventi passati

{% include events-list.html talks=past_talks empty_text="Nessun evento passato ancora registrato." %}
