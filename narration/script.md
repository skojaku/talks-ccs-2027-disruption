# Narration script (ccs-2027, ~15 min)
Each block: slide number, start time in the Kokoro movie, then the spoken text. Generated from `narration/script.py`.

## Slide 1  [0:00]

Hello everyone, I'm Sadamori Kojaku. Today I'll talk about a paper with Munjung Kim and Yong-Yeol Ahn, published in Science Advances. It is about how we measure whether a scientific paper is disruptive, and what happens when the standard measure breaks down. Before I begin, a quick note on what to expect. We will start with a question, how do we measure novelty, then see where a popular measure fails, then see how embeddings fix it, and finish with an open problem.

## Slide 2  [0:28]

Let me start with a movie. In 1989, Back to the Future Part Two imagined the year 2015. Smart glasses, video calls, flat screens. And today, we really do live in the future we once imagined.

## Slide 3  [0:43]

So let me ask you: what is the most memorable technology in your life? A shift, or a new technology. For many of us, it is the web.

## Slide 4  [0:52]

Maybe the smartphone.

## Slide 5  [0:54]

Maybe the three-D printer.

## Slide 6  [0:56]

Or, very recently, ChatGPT.

## Slide 7  [0:59]

But there is an older one that changed everything: the light bulb.

## Slide 8  [1:03]

The light bulb changed the human world more than you would think. People gained four to six more hours a day. It created the twenty-four-hour economy, and an evening entertainment culture. It is a good example of a technology that did not just add a tool, but changed the rhythm of society.

## Slide 9  [1:21]

Technologies keep arriving, and each one reshapes how we live.

## Slide 10  [1:25]

Douglas Adams described how we react to them. Anything that is in the world when you're born is normal and ordinary. It is just a natural part of the way the world works.

## Slide 11  [1:36]

Anything invented between when you are fifteen and thirty-five is new and exciting and revolutionary. You might even get a career in it.

## Slide 12  [1:45]

And anything invented after you are thirty-five is against the natural order of things.

## Slide 13  [1:51]

Let me test this on myself. Here is a timeline of my age.

## Slide 14  [1:55]

When I was six, pagers were everywhere. They were normal.

## Slide 15  [1:59]

At twelve, wireless phones arrived. That was innovative.

## Slide 16  [2:02]

At nineteen, the smartphone. Super cool.

## Slide 17  [2:05]

And now I'm thirty-six, and smart glasses feel like they go against the natural order. So Adams was right about me. The point is that our sense of what is new depends on when we happen to be born.

## Slide 18  [2:18]

Look at how phones changed around the turning point of my life, from the old Nokia to flip phones, to the iPhone. Each was a big shift.

## Slide 19  [2:27]

This is not just about gadgets. Science changes this way too. Bohr's atomic model in 1913, Vegard's in 1918, Schrödinger's in 1926. Each one changed how we see the atom. Disruption is a general feature of how knowledge advances. But can we measure it?

## Slide 20  [2:49]

So here is the question of this talk. How do we quantify disruptiveness? What does it mean for a paper to be disruptive, and can we put a number on it?

## Slide 21  [2:58]

A popular answer uses citation networks. It is the disruption index, proposed by Funk and Owen-Smith. A paper that is developing builds on earlier work, and is cited together with it. A disruptive paper is cited alone, without the work before it. The index runs from minus one, developing, to one, disruptive.

## Slide 22  [3:20]

Here is how it works. Take a focal paper, the diamond. Some later papers cite both the focal paper and its references. Some cite only the focal paper. And some cite only the references.

## Slide 23  [3:33]

We sort the citing papers into three classes. Cites the focal paper and its references. Cites only the focal paper. Or cites only the references.

## Slide 24  [3:43]

The D-index is the number citing only the focal paper, minus the number citing both, divided by the total. So D is close to one when most citing papers ignore the earlier work, and close to minus one when they cite it together.

## Slide 25  [3:58]

This index has been used widely, and it gave striking results. Large teams develop, small teams disrupt.

## Slide 26  [4:06]

Papers are becoming less disruptive over time.

## Slide 27  [4:09]

And remote collaboration produces fewer breakthrough ideas. All of these appeared in Nature.

## Slide 28  [4:15]

But the D-index fails for some well-known disruptive discoveries. This matters, because the measure is used to make claims about science as a whole. If it misses landmark discoveries, we should worry.

## Slide 29  [4:29]

Take the Higgs mechanism. In 1964, Englert, Brout, and Higgs predicted the Higgs boson. In 2013, they received the Nobel Prize in Physics.

## Slide 30  [4:40]

