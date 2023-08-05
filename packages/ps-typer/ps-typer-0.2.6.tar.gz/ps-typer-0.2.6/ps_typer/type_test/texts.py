import random
from pathlib import Path
from typing import Generator

from marshmallow.fields import Function

from ps_typer.type_test.api import FactsApi

# PATHS
PROJECT_FOLDER = Path(__file__).absolute().parents[1]
ASSETS_FOLDER = PROJECT_FOLDER / "assets"
TEXTS_FOLDER = ASSETS_FOLDER / "texts"
BROWN_TEXT = TEXTS_FOLDER / "brown.txt"
WEBTEXT_TEXT = TEXTS_FOLDER / "webtext.txt"
GUTENBERG_TEXT = TEXTS_FOLDER / "gutenberg.txt"

# CONSTANTS
RANDOM_TEXT_SENTENCES = 3  # Length in sentences for random text

# TEXTS
COMMON_PHRASES = [
    "A bird in the hand is worth two in the bush.",
    "A penny for your thoughts.",
    "A penny saved is a penny earned.",
    "A picture is worth 1000 words.",
    "Actions speak louder than words.",
    "Barking up the wrong tree.",
    "Birds of a feather flock together.",
    "By the skin of your teeth.",
    "Comparing apples to oranges.",
    "Do unto others as you would have them do unto you.",
    "Don't count your chickens before they hatch.",
    "Don't cry over spilt milk.",
    "Don't give up your day job.",
    "Don't put all your eggs in one basket.",
    "Every cloud has a silver lining.",
    "Get a taste of your own medicine.",
    "Good things come to those who wait.",
    "He has bigger fish to fry.",
    "He's a chip off the old block.",
    "Hit the nail on the head.",
    "It ain't over till the fat lady sings.",
    "It takes one to know one.",
    "It's raining cats and dogs.",
    "Kill two birds with one stone.",
    "Let the cat out of the bag.",
    "Look before you leap.",
    "Saving for a rainy day.",
    "Slow and steady wins the race.",
    "Take it with a grain of salt.",
    "The ball is in your court.",
    "The best thing since sliced bread.",
    "The devil is in the details.",
    "The early bird gets the worm.",
    "The elephant in the room.",
    "The whole nine yards.",
    "There are other fish in the sea.",
    "There's a method to his madness.",
    "There's no such thing as a free lunch.",
    "Throw caution to the wind.",
    "You can't have your cake and eat it too.",
    "You can't judge a book by its cover.",
    "A little learning is a dangerous thing.",
    "A snowball's chance in hell.",
    "A stitch in time saves nine.",
    "An apple a day keeps the doctor away.",
    "An ounce of prevention is worth a pound of cure.",
    "Bolt from the blue.",
    "Calm before the storm.",
    "Curiosity killed the cat.",
    "Don't beat a dead horse.",
    "Every dog has his day.",
    "Familiarity breeds contempt.",
    "Fortune favours the bold.",
    "Haste makes waste.",
    "He who laughs last laughs loudest.",
    "He's not playing with a full deck.",
    "He's sitting on the fence.",
    "It is a poor workman who blames his tools.",
    "It is always darkest before the dawn.",
    "It takes two to tango.",
    "Know which way the wind is blowing.",
    "Leave no stone unturned.",
    "Let sleeping dogs lie.",
    "Like riding a bicycle.",
    "Like two peas in a pod.",
    "Make hay while the sun shines.",
    "Once bitten, twice shy.",
    "Out of the frying pan and into the fire.",
    "Shape up or ship out.",
    "The pot calling the kettle black.",
    "There are clouds on the horizon.",
    "Those who live in glass houses shouldn't throw stones.",
    "Through thick and thin.",
    "Waste not, want not.",
    "Well begun is half done.",
    "When it rains it pours.",
    "You can't make an omelet without breaking some eggs.",
]

