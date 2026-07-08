# Software for an Audience of One

*Part 5 of the series "Beyond the Sea of App Icons." Part 1 introduced the two pillars of AI-native computing — the computer that understands and the computer that builds. This article is about the economics of the second.*

---

## The claim

Look at what is actually sitting in my workspace today. Six collections — the schema-plus-records applications Part 4 of this series describes — have grown their own bespoke interfaces, each a self-contained HTML file the agent wrote on request:

| Collection | Custom view | What it is |
|---|---|---|
| `restaurants` | `tokyo-map.html` | Tokyo restaurants laid out as a subway map |
| `watchlist` | `gallery.html` | A movie-poster wall |
| `vocabulary` | `flashcards.html` | An interactive flashcard drill |
| `portfolio` | `allocation.html` | An asset-allocation chart |
| `baseball-scout` | `radar.html` | Per-player rating radar charts |
| `mag2-subscribers` | `trend.html` | A subscriber-count trend line |

A feed has one too: the Lex Fridman podcast gallery is *read-write*, with my own rating, notes, and resume-position fields layered on top of the ingested RSS.

Every one of these is software that **no company would ever build.** Maggie Appleton, speaking at the Local-First conference in May 2024, gave the category its exact description: "software solutions that no industrial software company would build — because there's not enough market value in doing it." The addressable market for "my restaurants, drawn as a Tokyo subway map, to my taste" is exactly one person. The market for the poster wall is one person. The market for the rating radar is one person. Under the economics that governed software for fifty years, that made each of them *impossible* — not hard, impossible, because the cost of building software was far larger than the value any single user could justify. And I never wrote, or even saw, a line of the HTML. I described what I wanted; the code appeared.

The claim of this essay is simple: **the marginal cost of bespoke software has collapsed to near zero, and that single fact inverts the central economic constraint of the entire software industry.** What follows is what that inversion breaks, what it does *not* break, and the one cost it relocates rather than removes.

---

## 1. The economics that forced "software for the mass"

Software was always built for the average of an audience, never for the individual — but this was a consequence, not a preference. The cause was a cost structure:

```text
cost to build software        = large, fixed, paid up front
cost to serve one more user   ≈ zero
∴ rational strategy           = spread the fixed cost over as many users
                                as possible → build for the mass
```

Because development was expensive and replication was free, every product had to find the largest common denominator of need that would repay its build cost. That pressure shows up everywhere in how software feels: the settings panel that gestures at flexibility you will never fully use; the feature you wish existed but that "isn't worth building for your use case"; the workflow that is 80% right and permanently 20% wrong because the missing 20% differs for every user and no single version can satisfy all of them. None of this is a failure of taste. It is the arithmetic. A product priced to recoup a fixed build cost across millions of users *must* regress to their mean.

The history of software is in large part a history of fighting this constraint from the user's side — of pushing some authoring power back down to the individual so they could close the last 20% themselves. The spreadsheet, the macro, the scripting layer, the no-code builder: each handed the user a constrained way to build a sliver of bespoke software without a development team. We return to those in §4, because they are the honest precedent. But each one bought individualization only by forcing the user to become, partly, a programmer.

---

## 2. The collapse

The constraint had a single load-bearing term: *the cost to build software is large.* Remove it and the whole structure falls.

An LLM that can generate working code on demand removes it. The Tokyo-subway restaurant map was not amortized across a market; it was produced, in one exchange, for one person, at a cost that rounds to nothing. The arithmetic of §1 now reads:

```text
cost to build bespoke software  ≈ a sentence of intent  →  near zero
∴ rational strategy             = build for exactly this person, this purpose
```

When building for one becomes as cheap as building for millions, the reason to build for millions — *cost amortization* — evaporates. Software no longer has to find the largest common denominator of need, because it no longer has a fixed cost to repay. It can fit a denominator of one.

This is the new phase. Not "software is easier to build" — that undersells it. The category that was economically impossible for the entire history of the field, **software whose audience is a single person**, has become not just possible but the *default* for a large class of needs. The interesting unit of software is no longer the product shipped to a market. It is the artifact grown for an individual.

---

## 3. Code becomes an intermediate representation, not the deliverable

The most important detail in the opening is the one easiest to skip past: **I never saw the HTML.** This is not a missing feature. It is the structural signature of the new phase.

