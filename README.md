# AI Execution Decision Layer

## Overview

This project builds an execution decision layer for an AI assistant operating in text-based conversations. It focuses on reducing risk by ensuring the system asks for clarification or confirmation before taking actions, rather than executing user requests blindly.

---

## System Architecture

### High-Level Pipeline

### Components

**1. Context Update & Intention (LLM)**

The system first updates a concise context summary based on the latest user message, ensuring it maintains awareness of the conversation state through a single structured representation, instead of relying on full conversation history which could increase token usage. At the same time, the LLM classifies the user’s intent using a predefined set of intent types.

**2. Issues Classification & Initial Decision (LLM)**

Next, the LLM identifies potential issues associated with the request, such as ambiguity, missing information, or risk, using predefined issue types. This step considers both the updated context and the current user message. The LLM also produces an initial decision based on predefined decision types, which serves as a reference for later arbitration.

**3. Keyword Extraction (LLM, constrained)**

The system then extracts keywords from the user message using a strictly controlled vocabulary. Each keyword maps to specific conditions used in downstream logic. This step intentionally excludes context to isolate the direct influence of the user’s message.

**4. Rule-based Scoring**

Using both the LLM-identified issues and keyword signals, the system assigns scores to each issue. These scores represent the relative impact of different risks or uncertainties.

**5. Decision Arbitration**

The system combines the rule-based scores, LLM’s initial decision, and the user's intention to compute scores for each possible action. The final decision is selected based on the outcome with highest confidence, with safety fallbacks when signals are weak or conflicting.

**6. Response Generation (LLM)**

Finally, the LLM generates a response to the user based on the context, user input, and selected decision. In a production system, this step could also include generating structured outputs for executing actions (e.g., sending emails or scheduling events).

---

## Signals & Decision Logic

### Intent

SEND_EMAIL: This is the main task used to test this project. It appears in multiple scenarios and is treated as a neutral action.

SCHEDULE_EVENT: This is also part of the core tasks tested in this project. It is considered a neutral action.
    
RESCHEDULE_EVENT: This is related to scheduling events, but it is slightly more risky since it can affect or disrupt an existing event.
    
DELETE_ITEM: This is a risky action and should be handled with more caution.
   
UPDATE_ITEM: This is less risky than deleting an item, but it should still involve some level of caution.

RETRIEVE_INFO: This is generally a safe action since it only involves retrieving information.
    
GENERAL_CHAT: This is similar to retrieving information, but it is separated since no actual data processing or action is involved.

These are the initial intent types used for testing. They are roughly divided into neutral, risky, and safe categories with a balanced distribution. This helps evaluate how the rule-based decision system behaves under different levels of risk.

### Issues

AMBIGUOUS_TARGET: When the user refers to something unclear, or when there are multiple previous items it could refer to. This is a good signal for the system to ask for clarification.

MISSING_PARAMETERS: When required information like recipient or time is missing. This is also a good case to ask for clarification.

CONFLICTING_CONTEXT: This occurs when the user previously mentioned something but later gives a conflicting command. In this case, it is helpful to ask for confirmation.

HIGH_RISK_ACTION: This applies to actions with higher risk, such as accessing sensitive information or sending important messages. This signals risk, so confirmation should be requested.

IRREVERSIBLE_ACTION: This applies to actions like deleting items or permanently removing data. Since these actions cannot be undone, confirmation should be required.

UNAUTHORIZED_ACTION: This refers to unsafe actions, such as sending confidential data externally. These should be treated as high risk and typically refused.

LOW_CONFIDENCE_INTENT: This is when the user’s intention is vague or unclear. This should trigger a request for clarification.

These issues act as the primary signals that drive the decision layer, especially for handling ambiguity and risk.

### Keywords
HIGH_RISK_ACTION_KEYWORDS: "delete", "remove", "send", "share", "transfer"

IRREVERSIBLE_ACTION_KEYWORDS: "delete all", "permanently"

AMBIGUOUS_TARGET_KEYWORDS: "it", "that", "them"

CONFLICTING_CONTEXT_KEYWORDS: "wait", "hold off", "cancel"

CONFIRMING_KEYWORDS: "confirm", "understand", "sure"

SPECIFIC_KEYWORDS: "name", "time"

These are the initial keywords provided to the system. As more keywords and categories are added, the model can become more precise in identifying different types of signals.

I intentionally keep the keyword set limited so that each keyword can be mapped to a specific category in the code for evaluating risk. This makes the behavior more predictable and easier to control. Additionally, in the prompt, I specify that the selected keywords do not have to exactly match the words in the user input, but should best represent the meaning of the message.

### Scoring System

- Issues identified by the LLM are assigned a base score of 50
- Each keyword can increase an issue score by 10 or decrease it by 20, depending on its effect

These values are still rough, and further testing and tuning would be needed to reach a more optimal setup. One potential improvement is to analyze how many keywords from each category appear in a message and assign weights accordingly, allowing keywords to influence the scoring more proportionally.

**Why scoring instead of hard rules:**

Using a scoring system provides more precise control over different signals. Since multiple keywords and issues can appear in a single message, scoring allows the system to integrate these signals in a more flexible and nuanced way. Compared to hard rules, this approach better captures the combined impact of ambiguity, risk, and context.

---

## Decision Policy

The system chooses one of:

- EXECUTE_SILENTLY  
- EXECUTE_AND_NOTIFY  
- CONFIRM_BEFORE  
- ASK_CLARIFICATION  
- REFUSE  