BACKUP_FACTS = [
    "There are more possible iterations of a game of chess than there are atoms in the known universe. There are also more ways to arrange a deck of cards than atoms in the known universe.",
    "Cleopatra lived closer in time to the Moon landing than to the construction of the Great Pyramid of Giza.",
    "It can take a photon 100,000 years to travel from the core of the sun to the surface, but only 8 minutes to travel the rest of the way to earth. This is due to the extreme density of the core of the Sun (150 times that of water).",
    "It would take roughly 1.1 million mosquitoes, all sucking at once, to completely drain the average human of blood. The average human has 1.75 square metres of skin, so this would mean about 63 mosquitoes per square centimeter of your skin.",
    "Written language was developed independently by the Egyptians, Mesopotamians (the Sumer language), Chinese, and Mesoamericans (such as the Olmecs and Zapotecs). There is also evidence of possible forms of writing developed in other regions, such as Polynesia.",
    "Atoms are made up of mostly empty space. If the nucleus of an atom was the size of a football, the nearest electron would be 0.8km away. That means even the most solid-looking objects we see are predominantly nothingness. Put another way, if you were to remove all the empty space in the atoms that make up a human being, they would be a lot smaller than a grain of salt. In fact, you would be able to fit 6 billion of us inside a single apple.",
    "Honey does not spoil. You could feasibly eat 3000 year old honey. It does, however, crystallise with time, but all you have to do is put it in water and warm it until it's back to its original state and you can eat it. This has been observed by archaeologists excavating Egyptina tombs, finding pots of honey thousands of years old yet still preserved.",
    "If you somehow found a way to extract all of the gold from the bubbling core of our lovely little planet, it is estimated that there would be enough to cover the surface of the planet in 13 inches.",
    "To know when to mate, a male giraffe will continuously headbutt the female in the bladder until she urinates. The male then tastes the pee and that helps it determine whether the female is ovulating.",
    "The largest known living organism by mass is a clonal colony of quaking aspen trees. Pando (Latin for I spread out) is a group of genetically identical quaking aspens in Utah with an interconnected root system. It's an estimated 80,000 years old and takes up more than 400000 square metres. The largest organism by area is a colony of honey fungus in Oregon, which has almost as much biomass as Pando.",
    "The blue whale is the largest animal to have ever lived, reaching a confirmed max length of 29.9 meters and weight of 173 tonnes, dwarfing even the biggest dinosaurs and our biggest megaladon estimates. Their hearts are the size of a small car and have blood vessels so big that a small child could swim through. Our first ever recording of a blue whale's heartbeat showed their heartbeat staying within a range of 2-37bpm. For reference, the average human's resting heartrate is between 60-100bpm.",
    "Four times more people speak English as a second language than as a native one. It's the most widely spoken tongue in the world, with nearly two billion people learning it as a second language and only around 460 million people speaking it natively. As of 2012, India claims to have the world's second-largest English-speaking population at 125 million people, second only to the USA (330 million).",
    "About 400-500 grapes go into one bottle of wine. That's approximately 2kg per bottle.",
    "Once, a Texas man was hospitalized when a bullet he shot at an armadillo ricocheted off the animal and hit him in the jaw. Despite several reports saying bullets ricocheted off of armadillos, these creatures are not bulletproof. Their shells are made of bony plates called osteoderms that grow in the skin. They're loosely connected for flexibility and are covered by a layer of keratin, the protein that makes up hair, nails, and horns. The shell protects the armadillos from thorny shrubs, under which they can hide from predators.",
    "Chess is called the game of kings. The history of chess can be traced back nearly 1500 years, although the earliest origins are uncertain. The earliest predecessor of the game probably originated in India, before the 6th century AD. From India, the game spread to Persia. When the Arabs conquered Persia, chess was taken up by the Muslim world and subsequently spread to Southern Europe. In Europe, chess evolved into roughly its current form in the 15th century.",
    "It might seem safe to assume that the Canary Islands were named after canary birds, but the location was actually named after dogs. Although it's off the coast of northwestern Africa, the archipelago is actually part of Spain. In Spanish, the area's name is Islas Canarias, which comes from the Latin phrase 'Canariae Insulae' which means 'island of dogs.'",
    "When 174 world leaders signed the Paris Agreement on Earth Day in 2016 at the United Nations (UN) headquarters in New York, it was the largest number of countries ever to come together to sign anything on a single day, according to the UN. The agreement aimed to combat climate change and accelerate and intensify the actions and investments needed to strengthen the global climate effort.",
    "Earthquakes can range from minor tremors that are barely noticeable to building-toppling ground-shakers that cause massive destruction. But it's an inevitable part of life for those who live in countries such as China, Indonesia, Iran, and Turkey, which are some of the most earthquake-prone places on the planet. However, according to the U.S. Geological Survey, Japan records the most earthquakes in the world, but other countries such as Indonesia, Tonga or Fiji likely have the most earthquakes per unit area.",
    "According to the Population Reference Bureau, since the time 'modern' Homo sapiens first hit the scene 50,000 years ago, more than 108 billion members of our species have been born. And a large chunk of that number is alive right now. According to the bureau, the number of people alive today represents a whopping seven percent of the total number of humans who have ever lived.",
    "Not everyone lives in a booming city or sprawling suburb. Many people still make their homes outside of bustling locations-especially in India, which has the largest number of people living in rural areas (approximately 737 million people live outside of the city). China also has an impressively large rural population, with 545 million living outside of urban areas.",
    "While modern nation states known as countries are relatively new, many nations can trace back their history hundreds or thousands of years (for example, Greece). But South Sudan in North Africa just gained its independence from Sudan in 2011, which currently makes it the youngest country in the world (with widespread recognition). It gained independence from the Republic of Sudan after a decades long civil war which ended in 2005. As of 2019, South Sudan unfortunately ranks third-lowest in the UN World Happiness Report, and second-lowest on the Global Peace Index.",
    "The British royal family may be the most famous royal family on the planet, but there are still plenty of other nobles out there. In total, there are 26 royal families, and a total of 44 sovereign states around the world with a monarch as their Head of State. Examples include Japan, Spain, Swaziland, Bhutan, Thailand, Monaco, Sweden and the Netherlands",
    "Panda diplomacy is the practice of sending giant pandas from China to other countries as a tool of diplomacy. While the practice has been recorded as far back as the Tang dynasty, when Empress Wu Zetian sent a pair of giant pandas to Emperor Tenmu of Japan in 685CE, the term only came into popular use during the Cold War. The People's Republic of China began to use panda diplomacy more prominently in the 1950s, and has continued the practice into the present day. However, in 1984 they adopted a loan policy which meant that subsequent pandas would be loaned, not gifted, so almost all giant pandas worldwide belong to China.",
    "During his lifetime between 1162 and 1227, Genghis Khan fathered countless children.When Mongol armies attacked, the most beautiful women were reserved for Genghis. One thirteenth century Persian historian claimed that within a century of Khan's birth, his enthusiastic mating habits had created a lineage of more than 20,000 individuals. And while we may never know exactly how many offspring the leader of the Mongol Empire had, an international team of geneticists found that around 1 in every 200 men (around 16 million people) are direct descendants of his, according to a 2003 historical genetics paper.",
    "Tokyo is a booming city-not only by Japanese standards, but also compared to cities around the world. With around 37 million people living in Tokyo, it's the world's largest city when it comes to population size, according to Reuters. The next largest city is Delhi, India (population 29 million) and Shanghai, China (population 26 million).",
    "Canadians say 'sorry' so much that a law was passed in 2009 called the Apology Act declaring that an apology can't be used as evidence of admission to guilt.",
    "Scientists previously thought that the moon's volcanic activity died down a billion years ago. But new data from NASA's Lunar Reconnaissance Orbiter, or LRO, hints that lunar lava flowed much more recently, perhaps less than 100 million years ago. This would mean that there could still have been volcanic activity on the moon back when dinosaurs were still around.",
    "There were two AI chatbots created by Facebook to talk to each other, but they were shut down after they started communicating in a gibberish language they made for themselves. These AIs were made to trade with each other, and started speaking in this gibberish because no language enforcement was set for them, and their only goal was to trade, so English became irrelevant. The code and documentation for these AIs is publicly available and you can run them yourself if you want to.",
    "In 2009, Stephen Hawking held a reception for time travelers, but didn't publicize it until after. This way, only those who could time travel would be able to attend. Nobody else attended.",
    "In World War II, Germany tried to collapse the British economy by dropping millions of counterfeit bills over London. This was known as Operation Bernhard and estimates on the value of forged bills dropped varies from £132.6 million up to £300 million. This unit responsible for forging the bills also managed to perfect the art for US dollars, and forged bills were used to finance German intelligence operations.",
    "Birds are the closest living relatives of crocodilians, as well as the descendants of extinct dinosaurs with feathers. This means that birds are thought to be the only direct descendants of dinosaurs still living today.",
    "Cold showers have more health benefits than hot or warm showers. These include improving circulation, stimulating weight loss by improving metabolism, and easing depression by acting as a kind of light electroshock therapy. Cold showers can also increase your resistance to common illnesses.",
    "During the first live iPhone presentation, Steve Jobs had to frequently switch phones behind his desk. Otherwise, it would run out of RAM and crash. The 100 or so iphones in existence at the time were also riddled with bugs, meaning the development team had to come up with a 'golden path', a series of specific tasks performed in a specific order that would be least likely to cause the phone to crash.",
    "Movie theaters make roughly 85 percent of their profit off concession stands. This is because most of the money earned from ticket revenue goes to the movie distributors, and things like popcorn and fizzy drinks can be sold at profit margins of around 90%.",
    "If you ate nothing but rabbit meat, you would die from protein poisoning. This would be a mixture of too much protein and an absence of fat in the diet (fat is essential to human nutrition), and is the origin of the term rabbit starvation. Similarly, any diet made up entirely of lean meats would also lead to protein poisining.",
    "Italy built an entire courthouse to prosecute the Mafia back in 1986. Throughout and after the trial, several judges and magistrates were killed by the Mafia, including the two who led it--Giovanni Falcone and Paolo Borsellino. They indicted 475 members in a trial that lasted from 1986-1992. They convicted 338 people, sentenced to a total of 2,665 years, not including life sentences handed to 19 bosses. To date, it was the biggest trial in the world. In 2020, another courthouse has been built, this time to prosecute the 'Ndrangheta, believed to currently be the richest crime syndicate in the world.",
    "Pitbulls rank high among the most affectionate and least aggressive dogs. In general, they are not aggressive towards people but may be less tolerant of other dogs than other breeds. Pitbulls are only aggressive when forcibly trained/encouraged as such; usually because of irresponsible owners drawn to the dog's macho image who encourage aggression for fighting and protection.",
    "When Blackbeard captured ships, many of the African slaves on board would go on to become pirates. When he died, nearly one-third of his total crew were former slaves. However, most slaves. However, he was no abolitionist. Reports also account that Blackbeard and his associates also returned slaves to the mainland to be sold at auction.",
    "Cucumber can actually cure bad breath. A slice pressed to the roof of your mouth for 30 seconds with your tongue allows the phytochemicals to kill the problematic bacteria. Crunchy vegetables help remove plaque on teeth and gums, which bacteria can feed on, says Gregg Lituchy, a cosmetic dentist in New York City.",
    "The King of Macedon, Philip, threatened Sparta with ' If once I enter into your territories, I will destroy ye all, never to rise again'. The Spartans replied: 'If'. Subsequently, neither Philip nor his son Alexander the Great attempted to capture the city. Philip is also recorded as approaching Sparta on another occasion and asking whether he should come as friend or foe; the reply was 'Neither'.",
    "Einstein's brain went missing when he died in 1955. The pathologist on call, Thomas Harvey, who worked on his autopsy took it without permission. Einstein had left behind specific instructions regarding his remains: cremate them, and scatter the ashes secretly in order to discourage idolaters. Einstein's family was essentially strong-armed into agreeing to participate in research that Einstein explicitly did not want to participate in. Several studies were released about his brain many years later but none of them conclusively proved that there was anything special about his brain.",
    "Mulan has the highest kill-count of any (pure, not MCU, Star Wars etc. in which case Thanos easily comes out on top) Disney character (except for maybe King Kashekim Nedakh from Atlantis), and was the first Disney Princess to be shown killing people on-screen. From a scene in the movie, she shoots causes an avalanche to crush 2000 Huns, and only 6 survive. She later goes on to kill the leader of the Huns, one of the survivors, bringing her kill count to 1,995.",
    "One of the earliest depictions of dreadlocks dates back to 1600BCE (roughly 3600 years ago) to the Minoan civilization, one of Europe's earliest civilizations, who lived in what is now known as Greece.",
    "The reason the taste of artificial banana flavoring and artificial banana flavored products doesn't taste like bananas is because it is based on a type of banana that was mostly wiped out by several fungal plagues (most notably the Panama disease) in the 1950's.",
    "Due to the humid and moist conditions that a sloth lives in, algae will sometimes grow in its fur giving the animal a green tint. Sloths also move extremely slowly, with top speeds of 6cm per second. Both of these traits allow this so called lazy animal to be almost invisible to predators, giving them a major evolutionary advantage. They also have an extremely thorough digestive system, where food can take many days to pass through. This allows them to extract every bit of energy and nutrition from the relatively small amount of food they consume.",
    "American microbiologist Maurice Ralph Hilleman and his team are accredited with developing 8 of the 14 routine vaccinations used in current American vaccine schedules, these being measles, mumps, hepatitis A, hepatitis B, chickenpox, meningitis,  Neisseria meningitidis, Streptococcus pneumoniae and Haemophilus influenzae. He developed over 40 vaccines, an unparalleled record of productivity. According to one estimate, his vaccines save nearly 8 million lives each year.",
    """It is predicted that the reason why night insects, such as moths, are attracted to lights is because they mistake them for the light of the moon, which they use to navigate the Earth in a process called transverse orientation. "Elements in their eyes are tuned to faint light, and act 'like miniature telescopes'. Thus when they're faced with powerful artificial illumination, it can act as a 'super-stimulant'," says Lynn Kimsey, professor of entomology at UC Davis.""",
    "Film producer Jeffrey Katzenberg revived The Walt Disney Studios by producing some of their biggest hits: The Little Mermaid, The Lion King, Beauty and the Beast and Aladdin. He decided to quit after the chairman refused to promote him to the number two spot. After leaving them, they withheld a bonus from him, which he took them to court for $250 million they owed him and won. He went on to found DreamWorks Studios, and oversaw the production of such popular animated franchises as Shrek, Madagascar and Kung Fu Panda.",
    "Through the use of optogenetics, which uses a pulse of light to activate or deactivate neurons, scientists were able to create a false memory within a mouse's brain. A mouse was put in a box with the smell of acetephenone on one side and the smell of carvone on the other, but went to the side with acetephenone even though it had never smelled it before. This was done by simultaneously activating the neurons that sense acetophenone and those associated with reward, creating the 'memory' that the smell of acetephenone leads to a reward.",
    "The word 'quarantine' derives from the Venetian dialect of Italian and the words 'quaranta giorni', meaning 'forty days'. This is because when it was discovered that ships were infested with plague-carrying rats they were made to sit at anchor outside Venice's city walls for forty days before coming ashore.",
    "In a survival situation if you were to drink seawater it would rapidly dehydrate you and soon lead to your death. However, it is vastly less harmful to eat frozen seawater. This is because it contains a tenth the amount of salt as its liquid form, due to the fact that the salt is separated from the water when freezing as it does not fit into the crystalline structure of ice. If you are trying to make seawater drinkable manually, however, evaporation is still more efficient.",
    "Due to the extremely warm weather in the summer of 2013, several nuclear power plants across the world, including ones in Japan, Israel and Scotland, were forced to close down because of a sudden increase in the population of jellyfish, as well as loss in efficiency due to warmer water. Mass amounts of jellyfish can sometimes clog the filters that draw seawater into the power plants in order to cool down the reactors.",
    "France has conducted 210 nuclear weapon tests, more than the United Kingdom, China, India, and North Korea combined! This is just over a fifth of the amount conducted by the United States, however, who have conducted roughly 1,032 tests.",
    "Iran carries out the most gender-change operations in the world after Thailand. Estimates suggest around 50,000 people living in Iran are transgender. Sex reassignment surgeries are partially financially supported by the state. However, the government of Iran is considered to be one of the most discriminatory towards homosexual people in the world, and hundreds have been executed due to their sexual orientation. Some homosexual individuals in Iran have been pressured to undergo sex reassignment surgery in order to avoid legal and social persecution.",
    "There is an Australian man, James Harrison, who has a singularly unique blood plasma composition that has been used to cure Rhesus disease, a hemolytic disease that affects newborn babies. He has made over 1,000 donations throughout his lifetime, and these donations are estimated to have saved over 2.4 million babies from the condition.",
    "In Bordeaux, France, 1940, Portuguese diplomat Aristides de Sousa Mendes issued an estimated 30,000 Portuguese travel visas to Jewish families in order for them to flee persecution from the Nazis. Once his superiors had learned of his actions, he was ordered back to Portugal, dismissed from office and denied his pension benefits. Sousa Mendes went on to die in 1954, impoverished and unsung.",
    "Archeologists in London have found a Mesolithic tool-making factory that gives substantial proof human beings were living on the River Thames 7,000 BCE. That's over 9,000 years ago! This predates previous estimates of human habitation of the Thames, which was thought to be 4000 BCE.",
    "In 1995, strange 2-meter-wide circular patterns were discovered on the ocean's floor. Deemed the 'underwater crop circles', these mysterious patterns were a mystery until early 2011 when it was discovered that a previously undiscovered species of 12-centimeter long puffer-fish were the culprits. After studying these animals, scientists say that the meticulous creation and upkeep of these patterns by the male puffer-fish serve as an attraction for the opposite sex as well as a nest for the female puffer-fish's eggs.",
    "In the bioengineering department of the University of Illinois, researchers have created small 'biobots', partly out of synthetic gel and partly out of muscle cell, that can move on their own. Whilst only a small scientific step, this brings mechanical engineering one step closer to developing autonomous biobots: tiny devices that could exist within the human body, freely detecting illness and administering medication.",
    "Colombian drug-lord Pablo Escobar kept four hippos in his estate before his death in 1993. Deemed too much hassle to move by authorities, his hippos were left there and have since bred and escaped becoming an invasive species of Colombia. TThere are now an estimated 80-100 hippos living in the Magdalena River Basin area.",
    "The world's biggest tire producer is LEGO. In 2011, LEGO manufactured over 318 million tires, while brands such as Bridgestone, Michelin, Goodyear all produced below 200 million each. In Billund, Denmark, LEGO produces 870,000 tyres every day. They may be tiny toy tires, but the fact still stands.",
    "Research has found that a mid-day nap can make you more creative, focused, and fresh for the rest of the day. But one study in 2007 also found that they can also reduce your risk of heart disease. Specifically, those who regularly nap were found to be 37 percent less likely to die from a heart attack or other coronary ailment than those who worked straight through the day. This is likely due to reducing stress and lowering blood pressure.",
    "Orcas are the only predators that regularly kill and devour Pacific white-sided dolphins off the B.C. and Washington coasts. So researchers were surprised when drone footage showed such dolphins playing within a few fin-spans of killer whales' toothy jaws. As it turns out, the orcas they play with are of a different species, which are strict pescatarians, and so don't eat dolphins as they are mammals. This still seems like a surprising risk to take, as the two species are nearly identical to our eyes.",
    "NASA answering President Kennedy's challenge and landing men on the moon by 1969 required the most sudden burst of technological creativity, and the largest commitment of resources ($24 billion) ever made by any nation in peacetime. At its peak, the Apollo program employed 400,000 Americans and required the support of over 20,000 industrial firms and universities. In less than 8 years they developed 5 different space craft. i.e. Mercury, Gemini, Apollo service, Apollo command, Lunar Lander. Ultimately 24 people flew to the moon and 12 walked on it. In the 50 years since that time, no human has traveled more than a few hundred miles from Earth.",
    "There are more life forms on human skin than there are people on our planet. There are about a trillion microbes on your skin or in your skin, so more than 100 times the total number of humans on the planet. In fact, the ratio of human cells to microbes in the human body is roughly 1:1.3.",
    "The possibility of dying on your way to buy a lottery ticket is higher than the possibility of actually winning the lottery. You are also more likely to be struck by lightning, or be hit by a falling airplane part in your lifetime than win the lottery. This is because on average the chance of a ticket being the jackpot ticket is 1 in 13,983,816.",
    "It is possible that pessimism is inherited genetically. People can be predisposed to see the world more darkly than others if they have a different variation of the ADRA2b gene. Neuroscientist Professor Rebecca Todd explain: 'A previously known genetic variation causes some individuals to perceive the world more vividly than others - and particularly negative aspects of the world...For example, people who have this variation might look out at a crowd of people and only see angry faces'.",
    "In 1913, upon Edinburgh Zoo's opening, Norway gifted them their first king penguin. Since 1972, the Norwegian King's Guard has adopted 3 penguins, at different time periods, and each was given a rank within the regiment. One of them was even knighted by King Harald V of Norway as Sir Nils Olav III",
    "While the Egyptians were building the pyramids, a colony of Woolly mammoths that had survived, took residence on a small island called Wrangle Island. Mammoths lived there up until around 1,650 BCE, which is nearly 1,000 years after the pyramids were built.",
    "Jack Black is the son of rocket scientists. His parents, Thomas William Black and Judith Love Cohen were satellite engineers who worked on the Hubble Space Telescope. Jack Black joked about his academic parents in a 2003 interview with Newsweek, saying, \"I didn't inherit any of their brainpower. But I have the power to rock. They're rocket scientists. I'm a rock scientist.\"",
    'Ethan Zuckerman invented popup ads in the late 90s while working for Tripod.com. He has since apologized, and thinks it is time online sites and services moved away from using ads altogether. "I have come to believe that advertising is the original sin of the web" he writes in an article for The Atlantic, going on to explain that everything from Facebook tracking us across sites to Google knowing just about everything about you has something to do with advertising.',
    "Green is seen as a symbol of life, but scientists claim that the earliest life on Earth might have been purple. Early life-forms on Earth may have been able to generate metabolic energy from sunlight using a purple-pigmented molecule called retinal that possibly predates the evolution of chlorophyll and photosynthesis. If retinal has evolved on other worlds, it could create a a distinctive biosignature as it absorbs green light in the same way that vegetation on Earth absorbs red and blue light.",
    "The Earth is not a perfect sphere: instead, it is closer to an oblate spheroid. It is pudgier towards the equator, mostly due to the centrifugal force caused by the Earth's rotation. However, it is not a perfect oblate spheroid either. The mass is distributed very unevenly throughout the planet, and the higher the concentration of mass at one location, the stronger the gravitational pull, creating 'bumps' around the globe. Other dynamic factors also influence the shape of the Earth, such as tides (shifting the distribution of water), movement of tectonic plates, mass shifting inside the planet and more.",
    "Nowadays, E-commerce is a dominant market. Who wouldn't want to get anything at the click of a button? However, you'd be surprised that the earliest sale transaction on the internet was of weed. In 1972, long before eBay or Amazon, students from Stanford University in California and MIT in Massachusetts conducted the first ever online transaction. Using the Arpanet account at their artificial intelligence lab, the Stanford students sold their counterparts a tiny amount of marijuana.",
    "Walmart once had over 23,000 applications for 600 jobs in a newly opened store in Washignton DC. With those numbers, the Walmart acceptance rate was at 2.6%. This makes it twice as hard as getting into Harvard and over five times harder than getting into Cornell.",
    "According to the UN's World Happiness Report, Finland has been the world's happiest country for 3 consecutive years as of 2020. The data is based on citizens asked to rate their life from 1 to 10. Interestingly, Finland is closely followed by other European countries such as Denmark, Norway, Iceland, and the Netherlands.",
    r"According to a 2014 study, 12 out of 15 addicts were able to quit smoking through the use of magic mushrooms. For 3 sessions, the chronic smokers were treated with psychedelic mushrooms. Surprisingly, the 80% success rate dwarfed the 35% success rate of leading treatment drugs.",
    "Every year, the town of Lopburi holds a buffet for monkeys. During the Monkey Buffet Festival, the town serves 3000 kgs of fruits and vegetables to the local monkey population of 2,000 crab-eating macaques in Lopburi Province north of Bangkok. The festival was described as one of the strangest festivals by London's Guardian newspaper along with Spain's baby-jumping festival. During that festival, known as El Salto del Colacho (the devil jump), men dressed as the devil in red and yellow suits jump over babies born during the previous twelve months of the year who lie on mattresses in the street. The 'devils' hold whips and oversized castanets as they jump over the infant children.",
    "Rowan Atkinson has made generations laugh at his goofy antics as Mr. Bean. However, the Englishman is actually quite the intellectual. What most people don't know is that Atkinson has a Master's degree in Electrical Engineering from Oxford up his sleeve. His MSc thesis considered the application of self-tuning control. Oxfor also made Atkinson an Honorary Fellow in 2006.",
    "Chlorine is in all of our bodily secretions and excretions. Our body's chlorine levels are almost always parallel to the levels of sodium (due to the makeup of salt i.e. sodium chloride). There is roughly 95g of chlorine in the body, which is enough to disinfect about 8000l of water.",
    "Adrenaline, also known as epinephrine, is a hormone released by our body during stressful situations. This hormone gives us a temporary boost of strength, speed, or basically anything that can help us stay alive. In some cases, adrenaline also keeps us from feeling the pain of fatal wounds. It has even been found that adrenergic hormones, such as adrenaline, can produce retrograde enhancement of long-term memory in humans.",
    r"The Sun accounts for 99.8% of the mass in our solar system with a mass of around 330,000 times that of Earth. The Sun is made up of mostly hydrogen (three quarters worth) with the rest of its mass attributed to helium. It is roughly 4.5 billion years old. Although massive, it is relatively tiny compared to some other stars, and is classified as a yellow dwarf star. For example, UY Scuti, which lies near the center of the Milky Way, is classified as a hypergiant and is 1,708 solar radii (compared to the Sun's 1).",
    "The universe extends far beyond our own galaxy, The Milky Way, which is why scientists can only estimate how many stars are in space.  However, scientists estimate the universe contains approximately 1 septillion (1 followed by 24 zeros!) stars. While no one can actually count every single grain of sand on the earth, the estimated total from researchers at the University of Hawaii, is somewhere around seven quintillion, so there are many more stars in the known universe than grains of sand on Earth.",
    r"In Monopoly, when a player throws doubles (both dice land on the same number) he may take another turn. However, if he throws doubles three times in one turn, then he is considered to be 'speeding' and must go to jail. There is an approximately 0.46% chance of this happening. However, a monopoly game lasts about 20-25 turns, so according to Wolfram Alpha that's about a 7% chance of rolling three doubles in the whole game.",
    r"In terms of land area, the British Empire was the largest empire in recorded history, covering around 26% of the entire world's land surface. However, the Mongol Empire, which comes in at second with around 18% of the world's land surface, was the largest contiguous land empire, and was at its peak roughly 700 years before the British Empire.",
    r"Without a doubt, the greatest conqueror of all time was Genghis Khan, founder of the Mongol Empire. It is estimated that he was responsible for the deaths of up to 11% of the world's population (40 million people). Originally known as Temijin, this son of a Mongol chieftain was given the honorary title of Chinggis Khan when he assumed power, thought to mean 'the oceanic, universal ruler'. He went on to conquer more than double the land than the second greatest conqueror in history, Alexander the Great.",
    r"According to estimates in the Food Waste Index Report 2021 by UNEP, 931 million tonnes of food was wasted globally in 2019, roughly 17% of food produced for human consumption.If food waste were a country, it would be the third-biggest source of greenhouse gas emissions, behind only China and the United States. Individual households were found to be responsible for around 61% of the total, meaning reducing food waste at home could be extremely beneficial for the environment.",
    "Bones of primitive Homo sapiens first appear 300,000 years ago in Africa, with brains as large or larger than ours. They're followed by anatomically modern Homo sapiens at least 200,000 years ago, and brain shape became essentially modern by at least 100,000 years ago. However, tools, artefacts and cave art suggest that complex technology and cultures, 'behavioural modernity', evolved more recently, about 65,000 years ago, and agriculture as we understand it today is believed to have been discovered only 12,000 years ago.",
]

