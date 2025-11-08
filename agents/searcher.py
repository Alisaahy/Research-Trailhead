"""
Searcher Agent
Searches literature, assesses novelty/doability, and ranks research ideas
"""

import os
import json
import time
import requests
import google.generativeai as genai


class SearcherAgent:
    def __init__(self):
        """Initialize Searcher Agent"""
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.semantic_scholar_api = "https://api.semanticscholar.org/graph/v1"

    def research_ideas(self, ideas, user_topics):
        """
        Research each idea, assess novelty/doability, rank and return top 3

        Args:
            ideas: List of idea dictionaries from Reader Agent
            user_topics: List of user-selected topics

        Returns:
            Dictionary with top 3 ranked ideas with full details
        """
        scored_ideas = []

        # Process each idea
        for i, idea in enumerate(ideas):
            print(f"Processing idea {i+1}/{len(ideas)}: {idea['title']}")

            # Search for related papers
            papers = self._search_papers(idea)

            # Assess novelty
            novelty_assessment = self._assess_novelty(idea, papers)

            # Assess doability
            doability_assessment = self._assess_doability(idea, papers)

            # Calculate topic match score
            topic_match_score = self._calculate_topic_match(idea, user_topics)

            # Calculate composite score: 30% novelty + 40% doability + 30% topic match
            composite_score = (
                0.3 * novelty_assessment['novelty_score'] +
                0.4 * doability_assessment['doability_score'] +
                0.3 * topic_match_score
            )

            scored_ideas.append({
                'idea': idea,
                'papers': papers[:8],  # Keep top 8 papers
                'novelty_assessment': novelty_assessment,
                'doability_assessment': doability_assessment,
                'topic_match_score': topic_match_score,
                'composite_score': composite_score
            })

            # Rate limiting (Semantic Scholar: 100 req / 5 min)
            # Wait longer between ideas to avoid hitting rate limits
            time.sleep(3)

        # Sort by composite score
        scored_ideas.sort(key=lambda x: x['composite_score'], reverse=True)

        # Select top 3 with diversity check
        top_ideas = self._select_diverse_top_3(scored_ideas)

        # Synthesize literature for top 3
        for item in top_ideas:
            item['literature_synthesis'] = self._synthesize_literature(
                item['idea'],
                item['papers']
            )

        return {
            'top_ideas': top_ideas,
            'total_ideas_analyzed': len(ideas)
        }

    def _search_papers(self, idea, limit=20, max_retries=3):
        """
        Search for related papers using Semantic Scholar API with retry logic

        Returns:
            List of paper dictionaries
        """
        # Construct search query
        query = f"{idea['title']} {idea.get('description', '')[:100]}"

        for attempt in range(max_retries):
            try:
                # Search Semantic Scholar
                url = f"{self.semantic_scholar_api}/paper/search"
                params = {
                    'query': query,
                    'limit': limit,
                    'fields': 'title,abstract,year,citationCount,authors,url'
                }

                response = requests.get(url, params=params, timeout=10)

                # Handle rate limiting with exponential backoff
                if response.status_code == 429:
                    wait_time = (2 ** attempt) * 2  # 2s, 4s, 8s
                    print(f"Rate limited (429). Retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()

                data = response.json()
                papers = data.get('data', [])

                # Filter and format papers
                formatted_papers = []
                for paper in papers:
                    if paper.get('abstract'):
                        formatted_papers.append({
                            'title': paper.get('title', ''),
                            'abstract': paper.get('abstract', ''),
                            'year': paper.get('year'),
                            'citations': paper.get('citationCount', 0),
                            'authors': [a.get('name', '') for a in paper.get('authors', [])[:3]],
                            'url': paper.get('url', '')
                        })

                print(f"Successfully fetched {len(formatted_papers)} papers for: {idea['title'][:50]}")
                return formatted_papers

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429 and attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 2
                    print(f"Rate limited (429). Retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"Error searching papers: {e}")
                    return []
            except Exception as e:
                print(f"Error searching papers: {e}")
                return []

        print(f"Failed to fetch papers after {max_retries} attempts (rate limited)")
        return []

    def _assess_novelty(self, idea, papers):
        """
        Use Claude to assess novelty of research idea

        Returns:
            Dictionary with novelty assessment
        """
        papers_summary = "\n\n".join([
            f"Title: {p['title']}\nYear: {p['year']}\nAbstract: {p['abstract'][:300]}..."
            for p in papers[:10]
        ])

        prompt = f"""Assess the novelty of this research idea based on existing literature.

Research Idea:
Title: {idea['title']}
Description: {idea['description']}

Related Papers Found:
{papers_summary}

Assess:
1. Has this specific idea been extensively explored? (Yes/Partially/No)
2. Research maturity level: Unexplored / Emerging / Active / Saturated
3. What specific gap or unexplored angle does this idea address?
4. Novelty score: Rate 1-5 (1=extensively explored, 5=highly novel)

Return ONLY valid JSON:
{{
  "explored": "Yes/Partially/No",
  "maturity": "Unexplored/Emerging/Active/Saturated",
  "gap": "description of gap",
  "novelty_score": 1-5
}}"""

        try:
            response = self.model.generate_content(prompt)

            content = response.text
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                content = content[json_start:json_end]

            assessment = json.loads(content)
            return assessment

        except Exception as e:
            print(f"Error assessing novelty: {e}")
            return {
                'explored': 'Unknown',
                'maturity': 'Unknown',
                'gap': 'Unable to assess',
                'novelty_score': 3
            }

    def _assess_doability(self, idea, papers):
        """
        Use Gemini to assess doability/feasibility of research idea

        Returns:
            Dictionary with doability assessment
        """
        prompt = f"""Assess the feasibility and doability of this research idea.

Research Idea:
Title: {idea['title']}
Description: {idea['description']}

Based on the idea and typical research resources, assess:
1. Data availability: Are datasets available or need to be collected? (Available/Partially/Need to Collect)
2. Methodology complexity: Can standard methods be used? (Standard/Moderate/Novel Methods Needed)
3. Estimated timeline: (3 months / 6 months / 1 year+)
4. Required expertise: (Undergraduate / Masters / PhD level)
5. Doability score: Rate 1-5 (1=very difficult, 5=highly doable)

Return ONLY valid JSON:
{{
  "data_availability": "Available/Partially/Need to Collect",
  "methodology": "Standard/Moderate/Novel Methods Needed",
  "timeline": "3 months/6 months/1 year+",
  "expertise_level": "Undergraduate/Masters/PhD level",
  "doability_score": 1-5
}}"""

        try:
            response = self.model.generate_content(prompt)

            content = response.text
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                content = content[json_start:json_end]

            assessment = json.loads(content)
            return assessment

        except Exception as e:
            print(f"Error assessing doability: {e}")
            return {
                'data_availability': 'Unknown',
                'methodology': 'Unknown',
                'timeline': 'Unknown',
                'expertise_level': 'Unknown',
                'doability_score': 3
            }

    def _calculate_topic_match(self, idea, user_topics):
        """
        Calculate how well idea matches user's selected topics

        Returns:
            Score from 0-5
        """
        if not user_topics:
            return 3  # Neutral score if no topics

        idea_tags = [tag.lower() for tag in idea.get('topic_tags', [])]
        user_topics_lower = [topic.lower() for topic in user_topics]

        # Count matches
        matches = sum(1 for tag in idea_tags if any(topic in tag or tag in topic for topic in user_topics_lower))

        # Score based on match ratio
        if not idea_tags:
            return 2.5

        match_ratio = matches / max(len(user_topics), 1)
        score = min(match_ratio * 5, 5)

        return score

    def _select_diverse_top_3(self, scored_ideas):
        """
        Select top 3 ideas ensuring diversity (not all similar)

        Returns:
            List of top 3 idea dictionaries
        """
        if len(scored_ideas) <= 3:
            return scored_ideas

        # Simple diversity check: take top idea, then find next ideas with different keywords
        top_3 = [scored_ideas[0]]

        for item in scored_ideas[1:]:
            if len(top_3) >= 3:
                break

            # Check if idea is different enough from already selected
            is_diverse = True
            current_title = item['idea']['title'].lower()

            for selected in top_3:
                selected_title = selected['idea']['title'].lower()
                # Simple diversity check: ensure titles don't share too many words
                current_words = set(current_title.split())
                selected_words = set(selected_title.split())
                common_words = current_words & selected_words
                if len(common_words) > 3:  # More than 3 common words
                    is_diverse = False
                    break

            if is_diverse:
                top_3.append(item)

        # If we didn't get 3 diverse ideas, just take top 3 by score
        if len(top_3) < 3:
            top_3 = scored_ideas[:3]

        return top_3

    def _synthesize_literature(self, idea, papers):
        """
        Synthesize literature for an idea

        Returns:
            Dictionary with synthesized literature information
        """
        papers_text = "\n\n".join([
            f"[{i+1}] {p['title']} ({p['year']})\n{p['abstract'][:200]}..."
            for i, p in enumerate(papers[:8])
        ])

        prompt = f"""Synthesize the literature for this research idea.

Research Idea: {idea['title']}

Related Papers:
{papers_text}

Create a synthesis that includes:
1. A brief overview of what has been done (2-3 sentences)
2. Key papers categorized as: Foundational Work, Recent Advances, or Identifies Gaps
3. What's missing or unexplored
4. Suggested approach (methodology, potential datasets, concrete next steps)

Return ONLY valid JSON:
{{
  "overview": "What has been done...",
  "key_papers": [
    {{"paper_index": 1, "category": "Foundational/Recent/Gap", "summary": "2 sentence summary"}},
    ...
  ],
  "whats_missing": "The specific gap...",
  "suggested_approach": "Concrete next steps..."
}}"""

        try:
            response = self.model.generate_content(prompt)

            content = response.text
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                content = content[json_start:json_end]

            synthesis = json.loads(content)
            return synthesis

        except Exception as e:
            print(f"Error synthesizing literature: {e}")
            return {
                'overview': 'Unable to synthesize',
                'key_papers': [],
                'whats_missing': 'Unable to assess',
                'suggested_approach': 'Unable to provide'
            }