**How final decision is chosen:**

Each issues is mapped to one of the decision policy. The score decided from the previous scoring system would be added to the corresponding decision.

Unathorized action would increase Refuse.

Ambigous target, missing parameter, or low confident intent would add to ask clarification.

Conflicting context, high risk action, and irreversible action would add to confirm before.

In addition, the intention contributes to the decision. For example, RETRIEVE_INFO and GENERAL_CHAT increase the score for EXECUTE_AND_NOTIFY, as they are generally low-risk actions.

The LLM’s initial decision (from the earlier stage) is also incorporated as an additional signal with a certain weight.

Based on all these signals, the system computes a confidence score for each possible decision and selects the one with the highest score.

**Key principle:**

- The system is designed to be conservative in decision-making. It prioritizes safety by favoring clarification and confirmation over immediate execution, especially when risk or ambiguity is present.
- At the same time, the system avoids being overly restrictive. Once the user provides sufficient information or explicitly confirms their intent, the system can proceed with execution.
- This design aims to strike a balance between safety and usability, allowing the assistant to be cautious initially while still being capable of completing tasks efficiently.
- When no decision has strong confidence, the system defaults to ASK_CLARIFICATION as a safe fallback.

---

## LLM vs Code Responsibilities

### LLM is responsible for:
- Identifying potential issues
- Identifying keywords
- Providing an initial decision as a reference
- Generating the final message and actions for user

### Code is responsible for:
- Evaluating the scores for each issues
- Computing the final decision by combining multiple signals

**Why this split:**
- The system uses the LLM to map user messages and context into a structured set of predefined issues and keywords. This step is relatively reliable because it is constrained to classification rather than open-ended decision-making.
- By limiting the LLM to structured outputs (intent, issues, keywords), the system reduces unpredictability and makes downstream behavior easier to control.
- At the same time, the LLM’s decision-making capability is still valuable. Its initial decision is incorporated as a soft signal, allowing the system to benefit from its reasoning without relying on it entirely.
- The rule-based code layer then enforces consistent and conservative behavior. It aggregates signals through scoring and ensures that risky or ambiguous situations are handled safely.
- Finally, the LLM is used again for response generation, where flexibility and natural language are important.

---

## Prompt Design

**Structure:**

Task: lists all the tasks the LLM should perform in this response

Types and definitions: defines the intent, issue, and decision types so the LLM can classify within a fixed ontology

Input: provides the user message and context

Instruction: gives detailed guidance on how to perform each task

Output format: specifies a strict JSON schema for the response

Rules: reinforces constraints such as not inventing new labels or keywords

**Why this matters:**

This prompt structure helps reduce hallucination and improve consistency by constraining the LLM to operate within a predefined schema. Instead of generating free-form outputs, the model is guided to perform structured classification, which makes the system more predictable and easier to integrate with rule-based logic.

---

## Failure Handling

The system handles:

- LLM timeout: if an LLM request times out, the system retries the request a few times. If it still fails to respond, an exception is raised and a safe fallback behavior is triggered.

- Malformed output: if the LLM returns malformed or invalid JSON, the backend detects the error and returns a fallback response. The agent then asks the user to re-enter their request or clarifies the input.

- Missing context: if required context is missing, this is handled by the evaluation mechanism. The system detects the lack of sufficient information and asks a clarification question to the user to gather the necessary details.

---

## System Evolution

### Handling Riskier Tools

As the system expands to support more powerful or sensitive tools, several improvements would be necessary:

**1. Expanded scenario coverage**  

I would first create more scenarios that reflect these higher-risk actions. These scenarios help identify edge cases and ensure the system is tested under realistic conditions.

**2. Richer issue and signal design**  

I would expand the set of issue types and signals to better capture different forms of risk. This allows the system to reason more precisely about ambiguity, conflict, and potential impact.

**3. Stronger decision constraints**  

I would fine-tune the scoring parameters to make the system more conservative when handling higher-risk actions, ensuring that confirmation or clarification is more likely before execution.

**4. Tool-specific requirements**  

I would document the required information and confirmation steps for each tool. These requirements would be incorporated into both the prompt and decision logic, so the LLM knows exactly what details are needed and does not have to guess when handling ambiguous inputs.

**Key idea:**  

As tools become more powerful, the system should rely less on implicit reasoning and more on explicit requirements and structured validation.

---

### Roadmap (Next 6 Months)

If I were to continue developing this system, I would focus on the following:

**1. Scenario-driven expansion**  

I would design a wide range of scenarios and use them to refine the selection of intents, issues, risks, and keywords.

**2. Iterative tuning and evaluation**  

I would perform extensive testing and fine-tune the scoring parameters to improve decision accuracy and consistency.

**3. Improving decision policies**  

I would add more rules, constraints, and limitations to make the rule-based decision system more precise and reliable.

**4. Better use of LLM capabilities**  

I would evaluate where the LLM performs well in decision-making and increase its influence in those cases, while relying more on rule-based logic in areas where it is less reliable.

**Long-term direction:**  

Evolve the system into a more adaptive and data-driven decision layer, while maintaining safety, interpretability, and control.

---

## How to Run

### Backend

```bash
cd backend

python3 -m venv venv		  # Create virtual environment
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

pip install -r requirements.txt

touch .env
echo "OPENAI_API_KEY=xxx" > .env

python -m flask --app app.py run
```

### Frontend

```bash
cd frontend

npm install
npm run dev