LITERATURE_EXCERPTS = [
    "The Ministry of Truth, which concerned itself with news, entertainment, education and the fine arts. The Ministry of Peace, which concerned itself with war. The Ministry of Love, which maintained law and order. And the Ministry of Plenty, which was responsible for economic affairs. Their names, in Newspeak: Minitrue, Minipax, Miniluv and Miniplenty. - George Orwell, 1984",
    "He found himself understanding the wearisomeness of this life, where every path was an improvisation and a considerable part of one's waking life was spent watching one's feet. - William Golding, Lord of the Flies",
    "Vonnegut could not help looking back, despite the danger of being turned metaphorically into a pillar of salt, into an emblem of the death that comes to those who cannot let go of the past. - Kurt Vonnegut, Slaughterhouse-Five",
    "But I remembered one thing: it wasn't me that started acting deaf; it was people that first started acting like I was too dumb to hear or see or say anything at all. - Ken Kesey, One Flew Over the Cuckoo's Nest",
    "When today fails to offer the justification for hope, tomorrow becomes the only grail worth pursuing. - Arthur Miller, Death of a Salesman",
    "It is far better to endure patiently a smart which nobody feels but yourself, than to commit a hasty action whose evil consequences will extend to all connected with you; and besides, the Bible bids us return good for evil. - Charlotte Bronte, Jane Eyre",
    "As I took another breath, I saw the three stars again. They were not calling to me; they were letting me go, leaving me to the black universe I had wandered for so many lifetimes. I drifted into the black, and it got brighter and brighter. It wasn't black at all-it was blue. Warm, vibrant, brilliant blue... I floated into it with no fear at all. - Stephenie Meyer, The Host",
    "Religion is like language or dress. We gravitate toward the practices with which we were raised. In the end, though, we are all proclaiming the same thing. That life has meaning. That we are grateful for the power that created us. - Dan Brown, Angels & Demons",
    "First, let no one rule your mind or body. Take special care that your thoughts remain unfettered... Give men your ear, but not your heart. Show respect for those in power, but don't follow them blindly. Judge with logic and reason, but comment not. Consider none your superior whatever their rank or station in life. Treat all fairly, or they will seek revenge. Be careful with your money. Hold fast to your beliefs and others will listen. - Christopher Paolini, Eragon",
    "Love, whether newly born or aroused from a deathlike slumber, must always create sunshine, filling the heart so full of radiance, that it overflows upon the outward world. - Nathaniel Hawthorne, The Scarlet Letter",
    "You're both the fire and the water that extinguishes it. You're the narrator, the protagonist, and the sidekick. You're the storyteller and the story told. You are somebody's something, but you are also your you. - John Green, Turtles All the Way Down",
    "When you cannot pinpoint a pain in your body, the whole world seems to throb with it. Trees in pain, lit windows in pain, Wednesday nights in pain. Pianos flaming with pain, and the scale sliding up into a cry. - Patricia Lockwood, Priestdaddy",
    "At an early age, I learned that people make mistakes, and you have to decide if their mistakes are bigger than your love for them. - Angie Thomas, The Hate U Give",
    "Grief was what you owed the dead for the necessary crime of living on without them. - Kamila Shamsie, Home Fire",
    "Grief was the deal God struck with the angel of death, who wanted an unpassable river to separate the living from the dead; grief the bridge that would allow the dead to flit among the living, their footsteps overheard, their laughter around the corner, their posture recognizable in the bodies of strangers you would follow down the street, willing them to never turn around. - Kamila Shamsie, Home Fire",
    "If you are one of those people who has the ability to make it down to the bottom of the ocean, the ability to swim the dark waters without fear, the astonishing ability to move through life's worst crucibles and not die, then you also have the ability to bring something back to the surface that helps others in a way that they cannot achieve themselves. - Lidia Yuknavitch, The Misfit's Manifesto",
    "Her life is architected, elegant and angular, a beauty to behold, and mine is a stew, a juicy, sloppy mess of ingredients and feelings and emotions, too much salt and spice, too much anxiety, always a little dribbling down the front of my shirt. But have you tasted it? It's delicious. Jami Attenberg, All Grown Up",
    "I kept thinking about the uneven quality of time--the way it was almost always so empty, and then with no warning came a few days that felt so dense and alive and real that it seemed indisputable that that was what life was, that its real nature had finally been revealed. But then time passed and unthinkably grew dead again, and it turned out that that fullness had been an aberration and might never come back. - Elif Batuman, The Idiot",
    """My mother died today. Or maybe yesterday, I don't know. I received a telegram from the old people's home: "Mother deceased. Funeral tomorrow. Very sincerely yours." That doesn't mean anything. It might have been yesterday. - Albert Camus, The Stranger""",
    "America was never innocent. We popped our cherry on the boat over and looked back with no regrets. You can't ascribe our fall from grace to any single event or set of circumstances. You can't lose what you lacked at conception. - James Ellroy, American Tabloid",
    "The studio was filled with the rich odour of roses, and when the light summer wind stirred amidst the trees of the garden, there came through the open door the heavy scent of the lilac, or the more delicate perfume of the pink-flowering thorn. - Oscar Wilde, The Picture of Dorian Gray",
    "It is a truth universally acknowledged, that a single man in possession of a good fortune must be in want of a wife. However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered as the rightful property of some one or other of their daughters. - Jane Austen, Pride and Prejudice",
    "I was 37 then, strapped in my seat as the huge 747 plunged through dense cloud cover on approach to Hamburg Airport. Cold November rains drenched the earth. lending everything the gloomy air of a Flemish landscape: the ground crew in waterproofs, a flag atop a squat building, a BMW billboard. So - Germany again. - Haruki Murakami, Norwegian Wood",
    "But who can say what's best? That's why you need to grab whatever chance you have of happiness where you find it, and not worry about other people too much. My experience tells me that we get no more than two or three such chances in a life time, and if we let them go, we regret it for the rest of our lives. - Haruki Murakami, Norwegian Wood",
    "If you only read the books that everyone else is reading, you can only think what everyone else is thinking. - Haruki Murakami, Norwegian Wood",
    "No truth can cure the sorrow we feel from losing a loved one. No truth, no sincerity, no strength, no kindness can cure that sorrow. All we can do is see it through to the end and learn something from it, but what we learn will be no help in facing the next sorrow that comes to us without warning. - Haruki Murakami, Norwegian Wood",
    "Nikki, the name we finally gave my younger daughter, is not an abbreviation; it was a compromise I reached with her father. For paradoxically it was he who wanted to give her a Japanese name and I - perhaps out of some selfish desire not to be reminded of the past - insisted on an English one. - Kazuo Ishiguro, A Pale View of Hills",
    "Her first name was India - she was never able to get used to it. It seemed to her that her parents must have been thinking of someone else when they named her. Or were they hoping for another sort of daughter? As a child she was often on the point of inquiring, but time passed, and she never did. - Evan S. Connell,  Mrs Bridge",
    "For seven years I tried not to remember too much because there was too much to remember, and I didn't want to fall any further behind with the events of my life. I still don't have a vegetable garden. I still haven't been to France. I have gone to bed with enough people that they seem like actual people now, but while I was going to bed with them I thought I was catching up. I am sorry. I had lost what seemed like a lot of time. - Sarah Manguso, The Two Kinds of Decay",
    "Nobody died that year. Nobody prospered. There were no births or marriages. Seventeen reverent satires were written - disrupting a cliche and, presumably, creating a genre. There was a dream, of course, but many of the most important things, I find, are the ones learned in your sleep. Speech, tennis, music, skiing, manners, love - you try them waking and perhaps balk at the jump, and then you're over. - Renata Adler, Speedboat",
    "You don't know about me, without you have read a book by the name of The Adventures of Tom Sawyer, but that ain't no matter. That book was made by Mr Mark Twain, and he told the truth, mainly. There was things he stretched, but mainly he told the truth. That is nothing. - Mark Twain, The Adventures of Huckleberry Finn",
    "About all I know is, I sort of miss everybody I told about. Even old Stradlater and Ackley, for instance. I think I even miss that goddam Maurice. It's funny. Don't ever tell anybody anything. If you do, you start missing everybody. - J.D. Salinger, The Catcher in the Rye",
    """"But soon," he cried with sad and solemn enthusiasm, "I shall die, and what I now feel be no longer felt. Soon these burning miseries will be extinct. I shall ascend my funeral pile triumphantly and exult in the agony of the torturing flames. The light of that conflagration will fade away; my ashes will be swept into the sea by the winds. My spirit will sleep in peace, or if it thinks, it will not surely think thus. Farewell." He sprang from the cabin-window as he said this, upon the ice raft which lay close to the vessel. He was soon borne away by the waves, and lost in darkness and distance. - Mary Shelly, Frankenstein""",
    "So we beat on, boats against the current, borne back ceaselessly into the past. - F. Scott Fitzgerald, The Great Gatsby",
    "There was a white horse, on a quiet winter morning when snow covered the streets gently and was not deep, and the sky was swept with vibrant stars, except in the east, where dawn was beginning in a light blue flood. The air was motionless, but would soon start to move as the sun came up and winds from Canada came charging down the Hudson. - Mark Helprin, A New York Winter's Tale",
    "I must not fear. Fear is the mind-killer. Fear is the little-death that brings total obliteration. I will face my fear. I will permit it to pass over me and through me. And when it has gone past I will turn the inner eye to see its path. Where the fear has gone there will be nothing. Only I will remain. - Frank Herbert, Dune",
    "Stuff your eyes with wonder, he said, live as if you'd drop dead in ten seconds. See the world. It's more fantastic than any dream made or paid for in factories. - Ray Bradbury, Fahrenheit 451",
    "We cannot tell the precise moment when friendship is formed. As in filling a vessel drop by drop, there is at last a drop which makes it run over; so in a series of kindnesses there is at last one which makes the heart run over. - Ray Bradbury, Fahrenheit 451",
    "Don't ask for guarantees. And don't look to be saved in any one thing, person, machine, or library. Do your own bit of saving, and if you drown, at least die knowing you were heading for shore. - Ray Bradbury, Fahrenheit 451",
    "You can tell yourself that you would be willing to lose everything you have in order to get something you want. But it's a catch-22: all of those things you're willing to lose are what make you recognizable. Lose them, and you've lost yourself. - Jodi Picoult, Handle with Care",
    "You have brains in your head. You have feet in your shoes. You can steer yourself any direction you choose. You're on your own. And you know what you know. And YOU are the one who'll decide where to go... - Dr. Seuss, Oh, the Places You'll Go!",
    "I had forgotten that time wasn't fixed like concrete but in fact was fluid as sand, or water. I had forgotten that even misery can end. - Joyce Carol Oates, I Am No One You Know",
    "If you want to know what a man's like, take a good look at how he treats his inferiors, not his equals. - J.K. Rowling, Harry Potter and the Goblet of Fire",
    "We are the music-makers, And we are the dreamers of dreams, Wandering by lone sea-breakers, And sitting by desolate streams. World-losers and world-forsakers, Upon whom the pale moon gleams; Yet we are the movers and shakers, Of the world forever, it seems. - Arthur O'Shaughnessy, Ode",
    "The wide world is all about you: you can fence yourselves in, but you cannot for ever fence it out. - J.R.R. Tolkien, The Fellowship of the Ring",
    "There are many Beths in the world, shy and quiet, sitting in corners till needed, and living for others so cheerfully that no one sees the sacrifices till the little cricket on the hearth stops chirping, and the sweet, sunshiny presence vanishes, leaving silence and shadow behind. - Louisa May Alcott, Little Women",
    "But of course we can't take any credit for our talents. It's how we use them that counts. - Madeleine L'Engle, A Wrinkle in Time: With Related Readings",
    "The rules of the Hunger Games are simple. In punishment for the uprising, each of the twelve districts must provide one girl and one boy, called tributes, to participate. The twenty-four tributes will be imprisoned in a vast outdoor arena that could hold anything from a burning desert to a frozen wasteland. Over a period of several weeks, the competitors must fight to the death. The last tribute standing wins. - Suzanne Collins, The Hunger Games",
    "It does not do to dwell on dreams and forget to live, remember that. Now, why don't you put that admirable Cloak back on and get off to bed? - J.K. Rowling, Harry Potter and the Sorcerer's Stone",
    "Of course it is happening inside your head, Harry, but why on earth should that mean that it is not real? - J.K. Rowling, Harry Potter and the Deathly Hallows",
]

