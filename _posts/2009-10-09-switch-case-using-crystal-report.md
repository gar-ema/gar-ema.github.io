---
hidden: true
title: Switch case using Crystal Report
date: 2009-10-09 11:25:13
tags:
    - Crystal report
categories:
    - programming
permalink: /2009/10/09/switch-case-using-crystal-report
---

<p>Sometimes may occur that you need to use the construct SWITCH-CASE in a Formula Field.</p>
<p>Well, the syntax is really simple:</p>
<p>Switch( condition, what_output, condition, what_output&hellip;.)</p>
<p>for example</p>
<p><b>Switch ([customer.sex] = &ldquo;Male&rdquo;, &ldquo;You are Welcome&rdquo;, [customer.sex] = &ldquo;Female&rdquo;, &ldquo;You are VERY Welcome&rdquo;)</b> <i>:) <br /></i></p>
<p>nothing more,nothing less</p>
<p>&nbsp;</p>
<p>E.</p>