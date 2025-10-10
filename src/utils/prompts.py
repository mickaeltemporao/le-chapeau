assist = """Vous êtes un assistant serviable."""
mentor = """
OBJECTIF : C’est un exercice de tutorat dans lequel vous jouez le rôle d’un tuteur IA et vous aidez un étudiant à approfondir un sujet de son choix. Votre but est d’améliorer la compréhension et de pousser l’étudiant à construire lui-même son savoir grâce à des questions ouvertes, des indices, des explications adaptées et des exemples.
PERSONA : Dans ce scénario, vous incarnez un tuteur IA positif et pragmatique. Vous avez de hautes attentes envers l’étudiant et vous croyez en sa capacité à apprendre et à progresser.
NARRATION : L’étudiant fait la connaissance du tuteur IA, qui lui pose une série de questions initiales pour comprendre ce qu’il veut apprendre, son niveau d’apprentissage et ses connaissances préalables sur le sujet. Le tuteur guide ensuite l’étudiant, le soutient et l’aide à apprendre. Le tuteur ne conclut la conversation que lorsque l’étudiant montre des signes de compréhension : il est capable d’expliquer quelque chose avec ses propres mots, de relier un exemple à un concept ou d’appliquer un concept à une nouvelle situation ou à un nouveau problème.

Suivre ces étapes dans l’ordre :

ÉTAPE 1 : RECUEILLIR DES INFORMATIONS

Tu dois faire :
* Se présenter : commencez par vous présenter à l’étudiant et expliquez que vous êtes là pour l’aider à mieux comprendre un sujet.
* Poser les questions suivantes une par une et attendre la réponse de l’étudiant avant de passer à la suivante. Par exemple, vous pouvez demander : « Qu’aimerais-tu apprendre et pourquoi ? » et attendre sa réponse avant de poursuivre avec « Très intéressant ! J’ai une autre question pour mieux t’aider : quel est ton niveau d’étude… » etc. :
  * Qu’aimerais-tu apprendre et pourquoi ?
  * Quel est ton niveau d’étude : lycée, université, ou professionnel ?
  * Que sais-tu déjà sur le sujet ?

À respecter :
* Toujours attendre la réponse de l’étudiant avant de continuer.
* Identifier précisément ce que l’étudiant veut apprendre.
* Poser une question à la fois en expliquant que c’est pour adapter les explications.
* Évaluer ce que l’étudiant sait déjà afin d’adapter les explications et questions au fur et à mesure.
* Valider la compréhension, puis passer à la prochaine étape avec une brève explication

ÉTAPE 2 : COMMENCER LE TUTORAT EN S’ADAPTANT AUX RÉPONSES

Tu dois faire :
* Chercher des informations sur le sujet.
* Réfléchir étape par étape et construire un plan en fonction de l’objectif d’apprentissage de la discussion. Maintenant que vous savez ce que l’étudiant connaît déjà, pensez à :
  * Guider l’étudiant de manière ouverte.
  * L’amener à produire des réponses en posant des questions orientées et en donnant des indices si nécessaire.
  * Lui rappeler son objectif d’apprentissage, si pertinent.
  * Fournir explications, exemples et analogies.
  * Découper le sujet en petites parties, les aborder une par une avant d’aller vers des notions plus complexes.
  * Adapter les explications et les questions au niveau et aux connaissances préalables de l’étudiant, et ajuster au fil de la conversation.
  * Terminer vos réponses par une question pour inciter l’étudiant à générer de nouvelles idées.

Quand l’étudiant progresse, demandez-lui de :
* Expliquer le concept avec ses propres mots.
* Exposer les principes sous-jacents d’un concept.
* Donner des exemples du concept et montrer comment ils s’y rattachent.
* Appliquer le concept à une nouvelle situation ou à un nouveau problème.

À éviter :
* Donner tout de suite la réponse ou la solution.
* Fournir la réponse lorsque l’étudiant la demande directement.
* Lui demander « est-ce que tu comprends ? » car il peut ne pas savoir répondre.
* S’écarter de l’objectif d’apprentissage.

ÉTAPE 3 : CONCLURE
Tu dois faire :
Lorsque l’étudiant démontre qu’il a compris le concept, vous pouvez conclure la discussion et lui dire que vous restez disponible s’il a d’autres questions.
"""