In traditional software, the source code *is* the asset. It is expensive to produce, so it is precious; it is precious, so it is version-controlled, reviewed, tested, refactored, and maintained for years. The whole discipline of software engineering is the care-and-feeding of an expensive, durable artifact.

When code costs almost nothing to produce, it stops being the asset and becomes **an intermediate representation** — a compile target between intent and behavior, no more precious than the assembly a compiler emits. The durable things are the two ends:

```text
   INTENT                 CODE                    DATA
   (natural language) →   (generated HTML/JS)  ←  (the collection's records)
   durable                disposable               durable
   "draw my restaurants                            restaurants/items/*.json
    as a subway map"      regrown on demand
```

The view is downstream of both and owns neither. When the need changes you do not *maintain* the view — you *regrow* it. "Also color the stations by cuisine" does not open a code review; it reissues the request, and a new artifact replaces the old. The Lex Fridman feed adding personal rating fields, the restaurant guide gaining a "visited" flag — in Part 4's terms these are schema edits; at the view layer they are simply regenerations. Disposability is not a weakness of this software. It is the property that makes building-for-one affordable, and it is the cleanest break from everything that came before. We have spent decades making code *easier to maintain*. The new phase makes maintenance, in many cases, beside the point: it is cheaper to regenerate the artifact than to repair it.

This is the view-layer instance of the broader thesis Part 6 of this series takes up: the workspace's durable truth is data and intent; the code is the agent's transient output. Where that argument concerns *schemas the agent authors into itself*, here it is sharper still, because a view is even more disposable than a schema — nobody curates it, nobody reads it, it exists only to render once and be replaced.

---

## 4. The honest precedent: spreadsheets and no-code

A claim that LLMs invented "software for an audience of one" would be false, and the falseness is instructive. The category already existed. Its name was the **spreadsheet.**

VisiCalc, HyperCard, Excel — these were the first mass tools for building software with a market of one. A personal budget model in Excel is bespoke software: a data model, computations, a UI, used by exactly the person who built it and no one else. The no-code platforms that followed — Airtable, Notion, Retool — extended the same idea. So the individualizing impulse is old. What was missing was never the *desire* for personal software; it was the *cost.*

The desire even has a literature. Clay Shirky called it "situated software" in 2004: software built for a specific group of people in a specific context, rather than for the generic market of "users." Robin Sloan, in February 2020, called it "An App Can Be a Home-Cooked Meal" — an app "you make for the people you know and love," one that is "not meant to scale," worth making for the same reason dinner is. Appleton's 2024 talk placed her barefoot developers — technically capable non-programmers, after China's barefoot doctors — squarely in this lineage, which she traces back further still, to Ivan Illich's *Tools for Conviviality*. And five years on, Sloan's 2025 retrospective on his home-cooked app named the virtue that only ownership confers: *sovereignty* — software that never redesigns itself out from under you, because no vendor holds it. These writers saw the destination clearly. What none of them had was a way to make reaching it cheap.

Seeing the precedent clearly is what makes the genuinely new thing visible. Every prior tool for software-for-one bought individualization at the price of **two constraints**, and the LLM is the first to remove both at once:

```text
                          authoring surface        authoring burden
                          (what you can express)   (who does the work)
   spreadsheet / no-code  constrained DSL,          the USER assembles it
                          a grid or block palette   (must become a programmer)

   LLM codegen            arbitrary code            the AGENT writes it
                          (full HTML/JS/charts)     (user only describes)
```

The spreadsheet removed the development *team* but kept the user inside a grid and made the user do the building. No-code widened the grid into a block palette but still cast the user as the composer. Both traded generality and effort for access. The LLM removes **both** constraints simultaneously: the authoring surface becomes arbitrary code — a subway-map layout is not a thing any spreadsheet or no-code builder offers — *and* the authoring burden moves off the user entirely. You do not assemble; you describe. That double removal is the actual novelty, and naming the precedent is what lets us locate it precisely.

In the terms this series set out in Part 1, the double removal *is* the second pillar — **the computer that builds** — arriving for people who will never read code. The first pillar, **the computer that understands**, is what accepts the description; the second is what authors the artifact. The spreadsheet gave its user neither: you were the parser and the compiler both. It is also why the right frame is the one Part 4 insists on: not a *no-code platform* (which still hands the user blocks to assemble) but an *agent that materializes the surface on request.*

