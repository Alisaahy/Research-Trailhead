"""
Profiler Agent
Analyzes user descriptions and creates structured research profiles
"""

import os
import json
import google.generativeai as genai


class ProfilerAgent:
    def __init__(self):
        """Initialize Profiler Agent with Gemini API"""
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def analyze_description(self, description, experience_level=None):
        """
        Analyze user's manual description and create structured profile

        Args:
            description: User's text description of their research background
            experience_level: Optional pre-selected experience level

        Returns:
            Dictionary with structured profile
        """
        prompt = f"""You are a research profile analyzer. Analyze this researcher's description and create a structured profile.

RESEARCHER'S DESCRIPTION:
{description}

{f'STATED EXPERIENCE LEVEL: {experience_level}' if experience_level else ''}

Extract and infer the following information, returning ONLY valid JSON:

{{
  "expertise_level": "Undergraduate Student" | "PhD Student" | "Postdoc" | "Assistant Professor" | "Associate/Full Professor" | "Industry Researcher",
  "research_areas": ["area1", "area2", ...],  // 3-5 broad areas (e.g., "Natural Language Processing", "Computer Vision")
  "specific_topics": ["topic1", "topic2", ...],  // 5-10 specific topics (e.g., "Transformers", "Few-shot Learning")
  "technical_skills": ["skill1", "skill2", ...],  // Technical skills/tools mentioned (e.g., "PyTorch", "TensorFlow")
  "research_style": "Empirical" | "Theoretical" | "Applied" | "Mixed",  // Infer from description
  "resource_access": "Limited" | "Moderate" | "Extensive",  // Infer from position/institution
  "publication_count": 0,  // Estimate if mentioned, otherwise 0
  "h_index": 0,  // Estimate if mentioned, otherwise 0
  "novelty_preference": 0.5,  // 0-1, infer willingness to pursue novel/risky ideas
  "doability_preference": 0.7  // 0-1, infer preference for practical/doable projects
}}

GUIDELINES:
- For research_areas: Extract broad fields like "Machine Learning", "Bioinformatics", "Robotics"
- For specific_topics: Extract specific methods, models, or subfields mentioned
- For technical_skills: Include frameworks, languages, tools explicitly mentioned
- For research_style:
  * "Empirical": Focus on experiments, datasets, benchmarks
  * "Theoretical": Focus on proofs, algorithms, mathematical foundations
  * "Applied": Focus on real-world applications, systems
  * "Mixed": Combination of above
- For resource_access:
  * "Limited": Undergrad/early PhD, no mention of compute resources
  * "Moderate": PhD student/postdoc at known institution
  * "Extensive": Professor, industry researcher, mentions large compute
- For novelty_preference: Higher if they mention "novel", "innovative", "breakthrough"; lower if they mention "practical", "incremental"
- For doability_preference: Higher if they mention "feasible", "practical", "implementable"; lower if they're open to ambitious projects

Return ONLY the JSON object, no other text."""

        try:
            response = self.model.generate_content(prompt)

            # Parse JSON from response
            content = response.text
            json_start = content.find('{')
            json_end = content.rfind('}') + 1

            if json_start >= 0 and json_end > json_start:
                profile_json = content[json_start:json_end]
                profile = json.loads(profile_json)

                # Override expertise_level if provided
                if experience_level:
                    profile['expertise_level'] = experience_level

                return profile
            else:
                raise ValueError("No valid JSON found in response")

        except Exception as e:
            print(f"Error analyzing profile: {str(e)}")
            # Return default profile
            return {
                "expertise_level": experience_level or "PhD Student",
                "research_areas": ["Machine Learning"],
                "specific_topics": [],
                "technical_skills": [],
                "research_style": "Mixed",
                "resource_access": "Moderate",
                "publication_count": 0,
                "h_index": 0,
                "novelty_preference": 0.5,
                "doability_preference": 0.7
            }

    def analyze_scholar_data(self, scholar_data):
        """
        Analyze Google Scholar data and create structured profile

        Args:
            scholar_data: Dictionary with scholar profile data
                {
                    "name": str,
                    "affiliation": str,
                    "interests": [str],
                    "publications": [{title, year, citations, venue}],
                    "h_index": int,
                    "total_citations": int
                }

        Returns:
            Dictionary with structured profile
        """
        # Format publications for the prompt
        pub_summary = "\n".join([
            f"- {pub['title']} ({pub.get('year', 'N/A')}) - {pub.get('citations', 0)} citations"
            for pub in scholar_data.get('publications', [])[:10]  # Top 10 papers
        ])

        prompt = f"""You are a research profile analyzer. Analyze this researcher's Google Scholar profile and create a structured profile.

RESEARCHER PROFILE:
Name: {scholar_data.get('name', 'Unknown')}
Affiliation: {scholar_data.get('affiliation', 'Unknown')}
H-Index: {scholar_data.get('h_index', 0)}
Total Citations: {scholar_data.get('total_citations', 0)}
Stated Interests: {', '.join(scholar_data.get('interests', []))}

TOP PUBLICATIONS:
{pub_summary}

Based on this publication record, infer and return ONLY valid JSON:

{{
  "expertise_level": "PhD Student" | "Postdoc" | "Assistant Professor" | "Associate/Full Professor" | "Industry Researcher",
  "research_areas": ["area1", "area2", ...],  // Extract from publication venues/topics
  "specific_topics": ["topic1", "topic2", ...],  // Extract from paper titles and interests
  "technical_skills": ["skill1", "skill2", ...],  // Infer from methodologies in papers
  "research_style": "Empirical" | "Theoretical" | "Applied" | "Mixed",
  "resource_access": "Limited" | "Moderate" | "Extensive",  // Infer from affiliation and publication venues
  "publication_count": {len(scholar_data.get('publications', []))},
  "h_index": {scholar_data.get('h_index', 0)},
  "novelty_preference": 0-1,  // Infer from publication pattern and venues
  "doability_preference": 0-1  // Infer from publication frequency and scope
}}

INFERENCE GUIDELINES:
- expertise_level: Infer from h-index, citation count, affiliation
  * H-index < 5: PhD Student
  * H-index 5-15: Postdoc or early Assistant Prof
  * H-index 15-30: Assistant/Associate Prof
  * H-index > 30: Senior Professor
  * Adjust based on affiliation (industry suggests "Industry Researcher")
- research_areas: Look at publication venues (NeurIPS→ML, ACL→NLP, CVPR→CV)
- specific_topics: Extract key concepts from paper titles
- technical_skills: Infer tools/frameworks from publication style and venues
- research_style: Infer from paper types (empirical benchmarks vs theory papers)
- resource_access: Consider affiliation prestige and publication scale
- novelty_preference: Higher if publishing in top venues with novel contributions
- doability_preference: Higher if consistent publication record (suggests practical approach)

Return ONLY the JSON object, no other text."""

        try:
            response = self.model.generate_content(prompt)

            # Parse JSON from response
            content = response.text
            json_start = content.find('{')
            json_end = content.rfind('}') + 1

            if json_start >= 0 and json_end > json_start:
                profile_json = content[json_start:json_end]
                profile = json.loads(profile_json)
                return profile
            else:
                raise ValueError("No valid JSON found in response")

        except Exception as e:
            print(f"Error analyzing scholar profile: {str(e)}")
            # Return default profile based on h-index
            h_index = scholar_data.get('h_index', 0)
            if h_index < 5:
                expertise = "PhD Student"
            elif h_index < 15:
                expertise = "Postdoc"
            elif h_index < 30:
                expertise = "Assistant Professor"
            else:
                expertise = "Associate/Full Professor"

            return {
                "expertise_level": expertise,
                "research_areas": scholar_data.get('interests', ["Machine Learning"])[:3],
                "specific_topics": [],
                "technical_skills": [],
                "research_style": "Mixed",
                "resource_access": "Moderate",
                "publication_count": len(scholar_data.get('publications', [])),
                "h_index": h_index,
                "novelty_preference": 0.5,
                "doability_preference": 0.7
            }
