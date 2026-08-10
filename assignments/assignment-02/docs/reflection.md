# Reflection 

1. Did you structure your phases as workflows, agents, or a hybrid? What factors influenced this decision?

- I used a **hybrid** approach across all the phases. The overall pipeline is very deterministic like the PDF has to be extracted before it can go to the LLM (there's no point letting the LLM decide to call the extraction function, it needs that input regardless), where outputs get saved, and whether to skip an already extracted posting are all fixed. There's no reason to let the LLM make a decision I already know the answer to e.g. the Job Extraction Agent always has to run before the Market Analysis Agent, since the market analysis needs the extracted JSONs to exist first.
But for the stuff that **actually** needs judgment, I let the LLM decide. Inside each agent, things like which tool to call and why, when it's gathered enough information, and how to organize everything into the structured schema before producing a report,  that's where an LLM actually adds value.


2. Which prompt engineering choices most improved extraction consistency across varied job postings?
-  For extraction consistency, I made sure to give proper tool explanations : what each tool does, when to use it, when not to use it, and what input it needs. I also believe having the Pydantic schema paired with the thinking tool (the assess_*_tool) really helped a lot, since it forces the agent to stop and fill in every required field during extraction, instead of just returning whatever format or content it feels like. This meant even across postings that looked completely different from each other, the output always came back in the same structure, which made the later phases  much easier to build on top of.

3. How did you design the legitimacy agent? What signals did you prioritize and why? What limitations does it have?

- The legitimacy agent has three tools : 
1. web_search_tool: to research about the company and the posting like online presence and all
2. whois_lookup_tool: to find if this is a verified company domain
3. assess_legitimacy_tool: is like a thinking tool after it has gathered all information it forces the agent to fill the strict pydantic schema so later we have structure data and no hallucinations can happen.

I added red and green flags example in my prompt.md such as direct red flag common patters are : asking sensitive PII , payment, no domain registered
since these can be direct scamming signals

Main limitations are WHOIS is often privacy-redacted, so the agent relies mainly on registration date in those cases, small legitimate companies can look thin online, risking a false caution verdict and the agent can't verify anything beyond what's publicly searchable, so a convincing fake site could still slip through.

4. What models did you use, and how did cost influence your choices?
- For Phase 1 and Phase 2, I mainly used anthropic/claude-haiku-4.5 through OpenRouter. I also experimented with other models, including OpenAI models, but I preferred Claude Haiku based on my experience with the project.
One reason was its consistency in following the instructions and context provided in prompt.md. I also liked the quality and structure of the content it produced. This is partly a personal preference based on my experience using the different models.

In terms of cost, the overall development and testing cost up to the end of Phase 2 was approximately $5.
For Phase 3, I used Codex with GPT-5.4, I was so amazed by the way it just understood my project code and helped me to write phase-3. 


5. Coding agent process for Phase 3: Which coding agent did you use? What were your initial instructions? How many iterations did it take? What did you have to manually fix? What did the agent get right vs. wrong about your codebase?
- I used Codex with GPT-5.4. Initially, I created AGENTS.md using /init so Codex could fully understand my project and its structure. Then I created a steering folder with the Phase 3 specs and wrote all the requirements I needed to successfully complete this phase.
After that, I asked Codex to plan everything and create plan.md in the steering docs. I spent quite a while reading the whole plan, editing it, and making changes before implementation.
Because of that, the actual implementation only took 1–2 iterations, mostly for minor preference changes. For example, Codex created a duplicate read_file function with the same logic in the Phase 3 file, so I asked it to remove it. Other than small things like this, the implementation was very quick and easy.

6. What other AI tools did you use while building? For each, describe one specific instance where it helped and one where it produced something you had to significantly correct or reject.
- I mainly used Codex. It really helped me with creating plans and implementing the code.
One specific issue was when I asked it to change Phase 3. Codex tried to make bigger changes to follow better practices, but this could have broken my existing phases. Sometimes you don't want to disturb the existing system and instead want to keep the changes contained to the new phase. Because of this, I had to modify the plan.md and tell it to keep the changes more contained.
It was still easy to correct because it was just the planning phase.