QUOTES = [
    "The greatest glory in living lies not in never falling, but in rising every time we fall. - Nelson Mandela",
    "Your time is limited, so don't waste it living someone else's life. Don't be trapped by dogma - which is living with the results of other people's thinking. - Steve Jobs",
    "If life were predictable it would cease to be life, and be without flavor. - Eleanor Roosevelt",
    "If you look at what you have in life, you'll always have more. If you look at what you don't have in life, you'll never have enough. - Oprah Winfrey",
    "Do not go where the path may lead, go instead where there is no path and leave a trail. - Ralph Waldo Emerson",
    "Tell me and I forget. Teach me and I remember. Involve me and I learn. - Benjamin Franklin",
    "You will face many defeats in life, but never let yourself be defeated. - Maya Angelou",
    "Only a life lived for others is a life worthwhile. - Albert Einstein",
    "Twenty years from now you will be more disappointed by the things that you didn't do than by the ones you did do. So, throw off the bowlines, sail away from safe harbor, catch the trade winds in your sails. Explore, Dream, Discover. - Mark Twain",
    "The mediocre teacher tells. The good teacher explains. The superior teacher demonstrates. The great teacher inspires. - William Arthur Ward",
    "If you can't communicate and talk to other people and get across your ideas, you're giving up your potential. - Warren Buffet",
    "If you can't explain it simply, you don't understand it well enough. - Albert Einstein",
    "A designer knows he or she has achieved perfection, not when there is nothing left to add, but when there is nothing left to take away. - Nolan Haims",
    "Always do right. This will gratify some people and astonish the rest. - Mark Twain",
    "Never doubt that a small group of thoughtful, committed citizens can change the world. Indeed, it is the only thing that ever has. - Margaret Mead",
    "I'm sorry, but I don't want to be an emperor. That's not my business. I don't want to rule or conquer anyone. I should like to help everyone if possible; Jew, Gentile, black man, white. We all want to help one another. Human beings are like that. We want to live by each other's happiness, not by each other's misery. We don't want to hate and despise one another. In this world there is room for everyone, and the good earth is rich and can provide for everyone. - Charlie Chaplain",
    "Remembering that I'll be dead soon is the most important tool I've ever encountered to help me make the big choices in life. Almost everything - all external expectations, all pride, all fear of embarrassment or failure - these things just fall away in the face of death, leaving only what is truly important. - Steve Jobs",
    "No one wants to die. Even people who want to go to heaven don't want to die to get there. And yet, death is the destination we all share. No one has ever escaped it, and that is how it should be, because death is very likely the single best invention of life. It's life's change agent. It clears out the old to make way for the new. - Steve Jobs",
    "We speak not only to tell other people what we think, but to tell ourselves what we think. Speech is a part of thought. - Oliver Sacks",
    "We may not be able to stop evil in the world, but how we treat one another is entirely up to us. - Barack Obama",
    "The quality of mercy is not straind. It droppeth as the gentle rain from heaven upon the place beneath. It is twice blest: it blesseth him that gives and him that take - William Shakespeare, The Merchant of Venice",
    "I love you the more in that I believe you had liked me for my own sake and for nothing else. - John Keats",
    "Let us sacrifice our today so that our children can have a better tomorrow. - A.P.J. Abdul Kalam",
    "The most difficult thing is the decision to act, the rest is merely tenacity. The fears are paper tigers. You can do anything you decide to do. You can act to change and control your life; and the procedure, the process is its own reward. - Amelia Earhart",
    "Do not mind anything that anyone tells you about anyone else. Judge everyone and everything for yourself. - Henry James",
    "Good judgment comes from experience, and a lot of that comes from bad judgment. - Will Rogers",
    "Think in the morning. Act in the noon. Eat in the evening. Sleep in the night. - William Blake",
    "Work like you don't need the money. Love like you've never been hurt. Dance like nobody's watching. - Satchel Paige",
    "If you know the enemy and know yourself, you need not fear the result of a hundred battles. - Sun Tzu, The Art of War",
    "The supreme art of war is to subdue the enemy without fighting. - Sun Tzu, The Art of War",
    "There is only one corner of the universe you can be certain of improving, and that's your own self. - Aldous Huxley",
    "Wise men speak because they have something to say; Fools because they have to say something. - Plato",
    "Always remember that you are absolutely unique. Just like everyone else. - Margaret Mead",
    "The World is my country, all mankind are my brethren, and to do good is my religion. - Thomas Paine",
    "The only true wisdom is in knowing you know nothing. - Socrates",
    "As we express our gratitude, we must never forget that the highest appreciation is not to utter words, but to live by them. - John F. Kennedy",
    "Education is the most powerful weapon which you can use to change the world. - Nelson Mandela",
    "Today you are you! That is truer than true! There is no one alive who is you-er than you! - Dr. Seuss",
    "The only thing necessary for the triumph of evil is for good men to do nothing. - Edmund Burke",
    "Don't judge each day by the harvest you reap but by the seeds that you plant. - Robert Louis Stevenson",
    "It is during our darkest moments that we must focus to see the light. - Aristotle",
    "Where tillage begins, other arts follow. The farmers therefore are the founders of human civilization. - Daniel Webster",
    "Those who cannot remember the past are condemned to repeat it. - George Santayana",
    "The haft of the arrow had been feathered with one of the eagle's own plumes. We often give our enemies the means of our own destruction. - Aesop",
    "The unleashed power of the atom has changed everything save our modes of thinking, and we thus drift toward unparalleled catastrophes. - Albert Einstein",
    "If the brain were so simple we could understand it, we would be so simple we couldn't. - Lyall Watson",
    "Wherever we look, the work of the chemist has raised the level of our civilization and has increased the productive capacity of our nation. - Calvin Coolidge",
    "Better is bread with a happy heart than wealth with vexation. - Amenemope",
    "As soon as men decide that all means are permitted to fight an evil, then their good becomes indistinguishable from the evil that they set out to destroy. - Christopher Dawson",
    "Is it a fact - or have I dreamt it - that, by means of electricity, the world of matter has become a great nerve, vibrating thousands of miles in a breathless point of time? - Nathaniel Hawthorne",
    "The day when two army corps can annihilate each other in one second, all civilized nations, it is to be hoped, will recoil from war and discharge their troops. - Alfred Nobel",
    "A horse, a horse! My kingdom for a horse! - William Shakespeare, Richard III",
    "The press is the best instrument for enlightening the mind of man, and improving him as a rational, moral and social being. - Thomas Jefferson",
    "The speed of communication is wondrous to behold. It is also true that speed can multiply the distribution of information that we know to be untrue. - Edward R. Murrow",
    "There never was a good knife made of bad steel. - Benjamin Franklin",
    "And homeless near a thousand homes I stood, and near a thousand tables pined and wanted food. - William Wordsworth",
    "1. A robot may not injure a human being or, through inaction, allow a human being to come to harm. 2. A robot must obey any orders given to it by human beings, except where such orders would conflict with the First Law. 3. A robot must protect its own existence as long as such protection does not conflict with the First or Second Law. - Isaac Asimov",
    "Pale Death beats equally at the poor man's gate and at the palaces of kings. - Horace",
    "Most of us can, as we choose, make of the world either a palace or a prison. - John Lubbock",
    "We only live to discover beauty. All else is a form of waiting. - Kahlil Gibran",
    "Every genuine work of art has as much reason for being as the earth and the sun. - Ralph Waldo Emerson",
    "Time crumbles things; everything grows old and is forgotten under the power of time. - Aristotle",
    "The true test of civilization is, not the census, nor the size of cities, nor the crops - no, but the kind of man the country turns out. - Ralph Waldo Emerson",
    "He who knows others is wise; He who know himself is enlightened. - Lao Tzu",
    "Whoever desires to found a state and give it laws, must start with assuming that all men are bad and ever ready to display their vicious nature, whenever they may find occasion for it. - Niccolo Machiavelli",
    "In the country of the blind, the one-eyed man is king. - Erasmus",
    "I have a dream that my four little children will one day live in a nation where they will not be judged by the color of their skin but by the content of their character. I have a dream today. - Martin Luther King Jr.",
    "Not everything that counts can be counted, and not everything that can be counted counts. - Albert Einstein",
]


