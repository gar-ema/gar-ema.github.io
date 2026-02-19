---
title: "Old Articles"
permalink: /old-articles/
---

{% assign posts_by_year = site.posts | where: "hidden", true | group_by_exp: "post", "post.date | date: '%Y'" %}

{% for year in posts_by_year %}
## {{ year.name }}

<ul>
{% for post in year.items %}
  <li>
    <small>{{ post.date | date: "%d/%m" }}</small> &mdash;
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
  </li>
{% endfor %}
</ul>
{% endfor %}