The paper by Englert and Brout has a D-index of zero point one five, in the top two point eight percent. That looks right.

## Slide 31  [4:48]

But the paper by Higgs has a D-index of minus zero point two seven. That is the bottom zero point one percent. A Nobel Prize paper, among the least disruptive papers ever. Remember, this is a landmark paper that everyone agrees was a breakthrough. If a measure cannot recognize it, we have a problem.

## Slide 32  [5:09]

What is happening?

## Slide 33  [5:11]

The Higgs paper cites the paper by Englert and Brout. That is the key. Higgs wrote his paper just after Englert and Brout, and he cited them.

## Slide 34  [5:20]

Let's cut this single citation.

## Slide 35  [5:22]

Now look at these four papers. They cite both Higgs and Englert and Brout. Following the decision tree, they are in the class that cites the focal paper and its references.

## Slide 36  [5:34]

Without the citation, they move to a different class: they now cite only the focal paper.

## Slide 37  [5:39]

The D-index jumps from minus zero point two seven to zero point two eight. From the bottom zero point one percent to the top one point three percent. The citation structure is almost the same, and yet the verdict is completely different.

## Slide 38  [5:55]

So why is the D-index so sensitive? With the citation, minus zero point two seven. With one citation cut, zero point two eight. A single edge flips the score. This is a sign that the measure is fragile around exactly the cases we care about.

## Slide 39  [6:13]

The reason is that the D-index sorts each citing paper into a class. Does the paper build on the focal paper, on the work before it, or on both?

## Slide 40  [6:22]

But papers do not sort so cleanly. Some belong to two groups at once. A paper can build on the focal paper and on its references at the same time. Rounding that into one class throws away information.

## Slide 41  [6:36]

Our idea is simple. We preserve continuity by abandoning class rounding. Instead of putting papers into boxes, we want a continuous picture.

## Slide 42  [6:47]

To do that, we simulate the flow of knowledge with random walks on the citation network.

## Slide 43  [6:52]

A walker moves along citations, from paper to paper.

## Slide 44  [6:56]

Each walk gives us a sequence of papers.

## Slide 45  [6:59]

We then feed pairs of papers, an ancestor and a descendant, to word2vec. You can think of word2vec as an information compressor that gives each node a coordinate. And the coordinates will be arranged so that papers that are related are close to each other.

## Slide 46  [7:16]

Let me quickly explain how word2vec works. It is a small neural network. I will not go into the details, but I want you to see the key idea, because it is the heart of our measure.

## Slide 47  [7:28]

Take the sentence: chance favors only the prepared mind. We look at one word and its neighbor.

## Slide 48  [7:34]

The input is the word favors.

## Slide 49  [7:36]

And the network should predict the nearby word, prepared.

## Slide 50  [7:39]

That is the whole task.

## Slide 51  [7:41]

Inside the network, the word favors is turned into a vector. We call it the query vector.

## Slide 52  [7:47]

The word prepared also has a vector, which we call the key vector.

## Slide 53  [7:51]

So every word has two vectors, a query and a key. This is a small detail, but it is the one that matters most for what follows.

## Slide 54  [8:00]

How is it trained? By negation. We contrast real pairs with fake ones.

## Slide 55  [8:05]

A real pair, favors as query and prepared as key, is pulled together.

## Slide 56  [8:10]

Then we sample a random word, like water, as a fake partner.

## Slide 57  [8:14]

And that pair is pushed apart.

## Slide 58  [8:16]

In a table: favors and prepared is genuine, label one. Favors and water is not, label zero.

## Slide 59  [8:23]

This is just logistic regression on the dot product between a query and a key. We train it by maximizing the likelihood. Nothing exotic here. It is a very simple classifier, and the embedding is a by-product of training it.

## Slide 60  [8:38]

So word2vec turns pairs into coordinates.

## Slide 61  [8:42]

Back to the citation network. The random walk gives us parent and child, grandparent and grandchild pairs.

## Slide 62  [8:49]

We slide along the walk.

## Slide 63  [8:51]

And collect more pairs.

## Slide 64  [8:53]

Again.

## Slide 65  [8:54]

Until the walk ends.

## Slide 66  [8:56]

We repeat this many times, and obtain a large amount of training data.

## Slide 67  [9:01]

Now let's focus on one paper. Only pairs involving this paper matter for it. The other pairs are irrelevant to the focal paper.

## Slide 68  [9:10]

Pairs of a query and a key get closer in the embedding space. Think of it as a tug of war, where every real pair pulls its two members toward each other.

## Slide 69  [9:20]