# FUNCTIONS
def get_random_choice(lst: list) -> Generator:
    """
    Generator which shuffles a list of strings and yields one string at a time.
    Text is also stripped of trailing and leading whitespaces.
    """

    random.shuffle(lst)

    for text in lst:
        yield text.strip()


def get_random_text_from_api(fetch_random_text: Function, backup_text: list[str]):
    backup_generator: Generator = get_random_choice(backup_text)

    while True:
        random_api_text: str | None = fetch_random_text()

        yield random_api_text if random_api_text else next(backup_generator)


def get_random_text(text_filename: Path, num_sentences: int) -> Generator:
    """
    Generator which yields a string of a given number of sentences from a given
    text file (text_filename = Path object to .txt file).

    The text is also formatted slightly.
    """

    with open(text_filename) as corpus_text:
        lines = corpus_text.read().splitlines()

    while True:
        rand_int = int(random.random() * (len(lines) - num_sentences))
        rand_sentences = lines[rand_int : rand_int + num_sentences]

        raw_text = " ".join(rand_sentences)
        # Make sure first character is always capitalised if possible
        processed_text = f"{raw_text[0].upper()}{raw_text[1:]}"

        yield processed_text


_translate = {
    "Common Phrases": lambda: get_random_choice(COMMON_PHRASES),
    "Facts": lambda: get_random_text_from_api(FactsApi.get_random_fact, BACKUP_FACTS),
    "Famous Literature Excerpts": lambda: get_random_choice(LITERATURE_EXCERPTS),
    "Famous Quotes": lambda: get_random_choice(QUOTES),
    "Random Text: Brown": lambda: get_random_text(BROWN_TEXT, RANDOM_TEXT_SENTENCES),
    "Random Text: Gutenberg": lambda: get_random_text(
        GUTENBERG_TEXT, RANDOM_TEXT_SENTENCES
    ),
    "Random Text: Webtext": lambda: get_random_text(WEBTEXT_TEXT, RANDOM_TEXT_SENTENCES),
}