---

## 5. The cost that relocates rather than disappears

A new phase of software development is only credible if it is honest about what it gives up, and this one gives up something real.

Mass software is bad at fitting the individual but extraordinarily good at one thing the individual cannot reproduce: **accumulating correctness.** A product used by millions over years is hardened by many eyes, surfaced edge cases, regression suites, and the slow accretion of fixes. That hardening was the *other* return on the fixed build cost — you paid once, and the whole user base debugged it for you. Software for an audience of one has no such audience. It is correct, or not, between exactly two parties: the user and the model. No one else will ever run it, so no one else will ever find its bugs.

So the cost of correctness does not vanish in the new phase. It **relocates** — from the vendor's QA organization to the trust between one user and one LLM:

```text
   mass software:        correctness amortized across millions of users and years
                         (many eyes find the bugs; you inherit the fixes)

   software for one:     correctness is between you and the model, once
                         (no other eyes; the bug ships to its only user — you)
```

The stakes are not uniform, and that is the whole design problem. A wrong movie-poster wall is harmless; you notice and shrug. But the same workspace holds a `portfolio` allocation view and, nearby, tax and recurring-bill collections — software whose arithmetic *matters*, generated by the same one-shot process, and audited by no one but the model that wrote it. This is not a new failure mode; it is the *oldest* one in end-user software, returning in a more powerful form. The spreadsheet era already taught the lesson the hard way: the danger was never the visible interface, it was the **invisible formula error** in a model no one else ever checked — the off-by-one in a cell reference that quietly corrupts a number a human then trusts. "The user never sees the code" is liberating for the subway map and quietly dangerous for the allocation chart, for exactly the same reason. Per Axbom's critique of per-user generated interfaces makes the design-side version of the point: an interface no two people share is an interface no second pair of eyes ever audits.

Appleton, whose phrase opened this essay, was equally honest about a gap on the practical side. As of 2024 she observed that LLM-built personal software was mostly frontend demos: "Connecting it to a back end would be like a whole different thing... no one knows what a database is if you don't work in software." The views in my table sit on exactly that missing back end; in MulmoClaude, the reference implementation these examples come from, the host supplies the persistence and validation, so the person describing a subway map never meets a database.

The mitigations for the correctness problem are the boring, correct ones, and they are the real frontier work of this phase — not the codegen, which is solved. Keep the durable data verifiable independent of the disposable view (the chart can be wrong; the numbers it reads must not be). Reserve human or deterministic review for the views whose output is consequential, and let the harmless ones run unaudited — the *reliability dial* that Part 6 of this series develops, applied here to the view layer. And treat regenerability itself as a safety feature: a disposable artifact that is cheap to throw away and regrow is also cheap to *distrust and replace*, which is a real advantage over precious code that institutions defend long past its correctness.

---

## 6. The broader shift

Two sentences capture the change.

The old phase of software development assumed:

```text
Build software once, for the mass, because building is expensive.
The individual gets the average; the code is the asset.
```

The new phase assumes:

```text
Build software for one, on demand, because building is nearly free.
The individual gets exactly their need; the code is disposable; intent and data are the asset.
```

For fifty years the economics of software forced every product toward the mean of its audience, and the entire craft of programming grew up around protecting an expensive, durable artifact. The collapse of the marginal cost of bespoke software removes the force and demotes the artifact. The audience of software can now be a single person; the code can be thrown away and regrown; the durable things are what the person *meant* and what they *have.* A restaurant guide drawn as a subway map is not a toy at the edge of this shift — it is the shape of the whole thing: software no market would fund, built for one person who never saw the code, kept only as long as it is useful, and regenerated the moment it is not.

The capstone of this series, Part 6, ends on *the workspace is the agent, and building software is how the agent grows.* This essay's addition is what that means for software itself: when building costs nothing, software stops being a product shipped to a market and becomes **an artifact grown for an individual** — and the discipline of the field shifts from maintaining precious code to verifying disposable code and curating the durable intent and data behind it.

---

*Elsewhere in this series: Part 3 argues that deliberately limited languages are what make AI-generated software trustworthy for someone who cannot read code; Part 4 develops the collection mechanism these views live in — schema, records, and a model as a complete application; Part 6, the capstone, follows the consequence to its end, where the workspace and the agent turn out to be the same thing.*
