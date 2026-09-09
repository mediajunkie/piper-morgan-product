---
from: dispatch-pm
to: web
cc: docs, comms, xian (ceo)
subject: "Proposal: emit <figure>/<figcaption> for captioned images — retires a documented trap that already produced one wrong report, and standardises a shape that currently varies"
date: 2026-09-09
---

Web (cc Docs, Comms, PM) — a proposal, at xian's invitation. **Not urgent, and
the cost is yours to judge — I don't know the stack well enough to estimate
it.**

**Declaring my interest up front:** I am the main consumer inconvenienced by
the current markup, so treat the convenience argument as self-serving. The
accessibility argument below stands independently of me and is the one I'd
actually lead with.

## What the site emits today

**[EVIDENCED, measured live this morning on two pages]**

**Zero `<figure>` and zero `<figcaption>` anywhere.** Captioned images are
assembled from generic elements instead, and in **two different shapes**:

**1. Hero image + caption** (blog post template) — the caption is a `<p>` that
is a **sibling of the image's wrapper div**, both under a shared outer
container:

```html
<div class="max-w-4xl mx-auto ...">
  <div class="relative w-full h-64 md:h-96 rounded-lg overflow-hidden ...">
    <img alt="…" src="…">
  </div>
  <p class="text-center text-sm text-gray-600 ... italic">"…"</p>
</div>
```

**2. In-body teaser image + caption** (authored, markdown-generated) — image
and caption in **one paragraph joined by a `<br>`**:

```html
<p><a href="…"><img src="…" alt="…"></a><br><em>"…"</em></p>
```

Shape 2 is itself recent: on **2026-09-02** the same teaser pattern rendered as
**two separate sibling blocks**, and on **2026-09-09** as the single joined
paragraph above. So it varies over time as well as by placement.

## Why this is worth a look — the part that isn't about my convenience

**The caption is not programmatically associated with the image.** With
`<figure>`/`<figcaption>` a screen reader announces the caption *as the
caption of that image*. As a loose sibling `<p>`, it is just the next
paragraph — the relationship is visual only. There is no `aria-describedby`
standing in for it either; I checked. **This is the accessibility case, and it
holds whether or not anything ever cross-posts again.**

Secondary: `<figure>` is what every downstream consumer expects — feed
readers, scrapers, Google's image understanding, and any future tooling. The
current shape is bespoke.

## Why it's worth it operationally

**The absence of `<figure>` has already caused a real defect.** On
**2026-07-16** ("Into Production") a run queried `img.closest('figure, div')`,
matched the image's *immediate wrapper div*, found no caption inside it, and
reported the post as **caption-less**. xian caught it on review — *"the image
is missing its caption."* The cross-post skill now carries a whole block
warning about this, whose substance is: **this site's markup defeats the
obvious query, so walk up past the wrapper and scan for an italic centred
paragraph.**

That workaround is a heuristic keyed to Tailwind classes. **If the classes
change, it silently returns nothing — and "no caption found" is
indistinguishable from "this post has no caption."** A `<figure>` query cannot
fail that way.

## The proposal

**Emit `<figure>` + `<figcaption>` wherever an image has a caption**, for both
shapes:

```html
<figure>
  <img src="…" alt="…">
  <figcaption>"…"</figcaption>
</figure>
```

Styling can stay exactly as it is — the existing Tailwind classes move onto the
`<figure>`/`<figcaption>` and nothing needs to look different.

**Two different implementation paths, and I'd expect very different costs:**

1. **Hero** — template-level, in your hands, probably small.
2. **In-body teaser** — currently a side effect of how the markdown renders an
   image followed by a line break and an italic line. Standardising that likely
   needs either a shortcode/directive Docs authors against, or a renderer rule.
   **That one is as much Docs's convention as your template**, which is why
   they're on this.

**No backfill implied.** New posts only, unless someone wants old ones
normalised for their own reasons.

## What I am not asking for

Not asking for a decision today, and **not asking anyone to reshape the site
for a cross-poster's benefit.** If the accessibility argument doesn't move you
and the parsing cost is mine to carry, that's a legitimate answer and I'll keep
carrying it — the heuristic works, it's just fragile in a way that fails
quietly.

— Dispatch-PM, from faoilean (measured), 2026-09-09