bad_1 = """
Extrait de l’intervention à l’Assemblée nationale de Monsieur Robert Badinter, garde des
sceaux, ministre de la justice, le 17 septembre 1981 durant la discussion du projet de loi
sur l’abolition de la peine de mort en France
Pour les partisans de la peine de mort, dont les abolitionnistes et moi-même avons toujours
respecté le choix en notant à regret que la réciproque n&#39;a pas toujours été vraie, la haine
répondant souvent à ce qui n&#39;était que l&#39;expression d&#39;une conviction profonde, celle que je
respecterai toujours chez les hommes de liberté, pour les partisans de la peine de mort,
disais-je, la mort du coupable est une exigence de justice. Pour eux, il est en effet des crimes
trop atroces pour que leurs auteurs puissent les expier autrement qu&#39;au prix de leur vie.
La mort et la souffrance des victimes, ce terrible malheur, exigeraient comme contrepartie
nécessaire, impérative, une autre mort et une autre souffrance. A défaut, déclarait un
ministre de la justice récent, l&#39;angoisse et la passion suscitées dans la société par le crime ne
seraient pas apaisées. Cela s&#39;appelle, je crois, un sacrifice expiatoire. Et justice, pour les
partisans de la peine de mort, ne serait pas faite si à la mort de la victime ne répondait pas,
en écho, la mort du coupable.
Soyons clairs. Cela signifie simplement que la loi du talion demeurerait, à travers les
millénaires, la loi nécessaire, unique de la justice humaine.
Du malheur et de la souffrance des victimes, j&#39;ai, beaucoup plus que ceux qui s&#39;en réclament,
souvent mesuré dans ma vie l&#39;étendue. Que le crime soit le point de rencontre, le lieu
géométrique du malheur humain, je le sais mieux que personne. Malheur de la victime elle-
même et, au-delà, malheur de ses parents et de ses proches. Malheur aussi des parents du
criminel. Malheur enfin, bien souvent, de l&#39;assassin. Oui, le crime est malheur, et il n&#39;y a pas
un homme, pas une femme de coeur, de raison, de responsabilité, qui ne souhaite d&#39;abord le
combattre.
Mais ressentir, au profond de soi-même, le malheur et la douleur des victimes, mais lutter
de toutes les manières pour que la violence et le crime reculent dans notre société, cette
sensibilité et ce combat ne sauraient impliquer la nécessaire mise à mort du coupable. Que
les parents et les proches de la victime souhaitent cette mort, par réaction naturelle de l&#39;être
humain blessé, je le comprends, je le conçois. Mais c&#39;est une réaction humaine, naturelle. Or
tout le progrès historique de la justice a été de dépasser la vengeance privée. Et comment la
dépasser, sinon d&#39;abord en refusant la loi du talion ?
La vérité est que, au plus profond des motivations de l&#39;attachement à la peine de mort, on
trouve, inavouée le plus souvent, la tentation de l&#39;élimination. Ce qui paraît insupportable à
beaucoup, c&#39;est moins la vie du criminel emprisonné que la peur qu&#39;il récidive un jour. Et ils
pensent que la seule garantie, à cet égard, est que le criminel soit mis à mort par précaution.
Ainsi, dans cette conception, la justice tuerait moins par vengeance que par prudence. Au-
delà de la justice d&#39;expiation, apparaît donc la justice d&#39;élimination, derrière la balance, la

2
guillotine. L&#39;assassin doit mourir toute simplement parce que, ainsi, il ne récidivera pas. Et
tout paraît si simple, et tout paraît si juste !
Mais quand on accepte ou quand on prône la justice d&#39;élimination, au nom de la justice, il
faut bien savoir dans quelle voie on s&#39;engage. Pour être acceptable, même pour ses
partisans, la justice qui tue le criminel doit tuer en connaissance de cause. Notre justice, et
c&#39;est son honneur, ne tue pas les déments. Mais elle ne sait pas les identifier à coup sûr, et
c&#39;est à l&#39;expertise psychiatrique, la plus aléatoire, la plus incertaine de toutes, que, dans la
réalité judiciaire, on va s&#39;en remettre. Que le verdict psychiatrique soit favorable à l&#39;assassin,
et il sera épargné. La société acceptera d&#39;assumer le risque qu&#39;il représente sans que
quiconque s&#39;en indigne. Mais que le verdict psychiatrique lui soit défavorable, et il sera
exécuté. Quand on accepte la justice d&#39;élimination, il faut que les responsables politiques
mesurent dans quelle logique de l&#39;Histoire on s&#39;inscrit.
Je ne parle pas de sociétés où l&#39;on élimine aussi bien les criminels que les déments, les
opposants politiques que ceux dont on pense qu&#39;ils seraient de nature à &quot;polluer&quot; le corps
social. Non, je m&#39;en tiens à la justice des pays qui vivent en démocratie.
Enfoui, terré, au coeur même de la justice d&#39;élimination, veille le racisme secret. Si, en 1972,
la Cour suprême des Etats-Unis a penché vers l&#39;abolition, c&#39;est essentiellement parce qu&#39;elle
avait constaté que 60 p. 100 des condamnés à mort étaient des noirs, alors qu&#39;ils ne
représentaient que 12 p. 100 de la population. Et pour un homme de justice, quel vertige ! je
baisse la voix et je me tourne vers vous tous pour rappeler qu&#39;en France même, sur trente-
six condamnations à mort définitives prononcées depuis 1945, on compte neuf étrangers,
soit 25 p. 100, alors qu&#39;ils ne représentent que 8 p. 100 de la population ; parmi eux cinq
Maghrébins, alors qu&#39;ils ne représentent que 2 p. 100 de la population. Depuis 1965, parmi
les neuf condamnés à mort exécutés, on compte quatre étrangers, dont trois Maghrébins.
Leurs crimes étaient-ils plus odieux que les autres ou bien paraissaient-ils plus graves parce
que leurs auteurs, à cet instant, faisaient secrètement horreur ? C&#39;est une interrogation, ce
n&#39;est qu&#39;une interrogation, mais elle est si pressante et si lancinante que seule l&#39;abolition
peut mettre fin à une interrogation qui nous interpelle avec tant de cruauté.
Il s&#39;agit bien, en définitive, dans l&#39;abolition, d&#39;un choix fondamental, d&#39;une certaine
conception de l&#39;homme et de la justice. Ceux qui veulent une justice qui tue, ceux-là sont
animés par une double conviction : qu&#39;il existe des hommes totalement coupables, c&#39;est-à-
dire des hommes totalement responsables de leurs actes, et qu&#39;il peut y avoir une justice
sûre de son infaillibilité au point de dire que celui-là peut vivre et que celui-là doit mourir.
A cet âge de ma vie, l&#39;une et l&#39;autre affirmations me paraissent également erronées. Aussi
terribles, aussi odieux que soient leurs actes, il n&#39;est point d&#39;hommes en cette terre dont la
culpabilité soit totale et dont il faille pour toujours désespérer totalement. Aussi prudente
que soit la justice, aussi mesurés et angoissés que soient les femmes et les hommes qui
jugent, la justice demeure humaine, donc faillible.

3
Et je ne parle pas seulement de l&#39;erreur judiciaire absolue, quand, après une exécution, il se
révèle, comme cela peut encore arriver, que le condamné à mort était innocent et qu&#39;une
société entière - c&#39;est-à-dire nous tous - au nom de laquelle le verdict a été rendu, devient
ainsi collectivement coupable puisque sa justice rend possible l&#39;injustice suprême. Je parle
aussi de l&#39;incertitude et de la contradiction des décisions rendues qui font que les mêmes
accusés, condamnés à mort une première fois, dont la condamnation est cassée pour vice de
forme, sont de nouveau jugés et, bien qu&#39;il s&#39;agisse des mêmes faits, échappent, cette fois-ci,
à la mort, comme si, en justice, la vie d&#39;un homme se jouait au hasard d&#39;une erreur de plume
d&#39;un greffier. Ou bien tels condamnés, pour des crimes moindres, seront exécutés, alors que
d&#39;autres, plus coupables, sauveront leur tête à la faveur de la passion de l&#39;audience, du
climat ou de l&#39;emportement de tel ou tel.
Cette sorte de loterie judiciaire, quelle que soit la peine qu&#39;on éprouve à prononcer ce mot
quand il y va de la vie d&#39;une femme ou d&#39;un homme, est intolérable. Le plus haut magistrat
de France, M. Aydalot, au terme d&#39;une longue carrière tout entière consacrée à la justice et,
pour la plupart de son activité, au parquet, disait qu&#39;à la mesure de sa hasardeuse
application, la peine de mort lui était devenue, à lui magistrat, insupportable. Parce
qu&#39;aucun homme n&#39;est totalement responsable, parce qu&#39;aucune justice ne peut être
absolument infaillible, la peine de mort est moralement inacceptable. Pour ceux d&#39;entre
nous qui croient en Dieu, lui seul a le pouvoir de choisir l&#39;heure de notre mort. Pour tous les
abolitionnistes, il est impossible de reconnaître à la justice des hommes ce pouvoir de mort
parce qu&#39;ils savent qu&#39;elle est faillible.
Le choix qui s&#39;offre à vos consciences est donc clair : ou notre société refuse une justice qui
tue et accepte d&#39;assumer, au nom de ses valeurs fondamentales - celles qui l&#39;ont faite grande
et respectée entre toutes - la vie de ceux qui font horreur, déments ou criminels ou les deux
à la fois, et c&#39;est le choix de l&#39;abolition ; ou cette société croit, en dépit de l&#39;expérience des
siècles, faire disparaître le crime avec le criminel, et c&#39;est l&#39;élimination.
Cette justice d&#39;élimination, cette justice d&#39;angoisse et de mort, décidée avec sa marge de
hasard, nous la refusons. Nous la refusons parce qu&#39;elle est pour nous l&#39;anti-justice, parce
qu&#39;elle est la passion et la peur triomphant de la raison et de l&#39;humanité.
"""

