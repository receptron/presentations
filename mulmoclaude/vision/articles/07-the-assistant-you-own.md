# The Assistant You Own

*A standalone essay, written alongside the six-part series "Beyond the Sea of App Icons." It distills the series' final argument for anyone deciding — soon — where their AI assistant should live.*

It is seven in the morning and my assistant has been working all night. The podcast feeds it tracks were ingested at three. A recurring bill crossed its reminder threshold at six and a bell is waiting for me. The vocabulary flashcards my daughter asked about are updated. On the train, I take out my phone and ask it something about a restaurant list it keeps for me, and it answers — not some assistant, *my* assistant, the one that knows my records because it has been accumulating them for a year.

None of this is exotic anymore. Every large technology company is now promising exactly this: an AI assistant that is with you twenty-four hours a day, knows your life, and works while you sleep. The promise is real. The question nobody puts on the slide is a housing question: **where does this assistant live, and who owns the place where it lives?**

## I was half right

For years, I argued in public that the always-on assistant should live in the cloud, not in a device. The reasoning felt airtight. An assistant that lives in your phone dies when the phone is off, vanishes when you switch phones, and can't be reached from your laptop. An assistant you can talk to from *any* device, at *any* hour, has to live somewhere that never sleeps — and "somewhere that never sleeps" meant the cloud.

I now think that argument was half right, and the half I got wrong is the half that matters.

Right: the assistant must not be trapped in a device. Any-device access and around-the-clock presence are non-negotiable — they are what makes an assistant an assistant rather than an app.

Wrong: I never asked who should own the "somewhere." I said "the cloud" the way people say "the grid," as if it were neutral infrastructure. It is not. The cloud, in every actual product offering, is a specific company's computers — and if your assistant's self lives on a company's computers, that company owns your assistant.

## What renting an assistant means

Consider what accumulates inside an assistant that is genuinely useful: a year of your conversations. Your family's schedules and your recurring bills. The small applications it has built just for you — in my case, a restaurant guide, a flashcard drill, a ledger. Its memory of how you like things done. This accumulation is precisely what makes the assistant valuable, and it is precisely what you cannot take with you when it lives on someone else's servers.

We already know what renting feels like, because we have rented software for twenty years. The redesign you didn't ask for. The feature that disappears in a pivot. The price that changes because the vendor's strategy did. The service that is simply discontinued — every longtime internet user carries the memory of some beloved product that was shut down on a schedule that had nothing to do with them. Robin Sloan, writing about the apps he builds for his own family, named the virtue that rented software can never offer: *sovereignty* — "it won't change unless we want it to."

Now raise the stakes. A discontinued photo service loses you photos. A discontinued assistant loses you *the accumulated self of the thing that organizes your life* — its memory, its apps, its knowledge of you. That is not a product you should rent.

And here is the part that is harder to say: this applies to the model companies too, not just the platform companies. It is easy to nod along when the warning names Meta or Google, whose assistant offerings are structurally cloud-resident — the memory, the learning loop, the personality all live server-side, because hosting your assistant's self *is* the business model. But an assistant whose self lives with Anthropic or OpenAI is rented all the same. I say this as someone who builds on Anthropic's models every day and expects to for years: the model vendor deserves my API calls. It should not own my assistant.

## The most important part of your AI assistant is not the AI

That sentence sounds wrong, so let me earn it.

Strip an assistant down to its parts. There is a language model — the reasoning engine. And there is everything the assistant has accumulated: your data, your records, its memory, and the suite of small applications it has grown around your life. Now ask which part is *yours*. The model is brilliant, and it is also a commodity in the making — there are several excellent ones, there will be more, they leapfrog each other every few months, and the best one for a hard question today may not be the best one for a cheap question tomorrow. You should *want* to swap models the way you change engines or electricity plans: freely, opportunistically, without ceremony.

