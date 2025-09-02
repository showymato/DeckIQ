import json
import re

class TemplateChecker:
    def __init__(self):
        self.templates = self._load_templates()

    def _load_templates(self):
        """Load benchmark templates for comparison"""
        templates = {}

        # Y Combinator Template (Based on YC's standard format)
        templates['y_combinator'] = {
            'required_sections': [
                'problem',
                'solution', 
                'market',
                'traction',
                'business model',
                'competition',
                'team',
                'financials',
                'ask',
                'use of funds'
            ],
            'optional_sections': [
                'demo',
                'product roadmap', 
                'partnerships',
                'go-to-market',
                'risks'
            ],
            'description': 'Y Combinator standard pitch deck format focusing on problem-solution fit and traction'
        }

        # Sequoia Capital Template (Based on Sequoia's pitch guide)
        templates['sequoia_capital'] = {
            'required_sections': [
                'company purpose',
                'problem',
                'solution',
                'market size',
                'competition',
                'product',
                'business model',
                'team',
                'financial model',
                'funding ask'
            ],
            'optional_sections': [
                'go-to-market strategy',
                'technology',
                'risks and mitigation',
                'timeline',
                'partnerships'
            ],
            'description': 'Sequoia Capital pitch deck framework emphasizing market opportunity and execution'
        }

        return templates

    def check_template_gaps(self, deck_text, template_name):
        """
        Check what sections are missing from the deck compared to template
        Returns list of missing required sections
        """
        if template_name not in self.templates:
            return []

        template = self.templates[template_name]
        deck_lower = deck_text.lower()
        missing = []

        for section in template['required_sections']:
            # Get keywords for this section
            keywords = self._get_section_keywords(section)

            # Check if any keywords are found in the deck
            section_found = False
            for keyword in keywords:
                if keyword.lower() in deck_lower:
                    section_found = True
                    break

            if not section_found:
                missing.append(section.title())

        return missing

    def get_template_info(self, template_name):
        """Get template information"""
        return self.templates.get(template_name, {})

    def _get_section_keywords(self, section):
        """
        Get keywords to search for each section type
        More comprehensive keyword matching for better detection
        """
        keyword_map = {
            # Problem section keywords
            'problem': [
                'problem', 'pain point', 'challenge', 'issue', 'difficulty',
                'struggle', 'frustration', 'barrier', 'obstacle', 'gap'
            ],

            # Solution section keywords  
            'solution': [
                'solution', 'product', 'approach', 'how we', 'our platform',
                'we solve', 'we built', 'we created', 'our technology'
            ],

            # Market section keywords
            'market': [
                'market', 'tam', 'addressable', 'opportunity', 'market size',
                'industry', 'sector', 'customers', 'target market'
            ],

            # Traction section keywords
            'traction': [
                'traction', 'growth', 'users', 'customers', 'revenue',
                'metrics', 'kpis', 'milestones', 'progress', 'momentum'
            ],

            # Business model keywords
            'business model': [
                'business model', 'revenue', 'pricing', 'monetization',
                'how we make money', 'revenue streams', 'subscription'
            ],

            # Competition keywords
            'competition': [
                'competition', 'competitive', 'competitors', 'vs', 'compared to',
                'alternatives', 'differentiation', 'advantage'
            ],

            # Team section keywords
            'team': [
                'team', 'founder', 'ceo', 'experience', 'background',
                'leadership', 'advisors', 'employees', 'staff'
            ],

            # Financial keywords
            'financials': [
                'financial', 'revenue', 'projections', 'forecast',
                'profit', 'loss', 'cash flow', 'burn rate'
            ],

            # Funding ask keywords
            'ask': [
                'funding', 'raise', 'investment', 'capital', 'round',
                'asking for', 'seeking', 'need'
            ],

            # Use of funds keywords
            'use of funds': [
                'use of funds', 'allocation', 'spend', 'budget',
                'how we will use', 'investment will go'
            ],

            # Company purpose keywords
            'company purpose': [
                'mission', 'vision', 'purpose', 'why', 'our goal',
                'we believe', 'our mission'
            ],

            # Market size specific keywords
            'market size': [
                'market size', 'tam', 'sam', 'som', 'addressable market',
                'billion', 'million', 'market opportunity'
            ],

            # Product keywords
            'product': [
                'product', 'features', 'demo', 'technology', 'platform',
                'software', 'app', 'service', 'offering'
            ],

            # Financial model keywords
            'financial model': [
                'financial model', 'unit economics', 'metrics', 'ltv',
                'cac', 'gross margin', 'operating margin'
            ]
        }

        # Return keywords for the section, or the section name itself as fallback
        return keyword_map.get(section, [section])

    def get_all_templates(self):
        """Return all available templates"""
        return list(self.templates.keys())

    def calculate_coverage_score(self, deck_text, template_name):
        """Calculate what percentage of required sections are covered"""
        if template_name not in self.templates:
            return 0

        template = self.templates[template_name]
        total_sections = len(template['required_sections'])
        missing_sections = len(self.check_template_gaps(deck_text, template_name))

        coverage = ((total_sections - missing_sections) / total_sections) * 100
        return round(coverage, 1)
