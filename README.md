<p align="center">
  <img src="docs/image/orion-logo.png" alt="ORION Logo" width="200">
</p>

# ORION  
### Offensive Recon Intelligence Engine

ORION is an offensive reconnaissance tool focused on **decision-making**, not raw data collection.

It automates attack surface discovery, correlates technical signals, and applies intelligence to **prioritize assets, reduce noise, and explain why something matters**, assisting pentesters and bug bounty hunters during the most critical phase of an engagement: Recon.

---

## Overview

Modern reconnaissance tools generate massive amounts of data but leave the hardest part to the operator:  
**deciding what is actually worth attacking**.

ORION was designed to bridge this gap.

Instead of acting as another enumerator, ORION behaves like a **technical assistant**, analyzing reconnaissance data from an offensive perspective and helping the operator focus on assets with real potential.

It does not replace existing tools.  
It **orchestrates, interprets, and prioritizes their output**.

---

## Core Objectives

- Automate reconnaissance without losing context  
- Reduce noise and false positives  
- Prioritize assets with higher offensive potential  
- Provide explainable reasoning behind decisions  
- Help the operator decide **where to continue** and **where to stop**

ORION is built for professionals who already understand Recon and want to execute it more efficiently and strategically.

---

## How ORION Works

1. Receives a target domain as input  
2. Performs passive and active attack surface enumeration  
3. Collects technical signals:
   - DNS
   - HTTP behavior
   - Headers
   - Technology stack fingerprints
   - Infrastructure patterns
4. Correlates findings across assets  
5. Assigns an **Attack Interest Score** to each asset  
6. Explains why each asset was classified that way  
7. Suggests logical next reconnaissance steps  

The focus is not volume of output, but **actionable intelligence**.

---

## Key Features

- Advanced subdomain enumeration  
- Service and technology fingerprinting  
- Detection of environmental inconsistencies  
- Identification of staging, testing, and legacy environments  
- Context-aware dynamic wordlist generation  
- Asset prioritization based on offensive heuristics  
- Explainable scoring (no black-box decisions)  
- Assistant mode for guided Recon decisions  

---

## Attack Interest Score

Each discovered asset receives an **Attack Interest Score**, calculated using:

- Subdomain naming patterns  
- Stack and configuration inconsistencies  
- Exposed or misconfigured headers  
- Behavioral anomalies  
- Infrastructure and hosting context  
- Offensive heuristics based on real-world pentesting experience  

Every score is accompanied by a **clear explanation**, allowing the operator to understand and trust the prioritization logic.

---

## Use of Artificial Intelligence

AI in ORION is **assistive**, not authoritative.

It is used to:
- Explain complex technical findings  
- Correlate multiple weak signals into meaningful insights  
- Suggest logical next reconnaissance actions  
- Translate technical noise into human-readable reasoning  

All critical decisions remain deterministic and transparent.

---

## Interface Design

- CLI-first  
- Automation-friendly  
- OPSEC-aware  
- Clean, minimal, and focused output  
- Quiet mode for scripting and pipelines  

---

## Use Cases

- Bug bounty reconnaissance  
- Professional pentesting  
- Red Team operations  
- Large-scale attack surface mapping  
- Recon automation with human guidance  

---

## Roadmap (Planned Ideas)

- Recon profiles (bug bounty, red team, audit)  
- Learning from previous executions  
- Optional visualization layer  
- Professional reporting integration  
- Local offensive knowledge base  

---

## Ethical and Legal Notice

This project is intended **strictly for legal and authorized security testing**.

Use ORION only on:
- Assets you own  
- Authorized bug bounty programs  
- Formal and permitted pentesting engagements  

The author assumes no responsibility for misuse.

---

## Philosophy

Recon is not about collecting everything.  
It is about understanding **where it is worth looking**.