So the focal paper is pulled toward its neighbors from both sides.

## Slide 70  [9:24]

The focal paper sits between the papers that cite it and the papers that it cites.

## Slide 71  [9:29]

The focal paper ends up with two points: a key vector, and a query vector.

## Slide 72  [9:34]

If the citing and cited papers are not mixed, the key and the query are far apart. That is a discontinuity. If they are mixed, the key and the query sit close together. So the distance between the key and the query of one paper tells us how mixed its neighborhood is.

## Slide 73  [9:52]

We define the Embedding Disruptiveness Measure, or EDM, as one minus the cosine similarity between the query and the key. It tells how different the two sides are. For Englert and Brout and for Higgs, EDM is about one point zero, in the top four percent. Both are recognized as disruptive. The idea is that a disruptive paper sits between two groups that do not talk to each other, and an embedding makes this visible as a gap.

## Slide 74  [10:20]

Does EDM beat the D-index? We tested it with data from the American Physical Society, using the milestone papers selected by the editors of Physical Review Letters.

## Slide 75  [10:31]

First, a null model. We randomize the network while preserving the degrees and the time gaps, and shuffle everything else. This is important, because a citation count alone can make a paper look disruptive. We want to know if the measure captures something more than that.

## Slide 76  [10:48]

Here is the D-index of the milestone papers. Most are high, but there is a group at the bottom.

## Slide 77  [10:54]

These are milestone papers with a bottom-level D-index.

## Slide 78  [10:58]

And shuffling the network creates even more works with a high D-index. So part of a high D-index is explained by degrees and time gaps alone. That is a worrying sign for the D-index, because it means the measure partly reflects the structure of the network, not the quality of the work.

## Slide 79  [11:17]

Now EDM.

## Slide 80  [11:18]

Many milestone papers have a high EDM value.

## Slide 81  [11:22]

And randomization reduces the EDM score for most works. So EDM captures something beyond what degrees and time gaps explain. That is what we want from a measure of disruptiveness.

## Slide 82  [11:35]

Finally, a regression against human judgment. The odds ratio for the EDM percentile is one point two three, and significant. For the D-index it is one point oh three, which is not. EDM aligns better with human judgment. So the measure that keeps continuity is also closer to how experts judge papers.

## Slide 83  [11:56]

Let me summarize.

## Slide 84  [11:58]

First, the D-index fails on well-known discoveries. Higgs has a D of minus zero point two seven. That was the starting point.

## Slide 85  [12:07]

Second, EDM keeps continuity. A large gap between query and key marks a discontinuity.

## Slide 86  [12:14]

And third, EDM matches human judgment. In the paper we also show results on patents, with the same message.

## Slide 87  [12:23]

Now I'd like to end with an open problem: simultaneous discovery.

## Slide 88  [12:28]

Here are Higgs, and Englert and Brout again. There are many other cases like this one. This is a simultaneous discovery, and the two sides shared the Nobel Prize. Think about it for a moment. If two groups independently discover the same thing, and one cites the other, the D-index can punish both. That is a systematic blind spot.

## Slide 89  [12:49]

When we look at their papers in the embedding space, they sit very close to each other. In our data, we found eighteen thousand candidate pairs. We checked eighty highly cited ones, and sixty-four were real simultaneous discoveries. Simultaneous discoveries sit side by side.

## Slide 90  [13:08]

And this is not a random accident scattered everywhere. It suggests the environment is ripe. The time was ready for the idea. The D-index tends to overlook these papers, but embeddings make these local bursts visible. Maybe science is not about lone geniuses waiting for lightning to strike. It may be that the environment makes certain ideas ready to be found.

## Slide 91  [13:31]

Robert Merton argued that independent multiple discoveries are the dominant pattern in science, and that it is the singletons that need a special explanation. Embeddings give us a way to see when and where an idea becomes ripe.

## Slide 92  [13:46]

The method is not limited to papers. It applies to any directed network. Legal documents, where court decisions cite earlier ones. Patents, which we have partly done. And traffic networks, where we can ask where the bottlenecks are. Anywhere you have items that point to earlier items, you can ask which ones are bridges and which ones are developments.

## Slide 93  [14:08]

And we are now asking whether text embeddings also have this bottleneck structure. We are looking into it. If you are interested, please get in touch. That would be a different kind of data, but the same question: where are the discontinuities?

## Slide 94  [14:23]

Finally, an announcement. CompleNet 2027 will be held in Rochester, New York, March ninth to twelfth. I am a program chair, so please join us. You can scan the QR code to read the paper, and reach me through my website, Bluesky, or email. Thank you very much.
