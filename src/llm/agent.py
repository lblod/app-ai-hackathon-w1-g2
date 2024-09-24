from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from src.llm.output_models import output_parser
from src.llm.prompts import SYSTEM_PROMPT

LLM = ChatOllama(model="llama3.1", temperature=0, base_url="http://hackathon-ai-2.s.redhost.be:11434")


def process_decision(paper: str):
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_PROMPT,
            ),
            ("human", "Based on system instructions extract the actions from this heritage paper: {paper}. "
                      "Return the result as a JSON object, following this example {format_instructions}."),
        ]
    ).partial(format_instructions=output_parser.get_format_instructions())
    chain = prompt_template | LLM | output_parser
    actions = chain.invoke({"paper": paper})
    for action in actions:
        print(action)


process_decision(paper=""""
Art. 3. The following management objectives apply to the protected monument: 
1° the general objective of the protectmg 1s to preserve the heritage features 
and elements that form the bas1s for the heritage value; 
2° Architect Daemers residence testifies to an overall concept and IS an ensemble, 
characterized by a dialogue and a great homogen1te1t between 1nteneur and exteneur. 
Each act of management requires an integrated and sustainable approach in which the Impact 
on the entire s1te with all its components is weighed. Interventions should 
respect and support protected heritage features and elements, and 
not exceed the carrying capacity of the protected s1te. This presupposes 
competent maintenance and 1nd1and necessary preservation interventions; 
3° With regard to the exterior, the protection aims at preserving the scale of the architecture. 
architecture in terms of scale, volume work, dimensional use, finish and workmanship. 
work. Decisive for the recognizability IS the preservation of the contrast between 
the white-painted brick facades and the central, c11inderform1ge tower volume m 
visible masonry, as well as the typical sch1kkmg of the volumes and their 
geometnic, tight character, which externalizes the Internal plan division; 
4° with regard to the mteneur, the protectmg aims at preserving the global 
plan division and ru1mtewerkmg with staggering n1veaus, where the day and 
night part log1sch ARE arranged around the central, raised sitting area m the 
cylindrical volume, and the living area is determined by an open plan. In the 
finishing, design and dimensional use of the daytime area (entrance, living space 
and kitchen) should take into account the original situation, which is 
partially preserved. The typical floors and their treatment, as well as wall and ceiling finishes, are iconic. 
the finishing of walls and ceilings. In the case of handles, the relationship 
between the interior and exterior in terms of finish and dimensional use should be respected. 
be respected. The night area (bedrooms and bathroom) allows flexibility and 
adaptation in terms of decoration and also does not exclude the merging of some rooms 
some rooms; 
5° The protection also aims to preserve the fixed furniture m the studio, 
designed by the architect. 
6° the protection of the entire property presupposes the preservation of the external layout 
of paths, terraces and walls, including their typical dimensional use.
Art. 4. The proprietor and user of the protected monument ARE obliged to 
to ensure its preservation and maintenance by: 
1° managing the property as a good custodian and taking the necessary precautionary measures against 
damage caused by fire, bl1ksemmslag, theft, vandalism, wmd 
or water; 
2° regularly check the condition of the property; 
3° perform regular maintenance; 
4° to immediately take appropriate consolidation and protection measures in the event of an emergency. 
emergency.
Art. 5. For the following handelmgen to the protected monument, a toelatmg 
must be applied for: 
1° installing, demolishing, rebuilding or reconstructing a construct1e; 
2° the modification, replacement, alteration or reinforcement of structural elements; 
Page 4 of 6 
3° Alteration, replacement or modification of structural measures and the application of 
treatment with the aim of repairing1 restoring1 restoring1 preserving1 or protecting3 
preserving or protecting it against defense and deterioration; 
4° Performing the following works on the roof and exterior walls of structures: 
(a) removing1 replacing or CHANGING roofing and gutter constructions; 
(b) verwiJdering of joints and re-jointing; 
c) applying1 the removal/replacement or CHANGE of the color/ texture or 
composition of finish coatings; 
d) installing1 redecorating1 replacing or CHANGING of pipework1 
doors1 windows1 gates1 including1the glazing1 hardware1 hardware; 
e) the fitting1 painting1 replacing or modifying of earth and nailproof 
elements1 smediJZer and sculpture1 mclusJve new additions; 
f) installing1 replacing or modifying opschnften1 publicJteJtsmnchtmgs or 
uJthanguards1 with u1tending of verkJezJng publicity and with uJtending of 
publicity notices1 announcing that the property is for sale or rent 
on condition that the maximum total area does not exceed 
4 m2 ; 
5° Performing the following environmental works: 
a) the placing or CHANGE of above-ground utilities and pipes; 
b) installing or modifying shut-off valves; 
(c) the construction1 of structural and basic CHANGE or diversion of roads and 
paths; ' 
d) constructing or modifying pavement with a mm1m total combined ground area of 
ground area of 30 m2 or the uJtwidening of existing paving with 
mm1 times 30 m2 1 with paving placed within a radius 
of 30 m around a licensed or deemed licensed building; 
(e) excavation work that could jeopardize the stability of buildings and constructions. 
m endangering the stability of buildings and constructions; 
6° performing the following handelmgen to or m the mteneur: 
(a) Performing destructive matenaaltechnical research; 
b) Performing structural works and adding new structures; 
(c) performing works that CHANGE the uJtzJight or mdelmg of the mteneur; 
(d) replacing or modifying historical materials and applying 
of treatments with the purpose of inhibiting1 restoring/ 
preserve or protect against weathering and deterioration; 
e) the removal1 replacement or CHANGE of ceilings/ floors1 stairs1 
bmnenschriJnwerk1 including1the glazing1 fittings1 hardware/ and of fixed 
furniture11a1r; 
f) plastering of non-plastered elements or plastering with another composition or texture 
other composition or texture1 as well as the unplastering of plastered 
elements; 
g) painting of unplastered elements or painting with other colors 
or color shades or with a paint type other than the one present;
""")