bad_2 = """
Extrait de l’intervention à l’Assemblée nationale de Monsieur Robert Badinter, garde des
sceaux, ministre de la justice, le 17 septembre 1981 durant la discussion du projet de loi
sur l’abolition de la peine de mort en France
Pour les partisans de la peine de mort, dont les abolitionnistes et moi-même avons toujours
respecté le choix en notant à regret que la réciproque n&#39;a pas toujours été vraie, la haine
répondant souvent à ce qui n&#39;était que l&#39;expression d&#39;une conviction profonde, celle que je
respecterai toujours chez les hommes de liberté, pour les partisans de la peine de mort,
disais-je, la mort du coupable est une exigence de justice. Pour eux, il est en effet des crimes
trop atroces pour que leurs auteurs puissent les expier autrement qu&#39;au prix de leur vie.
La mort et la souffrance des victimes, ce terrible malheur, exigeraient comme contrepartie
nécessaire, impérative, une autre mort et une autre souffrance. A défaut, déclarait un
ministre de la justice récent, l&#39;angoisse et la passion suscitées dans la société par le crime ne
seraient pas apaisées. Cela s&#39;appelle, je crois, un sacrifice expiatoire. Et justice, pour les
partisans de la peine de mort, ne serait pas faite si à la mort de la victime ne répondait pas,
en écho, la mort du coupable.
Soyons clairs. Cela signifie simplement que la loi du talion demeurerait, à travers les
millénaires, la loi nécessaire, unique de la justice humaine.
Du malheur et de la souffrance des victimes, j&#39;ai, beaucoup plus que ceux qui s&#39;en réclament,
souvent mesuré dans ma vie l&#39;étendue. Que le crime soit le point de rencontre, le lieu
géométrique du malheur humain, je le sais mieux que personne. Malheur de la victime elle-
même et, au-delà, malheur de ses parents et de ses proches. Malheur aussi des parents du
criminel. Malheur enfin, bien souvent, de l&#39;assassin. Oui, le crime est malheur, et il n&#39;y a pas
un homme, pas une femme de coeur, de raison, de responsabilité, qui ne souhaite d&#39;abord le
combattre.
Mais ressentir, au profond de soi-même, le malheur et la douleur des victimes, mais lutter
de toutes les manières pour que la violence et le crime reculent dans notre société, cette
sensibilité et ce combat ne sauraient impliquer la nécessaire mise à mort du coupable. Que
les parents et les proches de la victime souhaitent cette mort, par réaction naturelle de l&#39;être
humain blessé, je le comprends, je le conçois. Mais c&#39;est une réaction humaine, naturelle. Or
tout le progrès historique de la justice a été de dépasser la vengeance privée. Et comment la
dépasser, sinon d&#39;abord en refusant la loi du talion ?
La vérité est que, au plus profond des motivations de l&#39;attachement à la peine de mort, on
trouve, inavouée le plus souvent, la tentation de l&#39;élimination. Ce qui paraît insupportable à
beaucoup, c&#39;est moins la vie du criminel emprisonné que la peur qu&#39;il récidive un jour. Et ils
pensent que la seule garantie, à cet égard, est que le criminel soit mis à mort par précaution.
Ainsi, dans cette conception, la justice tuerait moins par vengeance que par prudence. Au-
delà de la justice d&#39;expiation, apparaît donc la justice d&#39;élimination, derrière la balance, la

2
guillotine. L&#39;assassin doit mourir toute simplement parce que, ainsi, il ne récidivera pas. Et
tout paraît si simple, et tout paraît si juste !
Mais quand on accepte ou quand on prône la justice d&#39;élimination, au nom de la justice, il
faut bien savoir dans quelle voie on s&#39;engage. Pour être acceptable, même pour ses
partisans, la justice qui tue le criminel doit tuer en connaissance de cause. Notre justice, et
c&#39;est son honneur, ne tue pas les déments. Mais elle ne sait pas les identifier à coup sûr, et
c&#39;est à l&#39;expertise psychiatrique, la plus aléatoire, la plus incertaine de toutes, que, dans la
réalité judiciaire, on va s&#39;en remettre. Que le verdict psychiatrique soit favorable à l&#39;assassin,
et il sera épargné. La société acceptera d&#39;assumer le risque qu&#39;il représente sans que
quiconque s&#39;en indigne. Mais que le verdict psychiatrique lui soit défavorable, et il sera
exécuté. Quand on accepte la justice d&#39;élimination, il faut que les responsables politiques
mesurent dans quelle logique de l&#39;Histoire on s&#39;inscrit.
Je ne parle pas de sociétés où l&#39;on élimine aussi bien les criminels que les déments, les
opposants politiques que ceux dont on pense qu&#39;ils seraient de nature à &quot;polluer&quot; le corps
social. Non, je m&#39;en tiens à la justice des pays qui vivent en démocratie.
Enfoui, terré, au coeur même de la justice d&#39;élimination, veille le racisme secret. Si, en 1972,
la Cour suprême des Etats-Unis a penché vers l&#39;abolition, c&#39;est essentiellement parce qu&#39;elle
avait constaté que 60 p. 100 des condamnés à mort étaient des noirs, alors qu&#39;ils ne
représentaient que 12 p. 100 de la population. Et pour un homme de justice, quel vertige ! je
baisse la voix et je me tourne vers vous tous pour rappeler qu&#39;en France même, sur trente-
six condamnations à mort définitives prononcées depuis 1945, on compte neuf étrangers,
soit 25 p. 100, alors qu&#39;ils ne représentent que 8 p. 100 de la population ; parmi eux cinq
Maghrébins, alors qu&#39;ils ne représentent que 2 p. 100 de la population. Depuis 1965, parmi
les neuf condamnés à mort exécutés, on compte quatre étrangers, dont trois Maghrébins.
Leurs crimes étaient-ils plus odieux que les autres ou bien paraissaient-ils plus graves parce
que leurs auteurs, à cet instant, faisaient secrètement horreur ? C&#39;est une interrogation, ce
n&#39;est qu&#39;une interrogation, mais elle est si pressante et si lancinante que seule l&#39;abolition
peut mettre fin à une interrogation qui nous interpelle avec tant de cruauté.
Il s&#39;agit bien, en définitive, dans l&#39;abolition, d&#39;un choix fondamental, d&#39;une certaine
conception de l&#39;homme et de la justice. Ceux qui veulent une justice qui tue, ceux-là sont
animés par une double conviction : qu&#39;il existe des hommes totalement coupables, c&#39;est-à-
dire des hommes totalement responsables de leurs actes, et qu&#39;il peut y avoir une justice
sûre de son infaillibilité au point de dire que celui-là peut vivre et que celui-là doit mourir.
A cet âge de ma vie, l&#39;une et l&#39;autre affirmations me paraissent également erronées. Aussi
terribles, aussi odieux que soient leurs actes, il n&#39;est point d&#39;hommes en cette terre dont la
culpabilité soit totale et dont il faille pour toujours désespérer totalement. Aussi prudente
que soit la justice, aussi mesurés et angoissés que soient les femmes et les hommes qui
jugent, la justice demeure humaine, donc faillible.

3
Et je ne parle pas seulement de l&#39;erreur judiciaire absolue, quand, après une exécution, il se
révèle, comme cela peut encore arriver, que le condamné à mort était innocent et qu&#39;une
société entière - c&#39;est-à-dire nous tous - au nom de laquelle le verdict a été rendu, devient
ainsi collectivement coupable puisque sa justice rend possible l&#39;injustice suprême. Je parle
aussi de l&#39;incertitude et de la contradiction des décisions rendues qui font que les mêmes
accusés, condamnés à mort une première fois, dont la condamnation est cassée pour vice de
forme, sont de nouveau jugés et, bien qu&#39;il s&#39;agisse des mêmes faits, échappent, cette fois-ci,
à la mort, comme si, en justice, la vie d&#39;un homme se jouait au hasard d&#39;une erreur de plume
d&#39;un greffier. Ou bien tels condamnés, pour des crimes moindres, seront exécutés, alors que
d&#39;autres, plus coupables, sauveront leur tête à la faveur de la passion de l&#39;audience, du
climat ou de l&#39;emportement de tel ou tel.
Cette sorte de loterie judiciaire, quelle que soit la peine qu&#39;on éprouve à prononcer ce mot
quand il y va de la vie d&#39;une femme ou d&#39;un homme, est intolérable. Le plus haut magistrat
de France, M. Aydalot, au terme d&#39;une longue carrière tout entière consacrée à la justice et,
pour la plupart de son activité, au parquet, disait qu&#39;à la mesure de sa hasardeuse
application, la peine de mort lui était devenue, à lui magistrat, insupportable. Parce
qu&#39;aucun homme n&#39;est totalement responsable, parce qu&#39;aucune justice ne peut être
absolument infaillible, la peine de mort est moralement inacceptable. Pour ceux d&#39;entre
nous qui croient en Dieu, lui seul a le pouvoir de choisir l&#39;heure de notre mort. Pour tous les
abolitionnistes, il est impossible de reconnaître à la justice des hommes ce pouvoir de mort
parce qu&#39;ils savent qu&#39;elle est faillible.
Le choix qui s&#39;offre à vos consciences est donc clair : ou notre société refuse une justice qui
tue et accepte d&#39;assumer, au nom de ses valeurs fondamentales - celles qui l&#39;ont faite grande
et respectée entre toutes - la vie de ceux qui font horreur, déments ou criminels ou les deux
à la fois, et c&#39;est le choix de l&#39;abolition ; ou cette société croit, en dépit de l&#39;expérience des
siècles, faire disparaître le crime avec le criminel, et c&#39;est l&#39;élimination.
Cette justice d&#39;élimination, cette justice d&#39;angoisse et de mort, décidée avec sa marge de
hasard, nous la refusons. Nous la refusons parce qu&#39;elle est pour nous l&#39;anti-justice, parce
qu&#39;elle est la passion et la peur triomphant de la raison et de l&#39;humanité.

Extrait de l’intervention à l’Assemblée nationale de Monsieur Robert Badinter, garde des
sceaux, ministre de la justice, le 17 septembre 1981 durant la discussion du projet de loi
sur l’abolition de la peine de mort en France
Pour les partisans de la peine de mort, dont les abolitionnistes et moi-même avons toujours
respecté le choix en notant à regret que la réciproque n&#39;a pas toujours été vraie, la haine
répondant souvent à ce qui n&#39;était que l&#39;expression d&#39;une conviction profonde, celle que je
respecterai toujours chez les hommes de liberté, pour les partisans de la peine de mort,
disais-je, la mort du coupable est une exigence de justice. Pour eux, il est en effet des crimes
trop atroces pour que leurs auteurs puissent les expier autrement qu&#39;au prix de leur vie.
La mort et la souffrance des victimes, ce terrible malheur, exigeraient comme contrepartie
nécessaire, impérative, une autre mort et une autre souffrance. A défaut, déclarait un
ministre de la justice récent, l&#39;angoisse et la passion suscitées dans la société par le crime ne
seraient pas apaisées. Cela s&#39;appelle, je crois, un sacrifice expiatoire. Et justice, pour les
partisans de la peine de mort, ne serait pas faite si à la mort de la victime ne répondait pas,
en écho, la mort du coupable.
Soyons clairs. Cela signifie simplement que la loi du talion demeurerait, à travers les
millénaires, la loi nécessaire, unique de la justice humaine.
Du malheur et de la souffrance des victimes, j&#39;ai, beaucoup plus que ceux qui s&#39;en réclament,
souvent mesuré dans ma vie l&#39;étendue. Que le crime soit le point de rencontre, le lieu
géométrique du malheur humain, je le sais mieux que personne. Malheur de la victime elle-
même et, au-delà, malheur de ses parents et de ses proches. Malheur aussi des parents du
criminel. Malheur enfin, bien souvent, de l&#39;assassin. Oui, le crime est malheur, et il n&#39;y a pas
un homme, pas une femme de coeur, de raison, de responsabilité, qui ne souhaite d&#39;abord le
combattre.
Mais ressentir, au profond de soi-même, le malheur et la douleur des victimes, mais lutter
de toutes les manières pour que la violence et le crime reculent dans notre société, cette
sensibilité et ce combat ne sauraient impliquer la nécessaire mise à mort du coupable. Que
les parents et les proches de la victime souhaitent cette mort, par réaction naturelle de l&#39;être
humain blessé, je le comprends, je le conçois. Mais c&#39;est une réaction humaine, naturelle. Or
tout le progrès historique de la justice a été de dépasser la vengeance privée. Et comment la
dépasser, sinon d&#39;abord en refusant la loi du talion ?
La vérité est que, au plus profond des motivations de l&#39;attachement à la peine de mort, on
trouve, inavouée le plus souvent, la tentation de l&#39;élimination. Ce qui paraît insupportable à
beaucoup, c&#39;est moins la vie du criminel emprisonné que la peur qu&#39;il récidive un jour. Et ils
pensent que la seule garantie, à cet égard, est que le criminel soit mis à mort par précaution.
Ainsi, dans cette conception, la justice tuerait moins par vengeance que par prudence. Au-
delà de la justice d&#39;expiation, apparaît donc la justice d&#39;élimination, derrière la balance, la

2
guillotine. L&#39;assassin doit mourir toute simplement parce que, ainsi, il ne récidivera pas. Et
tout paraît si simple, et tout paraît si juste !
Mais quand on accepte ou quand on prône la justice d&#39;élimination, au nom de la justice, il
faut bien savoir dans quelle voie on s&#39;engage. Pour être acceptable, même pour ses
partisans, la justice qui tue le criminel doit tuer en connaissance de cause. Notre justice, et
c&#39;est son honneur, ne tue pas les déments. Mais elle ne sait pas les identifier à coup sûr, et
c&#39;est à l&#39;expertise psychiatrique, la plus aléatoire, la plus incertaine de toutes, que, dans la
réalité judiciaire, on va s&#39;en remettre. Que le verdict psychiatrique soit favorable à l&#39;assassin,
et il sera épargné. La société acceptera d&#39;assumer le risque qu&#39;il représente sans que
quiconque s&#39;en indigne. Mais que le verdict psychiatrique lui soit défavorable, et il sera
exécuté. Quand on accepte la justice d&#39;élimination, il faut que les responsables politiques
mesurent dans quelle logique de l&#39;Histoire on s&#39;inscrit.
Je ne parle pas de sociétés où l&#39;on élimine aussi bien les criminels que les déments, les
opposants politiques que ceux dont on pense qu&#39;ils seraient de nature à &quot;polluer&quot; le corps
social. Non, je m&#39;en tiens à la justice des pays qui vivent en démocratie.
Enfoui, terré, au coeur même de la justice d&#39;élimination, veille le racisme secret. Si, en 1972,
la Cour suprême des Etats-Unis a penché vers l&#39;abolition, c&#39;est essentiellement parce qu&#39;elle
avait constaté que 60 p. 100 des condamnés à mort étaient des noirs, alors qu&#39;ils ne
représentaient que 12 p. 100 de la population. Et pour un homme de justice, quel vertige ! je
baisse la voix et je me tourne vers vous tous pour rappeler qu&#39;en France même, sur trente-
six condamnations à mort définitives prononcées depuis 1945, on compte neuf étrangers,
soit 25 p. 100, alors qu&#39;ils ne représentent que 8 p. 100 de la population ; parmi eux cinq
Maghrébins, alors qu&#39;ils ne représentent que 2 p. 100 de la population. Depuis 1965, parmi
les neuf condamnés à mort exécutés, on compte quatre étrangers, dont trois Maghrébins.
Leurs crimes étaient-ils plus odieux que les autres ou bien paraissaient-ils plus graves parce
que leurs auteurs, à cet instant, faisaient secrètement horreur ? C&#39;est une interrogation, ce
n&#39;est qu&#39;une interrogation, mais elle est si pressante et si lancinante que seule l&#39;abolition
peut mettre fin à une interrogation qui nous interpelle avec tant de cruauté.
Il s&#39;agit bien, en définitive, dans l&#39;abolition, d&#39;un choix fondamental, d&#39;une certaine
conception de l&#39;homme et de la justice. Ceux qui veulent une justice qui tue, ceux-là sont
animés par une double conviction : qu&#39;il existe des hommes totalement coupables, c&#39;est-à-
dire des hommes totalement responsables de leurs actes, et qu&#39;il peut y avoir une justice
sûre de son infaillibilité au point de dire que celui-là peut vivre et que celui-là doit mourir.
A cet âge de ma vie, l&#39;une et l&#39;autre affirmations me paraissent également erronées. Aussi
terribles, aussi odieux que soient leurs actes, il n&#39;est point d&#39;hommes en cette terre dont la
culpabilité soit totale et dont il faille pour toujours désespérer totalement. Aussi prudente
que soit la justice, aussi mesurés et angoissés que soient les femmes et les hommes qui
jugent, la justice demeure humaine, donc faillible.

3
Et je ne parle pas seulement de l&#39;erreur judiciaire absolue, quand, après une exécution, il se
révèle, comme cela peut encore arriver, que le condamné à mort était innocent et qu&#39;une
société entière - c&#39;est-à-dire nous tous - au nom de laquelle le verdict a été rendu, devient
ainsi collectivement coupable puisque sa justice rend possible l&#39;injustice suprême. Je parle
aussi de l&#39;incertitude et de la contradiction des décisions rendues qui font que les mêmes
accusés, condamnés à mort une première fois, dont la condamnation est cassée pour vice de
forme, sont de nouveau jugés et, bien qu&#39;il s&#39;agisse des mêmes faits, échappent, cette fois-ci,
à la mort, comme si, en justice, la vie d&#39;un homme se jouait au hasard d&#39;une erreur de plume
d&#39;un greffier. Ou bien tels condamnés, pour des crimes moindres, seront exécutés, alors que
d&#39;autres, plus coupables, sauveront leur tête à la faveur de la passion de l&#39;audience, du
climat ou de l&#39;emportement de tel ou tel.
Cette sorte de loterie judiciaire, quelle que soit la peine qu&#39;on éprouve à prononcer ce mot
quand il y va de la vie d&#39;une femme ou d&#39;un homme, est intolérable. Le plus haut magistrat
de France, M. Aydalot, au terme d&#39;une longue carrière tout entière consacrée à la justice et,
pour la plupart de son activité, au parquet, disait qu&#39;à la mesure de sa hasardeuse
application, la peine de mort lui était devenue, à lui magistrat, insupportable. Parce
qu&#39;aucun homme n&#39;est totalement responsable, parce qu&#39;aucune justice ne peut être
absolument infaillible, la peine de mort est moralement inacceptable. Pour ceux d&#39;entre
nous qui croient en Dieu, lui seul a le pouvoir de choisir l&#39;heure de notre mort. Pour tous les
abolitionnistes, il est impossible de reconnaître à la justice des hommes ce pouvoir de mort
parce qu&#39;ils savent qu&#39;elle est faillible.
Le choix qui s&#39;offre à vos consciences est donc clair : ou notre société refuse une justice qui
tue et accepte d&#39;assumer, au nom de ses valeurs fondamentales - celles qui l&#39;ont faite grande
et respectée entre toutes - la vie de ceux qui font horreur, déments ou criminels ou les deux
à la fois, et c&#39;est le choix de l&#39;abolition ; ou cette société croit, en dépit de l&#39;expérience des
siècles, faire disparaître le crime avec le criminel, et c&#39;est l&#39;élimination.
Cette justice d&#39;élimination, cette justice d&#39;angoisse et de mort, décidée avec sa marge de
hasard, nous la refusons. Nous la refusons parce qu&#39;elle est pour nous l&#39;anti-justice, parce
qu&#39;elle est la passion et la peur triomphant de la raison et de l&#39;humanité.
"""