The accumulation is the opposite. It is worthless to everyone else and irreplaceable to you. Nobody else's assistant knows that the rent recurs on the tenth, that your restaurant list is organized by train line, that "the usual summary" means three paragraphs with the numbers up front. A year of that cannot be re-bought at any price; it can only be re-lived.

**The most important part of your AI assistant is not the AI.** It is the accumulated data and the collection of applications built for exactly you — and the model should be the interchangeable part, never the part that holds your accumulation hostage.

This inverts how the industry frames the choice. Every provider markets the model ("ours is smarter") precisely because the model is the part *they* own. The accumulation — the part *you* should own — is quietly stored where leaving means losing it. The ownership test is simple: **could you switch models tomorrow and keep your assistant? Could you move your assistant and keep its memory?** If either answer is no, you don't own an assistant. You have a subscription to one.

## The third place

So the device is wrong and the provider's cloud is wrong. What's left sounds almost quaint: your own computer.

An always-on PC at home runs the assistant twenty-four hours a day. Its entire self — memory, records, the apps it built, its configuration — is a directory of files on a disk you own. Your phone and your laptop stop being where the assistant lives and become thin windows into the assistant at home. The cloud still matters, but its role shrinks to the part that should be rented: the model, called as a service, swappable at will. Your own PC becomes your personal cloud.

For years the obvious objection was remote access, and it deserved to be treated as the hard problem, because a home machine opened to the internet is a burglary invitation. The answer, it turns out, is architecture rather than bravado: the phone never connects to the PC at all. Both sides talk through a relay — the phone drops a request into a queue that only you can read; the home machine, holding rights to nothing beyond your own data, picks it up, does the work, and posts the result back. The house only dials out; there is no open port, no public address, nothing to scan. And because the queue is durable, you can ask while the PC sleeps — it answers the moment it wakes. An imperfectly always-on machine still behaves like a continuous assistant.

I should be honest about the residue: the requests and replies do transit a relay running on someone's cloud. The assistant's self stays home; its errands travel. And self-hosting is not yet for everyone — someone must keep the machine updated and the disk backed up, and today that someone is a tinkerer. Closing that gap, making the owned assistant as effortless as the rented one, is in my view one of the genuinely important product problems of the next few years. But note what kind of problem it is: an engineering problem. Capture, by contrast, is a business model — the vendor cannot patch it away, because it is the point.

One more piece will come home eventually. Today the model is the part I still rent — contentedly, because it is the swappable part. But model compute is walking a road computing itself has walked before. Andrej Karpathy compares today's LLMs to the 1960s, when computers were so expensive that everyone time-shared a distant mainframe; that era ended in the most literal way possible — the computer became *personal*. Capable open models already run on consumer hardware, and mid-sized ones already handle the structured, tool-calling work an assistant does all day. There is no hurry, and the architecture doesn't care: when the day comes, nothing changes but an API endpoint pointing home instead of out. The last rented part of the assistant comes home, and the sovereignty is complete.

## Where I am testing this

MulmoClaude, the open-source agent I have been building, runs on my own PC and is my working answer to this essay. Its self is files: the memory, the collection schemas, the small apps it has authored for me. The model behind it is called over an API and is deliberately replaceable — the day a better one appears, the assistant keeps every memory and every app and simply thinks with a new engine. And with remote access from my phone finally working, it has crossed the threshold that matters: it is becoming the assistant I argued for all those years — always on, reachable from anywhere — just not living where I originally said it would.

The architecture that makes this possible — why an assistant can *be* a directory of files, how its applications are grown rather than installed, what keeps the generated parts trustworthy — is the subject of my six-part series, "Beyond the Sea of App Icons," and especially its conclusion, *The Workspace Is the Agent*. This essay is the short version of its last argument, the one I'd make to anyone about to choose an assistant: the model is the engine, and engines are for swapping. Make sure the part that accumulates — the part that becomes, over the years, a second self — accumulates on a disk that belongs to you.
