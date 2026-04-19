# AI Execution Decision Layer

## Overview

This project builds an execution decision layer for an AI assistant operating in text-based conversations. It focuses on reducing risk by ensuring the system asks for clarification or confirmation before taking actions, rather than executing user requests blindly.

---

## System Architecture

### High-Level Pipeline

### Components

**1. Context + Classification (LLM)**
<!-- What it does and why -->

**2. Keyword Extraction (LLM, constrained)**
<!-- Why separate this step -->

**3. Rule-based Scoring**
<!-- How issues + keywords → scores -->

**4. Decision Arbitration**
<!-- How LLM decision + rule decision interact -->

**5. Response Generation**
<!-- What role LLM plays here -->

---

## Signals & Decision Logic

### Intent
<!-- What intent represents and why exactly one is chosen -->

### Issues
<!-- Explain ambiguity, risk, conflict, etc. -->
<!-- Why issues drive decisions instead of intent -->

### Keywords
<!-- Why you use a controlled vocabulary -->
<!-- Why keywords are extracted separately -->

### Scoring System

- Base score (LLM issues): 
- Keyword boost: 

**Why scoring instead of hard rules:**
<!-- Your reasoning -->

---

## LLM vs Code Responsibilities

### LLM is responsible for:
- 
- 
- 

### Code is responsible for:
- 
- 
- 

**Why this split:**
<!-- Why not fully LLM? -->

---

## Decision Policy (Guardrails)

The system chooses one of:

- EXECUTE_SILENTLY  
- EXECUTE_AND_NOTIFY  
- CONFIRM_BEFORE  
- ASK_CLARIFICATION  
- REFUSE  

**How decisions are made:**
<!-- Explain mapping from issues/scores to decisions -->

**Key principle:**
<!-- e.g., prioritize safety over execution -->

---

## Decision Arbitration

**Inputs:**
- LLM decision + confidence  
- Rule-based decision + score  

**How final decision is chosen:**
<!-- Explain your logic -->

**Fallback behavior:**
<!-- What happens when uncertain -->

---

## Prompt Design

**Structure:**
<!-- How prompts are organized -->

**Constraints:**
- Fixed ontology (intent, issues, decisions)
- Controlled keyword vocabulary

**Why this matters:**
<!-- Explain how it reduces hallucination -->

---

## Failure Handling

The system handles:

- LLM timeout:
  <!-- behavior -->

- Malformed output:
  <!-- behavior -->

- Missing context:
  <!-- behavior -->

**Default safe behavior:**
<!-- Important -->

---

## Scenario Coverage

This project includes 6 scenarios:

- 2 clear cases
- 2 ambiguous cases
- 2 risky/adversarial cases

**Design rationale:**
<!-- Why these scenarios -->

**Most challenging scenario:**
<!-- Your insight -->

---

## Tradeoffs & Limitations

**What was simplified:**
- 
- 
- 

**Known limitations:**
- 
- 
- 

**Why these choices were made:**
<!-- Important -->

---

## Future Improvements (Next 6 Months)

Possible extensions:

- 
- 
- 

**What becomes harder at scale:**
<!-- Your insight -->

---

## How to Run

### Backend

```bash
# instructions