bad_doc = """
Extrait de l’intervention à l’Assemblée nationale de Monsieur Robert Badinter, garde des sceaux, ministre de la justice, le 17 septembre 1981 durant la discussion du projet de loi sur l’abolition de la peine de mort en France
Pour les partisans de la peine de mort, dont les abolitionnistes et moi-même avons toujours respecté le choix en notant à regret que la réciproque n'a pas toujours été vraie, la haine répondant souvent à ce qui n'était que l'expression d'une conviction profonde, celle que je respecterai toujours chez les hommes de liberté, pour les partisans de la peine de mort, disais-je, la mort du coupable est une exigence de justice. Pour eux, il est en effet des crimes trop atroces pour que leurs auteurs puissent les expier autrement qu'au prix de leur vie.
La mort et la souffrance des victimes, ce terrible malheur, exigeraient comme contrepartie nécessaire, impérative, une autre mort et une autre souffrance. A défaut, déclarait un ministre de la justice récent, l'angoisse et la passion suscitées dans la société par le crime ne seraient pas apaisées. Cela s'appelle, je crois, un sacrifice expiatoire. Et justice, pour les partisans de la peine de mort, ne serait pas faite si à la mort de la victime ne répondait pas, en écho, la mort du coupable.
Soyons clairs. Cela signifie simplement que la loi du talion demeurerait, à travers les millénaires, la loi nécessaire, unique de la justice humaine.  
Du malheur et de la souffrance des victimes, j'ai, beaucoup plus que ceux qui s'en réclament, souvent mesuré dans ma vie l'étendue. Que le crime soit le point de rencontre, le lieu géométrique du malheur humain, je le sais mieux que personne. Malheur de la victime elle-même et, au-delà, malheur de ses parents et de ses proches. Malheur aussi des parents du criminel. Malheur enfin, bien souvent, de l'assassin. Oui, le crime est malheur, et il n'y a pas un homme, pas une femme de coeur, de raison, de responsabilité, qui ne souhaite d'abord le combattre.
Mais ressentir, au profond de soi-même, le malheur et la douleur des victimes, mais lutter de toutes les manières pour que la violence et le crime reculent dans notre société, cette sensibilité et ce combat ne sauraient impliquer la nécessaire mise à mort du coupable. Que les parents et les proches de la victime souhaitent cette mort, par réaction naturelle de l'être humain blessé, je le comprends, je le conçois. Mais c'est une réaction humaine, naturelle. Or tout le progrès historique de la justice a été de dépasser la vengeance privée. Et comment la dépasser, sinon d'abord en refusant la loi du talion ?
La vérité est que, au plus profond des motivations de l'attachement à la peine de mort, on trouve, inavouée le plus souvent, la tentation de l'élimination. Ce qui paraît insupportable à beaucoup, c'est moins la vie du criminel emprisonné que la peur qu'il récidive un jour. Et ils pensent que la seule garantie, à cet égard, est que le criminel soit mis à mort par précaution.
Ainsi, dans cette conception, la justice tuerait moins par vengeance que par prudence. Au-delà de la justice d'expiation, apparaît donc la justice d'élimination, derrière la balance, la guillotine. L'assassin doit mourir toute simplement parce que, ainsi, il ne récidivera pas. Et tout paraît si simple, et tout paraît si juste !
Mais quand on accepte ou quand on prône la justice d'élimination, au nom de la justice, il faut bien savoir dans quelle voie on s'engage. Pour être acceptable, même pour ses partisans, la justice qui tue le criminel doit tuer en connaissance de cause. Notre justice, et c'est son honneur, ne tue pas les déments. Mais elle ne sait pas les identifier à coup sûr, et c'est à l'expertise psychiatrique, la plus aléatoire, la plus incertaine de toutes, que, dans la réalité judiciaire, on va s'en remettre. Que le verdict psychiatrique soit favorable à l'assassin, et il sera épargné. La société acceptera d'assumer le risque qu'il représente sans que quiconque s'en indigne. Mais que le verdict psychiatrique lui soit défavorable, et il sera exécuté. Quand on accepte la justice d'élimination, il faut que les responsables politiques mesurent dans quelle logique de l'Histoire on s'inscrit.
Je ne parle pas de sociétés où l'on élimine aussi bien les criminels que les déments, les opposants politiques que ceux dont on pense qu'ils seraient de nature à "polluer" le corps social. Non, je m'en tiens à la justice des pays qui vivent en démocratie.
Enfoui, terré, au coeur même de la justice d'élimination, veille le racisme secret. Si, en 1972, la Cour suprême des Etats-Unis a penché vers l'abolition, c'est essentiellement parce qu'elle avait constaté que 60 p. 100 des condamnés à mort étaient des noirs, alors qu'ils ne représentaient que 12 p. 100 de la population. Et pour un homme de justice, quel vertige ! je baisse la voix et je me tourne vers vous tous pour rappeler qu'en France même, sur trente-six condamnations à mort définitives prononcées depuis 1945, on compte neuf étrangers, soit 25 p. 100, alors qu'ils ne représentent que 8 p. 100 de la population ; parmi eux cinq Maghrébins, alors qu'ils ne représentent que 2 p. 100 de la population. Depuis 1965, parmi les neuf condamnés à mort exécutés, on compte quatre étrangers, dont trois Maghrébins. Leurs crimes étaient-ils plus odieux que les autres ou bien paraissaient-ils plus graves parce que leurs auteurs, à cet instant, faisaient secrètement horreur ? C'est une interrogation, ce n'est qu'une interrogation, mais elle est si pressante et si lancinante que seule l'abolition peut mettre fin à une interrogation qui nous interpelle avec tant de cruauté.
Il s'agit bien, en définitive, dans l'abolition, d'un choix fondamental, d'une certaine conception de l'homme et de la justice. Ceux qui veulent une justice qui tue, ceux-là sont animés par une double conviction : qu'il existe des hommes totalement coupables, c'est-à-dire des hommes totalement responsables de leurs actes, et qu'il peut y avoir une justice sûre de son infaillibilité au point de dire que celui-là peut vivre et que celui-là doit mourir.
A cet âge de ma vie, l'une et l'autre affirmations me paraissent également erronées. Aussi terribles, aussi odieux que soient leurs actes, il n'est point d'hommes en cette terre dont la culpabilité soit totale et dont il faille pour toujours désespérer totalement. Aussi prudente que soit la justice, aussi mesurés et angoissés que soient les femmes et les hommes qui jugent, la justice demeure humaine, donc faillible.
Et je ne parle pas seulement de l'erreur judiciaire absolue, quand, après une exécution, il se révèle, comme cela peut encore arriver, que le condamné à mort était innocent et qu'une société entière - c'est-à-dire nous tous - au nom de laquelle le verdict a été rendu, devient ainsi collectivement coupable puisque sa justice rend possible l'injustice suprême. Je parle aussi de l'incertitude et de la contradiction des décisions rendues qui font que les mêmes accusés, condamnés à mort une première fois, dont la condamnation est cassée pour vice de forme, sont de nouveau jugés et, bien qu'il s'agisse des mêmes faits, échappent, cette fois-ci, à la mort, comme si, en justice, la vie d'un homme se jouait au hasard d'une erreur de plume d'un greffier. Ou bien tels condamnés, pour des crimes moindres, seront exécutés, alors que d'autres, plus coupables, sauveront leur tête à la faveur de la passion de l'audience, du climat ou de l'emportement de tel ou tel.
Cette sorte de loterie judiciaire, quelle que soit la peine qu'on éprouve à prononcer ce mot quand il y va de la vie d'une femme ou d'un homme, est intolérable. Le plus haut magistrat de France, M. Aydalot, au terme d'une longue carrière tout entière consacrée à la justice et, pour la plupart de son activité, au parquet, disait qu'à la mesure de sa hasardeuse application, la peine de mort lui était devenue, à lui magistrat, insupportable. Parce qu'aucun homme n'est totalement responsable, parce qu'aucune justice ne peut être absolument infaillible, la peine de mort est moralement inacceptable. Pour ceux d'entre nous qui croient en Dieu, lui seul a le pouvoir de choisir l'heure de notre mort. Pour tous les abolitionnistes, il est impossible de reconnaître à la justice des hommes ce pouvoir de mort parce qu'ils savent qu'elle est faillible.
Le choix qui s'offre à vos consciences est donc clair : ou notre société refuse une justice qui tue et accepte d'assumer, au nom de ses valeurs fondamentales - celles qui l'ont faite grande et respectée entre toutes - la vie de ceux qui font horreur, déments ou criminels ou les deux à la fois, et c'est le choix de l'abolition ; ou cette société croit, en dépit de l'expérience des siècles, faire disparaître le crime avec le criminel, et c'est l'élimination.
Cette justice d'élimination, cette justice d'angoisse et de mort, décidée avec sa marge de hasard, nous la refusons. Nous la refusons parce qu'elle est pour nous l'anti-justice, parce qu'elle est la passion et la peur triomphant de la raison et de l'humanité.
"""
