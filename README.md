![GitHub Repo](https://img.shields.io/badge/Research-Paper-blue)
# **Enhancing Q&A Communities with Knowledge-Augmented Generation: An LLM-Based Framework for Fast and Accurate Responses**

## 📜 Overview
<p align="center">
This study introduces a knowledge-augmented generation approach for answering questions in Q&A communities, which comprises two main components: user knowledge modeling, with a fine-tuned Llama-2 as its backbone, and personalized answer generation, built on a pre-trained GPT-4o. As depicted in Fig. 1, the first component retrieves each user's past questions and analyzes them to identify the topics they are most interested in or engage with frequently. Specifically, for each question in the user's activity history, a Llama-2 model generates a sequence of thematic tags. These tags are then aggregated, sorted by term frequency, and concatenated into a unified sequence encapsulating the user's favored topics. This process is executed offline, with the final representations stored in a database and updated periodically. When a new question arises, the second component uses the user's knowledge alongside the task description and question body to prompt a GPT-4o model. 
</p>
<p align="center"><img src="./ProposedFramework.jpg" width="700"></p>
<p align="center"><b> Fig 1. </b> Overview of the proposed knowledge-augmented generation approach</p>
