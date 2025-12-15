# RF-LLM-agent

A Python-based framework that uses a **Large Language Model (LLM)** to assist in the **design and optimization of microstrip patch antennas** in **CST Studio Suite**. This project demonstrates how an LLM can be integrated with automated simulation workflows to iteratively generate, simulate, and refine antenna geometries.

---

## 🚀 Features

- 🤖 **LLM-driven antenna design**  
  Uses in-context learning (ICL) and prompt engineering to guide design iterations. :contentReference[oaicite:1]{index=1}

- 🔄 **Automated simulation loop**  
  Interfaces with CST Studio Suite via VBA macros to run simulations automatically.

- 📊 **S-parameter interpretation**  
  Parses simulated S-parameter results to evaluate antenna performance and guide next steps.

- 🛠 Python scripts for generation, evaluation, and refinement of patch antennas.

---

## 🧠 Motivation

Designing RF antennas typically requires manual iteration between simulation and adjustment. By leveraging a large language model as a design assistant, this project explores a more automated, intelligent workflow that:

1. Suggests design changes  
2. Runs simulations  
3. Interprets the results  
4. Refines the design

This cycle continues until antenna performance improves or design goals are met. :contentReference[oaicite:2]{index=2}

---

## 📁 Repository Contents

| File | Description |
|------|-------------|
| `generate_patch_antenna.py` | Generates candidate microstrip patch geometries. |
| `RF EDA.py` | Core orchestration script linking LLM prompts with simulation & analysis. |
| `S11_results.csv` | Sample S-parameter results from simulations. |
| `Prompt.txt` | Example prompts used for guiding the LLM. |
| `RF EDA Promt (Python).txt` | Prompt template for Python automation. |

*(Adjust this section if files change or you add more scripts.)*

---

## 🛠️ Getting Started

### Requirements
- Python 3.8+
- CST Studio Suite (with access to VBA scripting)
- OpenAI API key (or other LLM provider)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/huxiluxi/RF-LLM-agent.git
   cd RF-LLM-agent
