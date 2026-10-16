# Narration script (Kokoro, af_heart, 0.96x)

| # | start | text |
|---|---|---|
| 1 | 0:00 | Hello everyone, I'm Sadamori Kojaku. Today I'll talk about a paper with Munjung Kim and Yong-Yeol Ahn, published in Science Advances. It is about how we measure whether a scientific paper is disruptive, and what happens when the standard measure breaks down. Before I begin, a quick note on what to expect. We will start with a question, how do we measure novelty, then see where a popular measure fails, then see how embeddings fix it, and finish with an open problem. |
| 2 | 0:28 | Let me start with a movie. In 1989, Back to the Future Part Two imagined the year 2015. Smart glasses, video calls, flat screens. And today, we really do live in the future we once imagined. |
| 3 | 0:43 | So let me ask you: what is the most memorable technology in your life? A shift, or a new technology. |
| 4 | 0:50 | For many of us, it is the web. |
| 5 | 0:52 | Maybe the smartphone. |
| 6 | 0:54 | Maybe the three-D printer. |
| 7 | 0:56 | Or, very recently, ChatGPT. |
| 8 | 0:59 | But there is an older one that changed everything: the light bulb. |
| 9 | 1:03 | The light bulb changed the human world more than you would think. People gained four to six more hours a day. It created the twenty-four-hour economy, and an evening entertainment culture. It is a good example of a technology that did not just add a tool, but changed the rhythm of society. |
| 10 | 1:22 | Technologies keep arriving, and each one reshapes how we live. |
| 11 | 1:26 | Douglas Adams described how we react to them. Anything that is in the world when you're born is normal and ordinary. It is just a natural part of the way the world works. |
| 12 | 1:37 | Anything invented between when you are fifteen and thirty-five is new and exciting and revolutionary. You might even get a career in it. |
| 13 | 1:45 | And anything invented after you are thirty-five is against the natural order of things. |
| 14 | 1:51 | Let me test this on myself. Here is a timeline of my age. |
| 15 | 1:55 | When I was six, pagers were everywhere. They were normal. |
| 16 | 1:59 | At twelve, wireless phones arrived. That was innovative. |
| 17 | 2:03 | At nineteen, the smartphone. Super cool. |
| 18 | 2:06 | And now I'm thirty-six, and smart glasses feel like they go against the natural order. So Adams was right about me. The point is that our sense of what is new depends on when we happen to be born. |
| 19 | 2:19 | Look at how phones changed around the turning point of my life, from the old Nokia to flip phones, to the iPhone. Each was a big shift. |
| 20 | 2:28 | This is not just about gadgets. Science changes this way too. Bohr's atomic model in 1913, Vegard's in 1918, Schrödinger's in 1926. Each one changed how we see the atom. Disruption is a general feature of how knowledge advances. But can we measure it? |
| 21 | 2:49 | So here is the question of this talk. How do we quantify disruptiveness? What does it mean for a paper to be disruptive, and can we put a number on it? |
| 22 | 2:59 | A popular answer uses citation networks. It is the disruption index, proposed by Funk and Owen-Smith. A paper that is developing builds on earlier work, and is cited together with it. A disruptive paper is cited alone, without the work before it. The index runs from minus one, developing, to one, disruptive. |
| 23 | 3:20 | Here is how it works. Take a focal paper, the diamond. Some later papers cite both the focal paper and its references. Some cite only the focal paper. And some cite only the references. |
| 24 | 3:33 | We sort the citing papers into three classes. Cites the focal paper and its references. Cites only the focal paper. Or cites only the references. |
| 25 | 3:44 | The D-index is the number citing only the focal paper, minus the number citing both, divided by the total. So D is close to one when most citing papers ignore the earlier work, and close to minus one when they cite it together. |
| 26 | 3:59 | This index has been used widely, and it gave striking results. Large teams develop, small teams disrupt. |
| 27 | 4:06 | Papers are becoming less disruptive over time. |
| 28 | 4:10 | And remote collaboration produces fewer breakthrough ideas. All of these appeared in Nature. |
| 29 | 4:15 | But the D-index fails for some well-known disruptive discoveries. This matters, because the measure is used to make claims about science as a whole. If it misses landmark discoveries, we should worry. |
| 30 | 4:29 | Take the Higgs mechanism. In 1964, Englert, Brout, and Higgs predicted the Higgs boson. In 2013, they received the Nobel Prize in Physics. |
| 31 | 4:41 | The paper by Englert and Brout has a D-index of zero point one five, in the top two point eight percent. That looks right. |
| 32 | 4:49 | But the paper by Higgs has a D-index of minus zero point two seven. That is the bottom zero point one percent. A Nobel Prize paper, among the least disruptive papers ever. Remember, this is a landmark paper that everyone agrees was a breakthrough. If a measure cannot recognize it, we have a problem. |
| 33 | 5:09 | What is happening? |
| 34 | 5:11 | Look at this small citation network. Higgs, with the ring, is the focal paper. Higgs cites the paper by Englert and Brout, so that paper is a reference of Higgs. Now sort the papers that cite them. Blue papers cite the focal paper and a reference. Red papers cite only the focal paper. Grey papers cite only the references. All three cases are here. The three papers on top are blue, because they cite both Higgs and Englert and Brout. |
| 35 | 5:37 | Now let's cut this single citation. |
| 36 | 5:40 | Now Englert and Brout is no longer a reference of Higgs. The three papers cite only the focal paper, so they turn from blue to red. Red is the good score, the disruptive side. So the D-index jumps from minus zero point two seven to zero point two eight. From the bottom zero point one percent to the top one point three percent. One citation, and the verdict is completely different. |
| 37 | 6:04 | So why is the D-index so sensitive? With the citation, minus zero point two seven. With one citation cut, zero point two eight. A single edge flips the score. This is a sign that the measure is fragile around exactly the cases we care about. |
| 38 | 6:22 | The reason is that the D-index sorts each citing paper into a class. Does the paper build on the focal paper, on the work before it, or on both? |
| 39 | 6:31 | But papers do not sort so cleanly. Some belong to two groups at once. A paper can build on the focal paper and on its references at the same time. Rounding that into one class throws away information. |
| 40 | 6:45 | Our idea is simple. We preserve continuity by abandoning class rounding. Instead of putting papers into boxes, we want a continuous picture. |
| 41 | 6:55 | To do that, we simulate the flow of knowledge with random walks on the citation network. |
| 42 | 7:01 | A walker moves along citations, from paper to paper. |
| 43 | 7:05 | Each walk gives us a sequence of papers. |
| 44 | 7:08 | We then feed pairs of papers, an ancestor and a descendant, to word2vec. You can think of word2vec as an information compressor that gives each node a coordinate. And the coordinates will be arranged so that papers that are related are close to each other. |
| 45 | 7:25 | Let me quickly explain how word2vec works. It is a small neural network. I will not go into the details, but I want you to see the key idea, because it is the heart of our measure. |
| 46 | 7:37 | Take the sentence: chance favors only the prepared mind. We look at one word and its neighbor. |
| 47 | 7:43 | The input is the word favors. |
| 48 | 7:45 | And the network should predict the nearby word, prepared. |
| 49 | 7:48 | That is the whole task. |
| 50 | 7:50 | Inside the network, the word favors is turned into a vector. We call it the query vector. |
| 51 | 7:56 | The word prepared also has a vector, which we call the key vector. |
| 52 | 8:00 | So every word has two vectors, a query and a key. This is a small detail, but it is the one that matters most for what follows. |
| 53 | 8:09 | How is it trained? By negation. We contrast real pairs with fake ones. |
| 54 | 8:14 | A real pair, favors as query and prepared as key, is pulled together. |
| 55 | 8:19 | Then we sample a random word, like water, as a fake partner. |
| 56 | 8:23 | And that pair is pushed apart. |
| 57 | 8:25 | In a table: favors and prepared is genuine, label one. Favors and water is not, label zero. |
| 58 | 8:32 | This is just logistic regression on the dot product between a query and a key. We train it by maximizing the likelihood. Nothing exotic here. It is a very simple classifier, and the embedding is a by-product of training it. |
| 59 | 8:47 | So word2vec turns pairs into coordinates. |
| 60 | 8:50 | Back to the citation network. The random walk gives us parent and child, grandparent and grandchild pairs. |
| 61 | 8:58 | We slide along the walk. |
| 62 | 9:00 | And collect more pairs. |
| 63 | 9:02 | Again. |
| 64 | 9:03 | Until the walk ends. |
| 65 | 9:05 | We repeat this many times, and obtain a large amount of training data. |
| 66 | 9:10 | Now let's focus on one paper. Only pairs involving this paper matter for it. The other pairs are irrelevant to the focal paper. |
| 67 | 9:18 | Pairs of a query and a key get closer in the embedding space. Think of it as a tug of war, where every real pair pulls its two members toward each other. |
| 68 | 9:29 | So the focal paper is pulled toward its neighbors from both sides. |
| 69 | 9:33 | The focal paper sits between the papers that cite it and the papers that it cites. |
| 70 | 9:38 | The focal paper ends up with two points: a key vector, and a query vector. |
| 71 | 9:43 | If the citing and cited papers are not mixed, the key and the query are far apart. That is a discontinuity. If they are mixed, the key and the query sit close together. So the distance between the key and the query of one paper tells us how mixed its neighborhood is. |
| 72 | 10:01 | We define the Embedding Disruptiveness Measure, or EDM, as one minus the cosine similarity between the query and the key. It tells how different the two sides are. For Englert and Brout and for Higgs, EDM is about one point zero, in the top four percent. Both are recognized as disruptive. The idea is that a disruptive paper sits between two groups that do not talk to each other, and an embedding makes this visible as a gap. |
| 73 | 10:28 | Does EDM beat the D-index? We tested it with data from the American Physical Society, using the milestone papers selected by the editors of Physical Review Letters. |
| 74 | 10:40 | First, a null model. We randomize the network while preserving the degrees and the time gaps, and shuffle everything else. This is important, because a citation count alone can make a paper look disruptive. We want to know if the measure captures something more than that. |
| 75 | 10:57 | Here is the D-index of the milestone papers. Most are high, but there is a group at the bottom. |
| 76 | 11:03 | These are milestone papers with a bottom-level D-index. |
| 77 | 11:07 | And shuffling the network creates even more works with a high D-index. So part of a high D-index is explained by degrees and time gaps alone. That is a worrying sign for the D-index, because it means the measure partly reflects the structure of the network, not the quality of the work. |
| 78 | 11:26 | Now EDM. |
| 79 | 11:27 | Many milestone papers have a high EDM value. |
| 80 | 11:31 | And randomization reduces the EDM score for most works. So EDM captures something beyond what degrees and time gaps explain. That is what we want from a measure of disruptiveness. |
| 81 | 11:44 | Finally, a regression against human judgment. The odds ratio for the EDM percentile is one point two three, and significant. For the D-index it is one point oh three, which is not. EDM aligns better with human judgment. So the measure that keeps continuity is also closer to how experts judge papers. |
| 82 | 12:05 | So which disruptive works does EDM find that the D-index misses? Let's look at the answer. |
| 83 | 12:11 | Take the Higgs mechanism again. Englert and Brout have a D-index of zero point one five, in the top two point eight percent. Higgs has minus zero point two seven, in the bottom zero point one percent. With EDM, both papers get a score above one, in the top four or five percent. The same discovery now gets the same verdict. |
| 84 | 12:33 | Another case is the J over psi meson. In 1974, two teams, led by Richter and Ting, announced the same particle independently, and the two papers cited each other. Because of those citations, the D-index puts both papers at the bottom, around minus zero point one and minus zero point six. EDM scores them zero point nine nine and zero point nine seven, in the top five and seven percent. |
| 85 | 13:01 | This is not only two cases. EDM finds many more simultaneous discoveries, such as asymptotic freedom, the new quark, and reverse transcriptase. In every pair, the D-index is near the developing end and EDM is near the disruptive end. |
| 86 | 13:17 | When we look at these papers in the embedding space, they sit very close to each other. In our data, we found eighteen thousand candidate pairs. We checked eighty highly cited ones, and sixty-four were real simultaneous discoveries. Simultaneous discoveries sit side by side. |
| 87 | 13:36 | Robert Merton argued that independent multiple discoveries are the dominant pattern in science, and that it is the singletons that need a special explanation. Embeddings give us a way to see when and where an idea becomes ripe. |
| 88 | 13:52 | Let me summarize. |
| 89 | 13:54 | First, the D-index fails on well-known discoveries. Higgs has a D of minus zero point two seven. That was the starting point. |
| 90 | 14:03 | Second, EDM keeps continuity. A large gap between query and key marks a discontinuity. |
| 91 | 14:10 | And third, EDM matches human judgment. In the paper we also show results on patents, with the same message. |
| 92 | 14:18 | And fourth, EDM finds simultaneous discoveries. The papers of one discovery sit side by side in the embedding space, while the D-index overlooks them. |
| 93 | 14:29 | As future work, we would like to quantify the same thing elsewhere: legal documents and patents, mobility networks, and other embeddings such as text. Anywhere items point to earlier items, we can ask where the discontinuities are. |
| 94 | 14:44 | Finally, an announcement. CompleNet 2027 will be held in Rochester, New York, March ninth to twelfth. I am a program chair, so please join us. You can scan the QR code to read the paper, and reach me through my website, Bluesky, or email. Thank you very much. |
