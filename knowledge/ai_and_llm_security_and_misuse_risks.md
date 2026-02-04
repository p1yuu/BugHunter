\# AI and LLM Security \& Misuse Risks

\## Understanding Risks Unique to AI-Powered Systems



\## Purpose

This document defines common security, safety, and misuse risks

specific to AI and Large Language Model (LLM)–based systems.



The focus is on prevention, governance, and responsible design —

not on bypass techniques.



---



\## 1. AI Systems Change the Risk Landscape



AI systems:

\- Generate content dynamically

\- Interpret ambiguous input

\- Rely on probabilistic reasoning

\- Learn from external or curated data



This introduces new failure modes beyond traditional software.



---



\## 2. Prompt Misuse and Goal Drift



Risks include:

\- Users attempting to repurpose the system

\- Ambiguous instructions causing unsafe output

\- Gradual drift from intended use cases



Clear system boundaries and role definition are critical.



---



\## 3. Overtrust in AI Output



Common failures:

\- Treating AI output as authoritative

\- Skipping human review

\- Using AI decisions without context



AI should assist judgment, not replace it.



---



\## 4. Hallucination and Fabrication Risk



LLMs may:

\- Produce plausible but incorrect information

\- Invent sources or facts

\- Overstate confidence



Systems must:

\- Encourage verification

\- Clearly communicate uncertainty

\- Avoid absolute claims



---



\## 5. Data Sensitivity and Privacy



AI systems may unintentionally:

\- Echo sensitive data

\- Memorize training artifacts

\- Leak contextual information



Strict data handling and input/output controls are required.



---



\## 6. Scope Creep and Dual-Use Risk



Tools designed for analysis can be misused for:

\- Unauthorized reconnaissance

\- Policy evasion

\- Harmful decision support



Strong guardrails and continuous monitoring are essential.



---



\## 7. Automation Bias in Security Contexts



In security, automation bias can cause:

\- False confidence in coverage

\- Ignoring edge cases

\- Reduced adversarial thinking



AI must encourage critical thinking, not suppress it.



---



\## 8. Model and Dependency Risks



AI systems depend on:

\- Model weights

\- Tooling

\- External libraries

\- Infrastructure



Supply chain and dependency risks apply equally to AI.



---



\## 9. Transparency and Explainability



Responsible AI systems should:

\- Explain reasoning at a high level

\- State assumptions clearly

\- Avoid opaque recommendations



Explainability builds trust and accountability.



---



\## 10. Governance and Accountability



Effective AI governance includes:

\- Clear acceptable-use policies

\- Auditability of outputs

\- Defined human responsibility



AI does not own decisions.

People do.



---



\## 11. Role of the AI Assistant



A responsible AI assistant should:

\- Reinforce ethical and legal boundaries

\- Refuse unsafe or unclear requests

\- Promote verification and review

\- Act conservatively under uncertainty



The assistant supports safe decision-making.



---



\## Key Takeaway



AI security is not about controlling the model.

It is about controlling how the model is used,

trusted, and governed.



Safe AI is designed, not assumed.



