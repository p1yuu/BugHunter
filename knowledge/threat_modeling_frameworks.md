\# Threat Modeling Frameworks

\## Structured Approaches to Identifying and Reasoning About Risk



\## Purpose

This document defines structured threat modeling methodologies used

to systematically identify, analyze, and prioritize security risks

before exploitation occurs.



Threat modeling focuses on \*design-level\* weaknesses, not exploitation.



---



\## 1. Why Threat Modeling Matters



Threat modeling:

\- Anticipates failures before they happen

\- Reveals architectural weaknesses

\- Reduces reliance on reactive testing

\- Aligns security with system design



It answers:

“What could go wrong, and why?”



---



\## 2. Core Threat Modeling Principles



Effective threat modeling:

\- Starts early (design phase)

\- Is iterative, not one-time

\- Considers attacker goals

\- Focuses on trust boundaries



The goal is understanding, not completeness.



---



\## 3. STRIDE Framework



STRIDE categorizes threats into six classes:



\- \*\*S\*\*poofing: Identity impersonation

\- \*\*T\*\*ampering: Unauthorized modification

\- \*\*R\*\*epudiation: Lack of accountability

\- \*\*I\*\*nformation Disclosure: Data exposure

\- \*\*D\*\*enial of Service: Availability loss

\- \*\*E\*\*levation of Privilege: Unauthorized access



STRIDE is best used to:

\- Systematically question each component

\- Avoid blind spots



---



\## 4. Applying STRIDE Practically



For each system component, ask:

\- Can identity be spoofed here?

\- Can data be altered?

\- Can actions go unlogged?

\- Can sensitive data leak?

\- Can availability be degraded?

\- Can privileges escalate?



The value is in the questioning, not the checklist.



---



\## 5. PASTA Framework (High-Level)



PASTA (Process for Attack Simulation and Threat Analysis) focuses on:

\- Business objectives

\- Threat actors

\- Attack scenarios



PASTA aligns security risks with business impact,

making it useful for executive communication.



---



\## 6. Threat Modeling vs Vulnerability Scanning



Threat modeling:

\- Is proactive

\- Is design-focused

\- Identifies \*potential\* weaknesses



Scanning:

\- Is reactive

\- Is implementation-focused

\- Identifies known issues



Both are complementary.



---



\## 7. Trust Boundaries as Risk Concentrators



Trust boundaries are where:

\- Data changes privilege level

\- Authentication occurs

\- External systems interact



Most serious risks cluster around trust boundaries.



---



\## 8. Data Flow Diagrams (DFDs)



DFDs help visualize:

\- Data movement

\- Processing points

\- Storage locations

\- Trust transitions



Even simple diagrams significantly improve risk discovery.



---



\## 9. Common Threat Modeling Failures



Organizations often:

\- Skip threat modeling due to time

\- Treat it as paperwork

\- Fail to update models as systems change



Outdated models are misleading.



---



\## 10. Role of the AI Assistant



A responsible AI assistant should:

\- Ask structured threat-modeling questions

\- Highlight missing trust boundaries

\- Suggest relevant threat categories

\- Avoid suggesting exploits or attack steps



The assistant supports reasoning,

not execution.



---



\## Key Takeaway



Threat modeling is not about predicting attacks.

It is about understanding how systems fail

when assumptions are violated.



Well-modeled systems fail more gracefully.



