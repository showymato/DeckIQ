import google.generativeai as genai
import streamlit as st
import time
import random

class GeminiHelper:
    def __init__(self, model, model_name):
        self.model = model
        self.model_name = model_name
        self.max_retries = 3
        self.base_delay = 1

    def _generate_with_retry(self, prompt, max_length=30000):
        """Generate content with retry logic and error handling"""
        for attempt in range(self.max_retries):
            try:
                # Truncate content if too long
                if len(prompt) > max_length:
                    prompt = prompt[:max_length] + "\n\n[Content truncated due to length]"

                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        max_output_tokens=4000,
                        top_p=0.8,
                        top_k=40
                    )
                )

                if response.text:
                    return response.text
                else:
                    return "Error: No response generated. Please try again."

            except Exception as e:
                error_msg = str(e).lower()

                # Handle specific error types
                if "quota" in error_msg or "rate limit" in error_msg:
                    if attempt < self.max_retries - 1:
                        wait_time = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
                        st.warning(f"Rate limit reached. Waiting {wait_time:.1f} seconds before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        return "Error: API quota exceeded. Please try again later or check your API limits."

                elif "404" in error_msg or "not found" in error_msg:
                    return f"Error: Model {self.model_name} not available. Please check your API configuration."

                elif "authentication" in error_msg or "invalid" in error_msg:
                    return "Error: Invalid API key. Please check your Google Gemini API key."

                elif "network" in error_msg or "connection" in error_msg:
                    if attempt < self.max_retries - 1:
                        st.warning(f"Network issue. Retrying... (Attempt {attempt + 2}/{self.max_retries})")
                        time.sleep(2)
                        continue
                    else:
                        return "Error: Network connection failed. Please check your internet connection."

                else:
                    if attempt < self.max_retries - 1:
                        st.warning(f"Unexpected error. Retrying... (Attempt {attempt + 2}/{self.max_retries})")
                        time.sleep(1)
                        continue
                    else:
                        return f"Error: {str(e)}. Please try again or contact support."

        return "Error: Failed after multiple attempts. Please try again later."

    def generate_structure(self, deck_text):
        """Generate structured outline with enhanced prompting"""
        prompt = f"""
        You are an expert startup advisor. Analyze this pitch deck content and create a professional, investor-ready structured outline.

        **INSTRUCTIONS:**
        - Reorganize the content into clear sections that follow investor expectations
        - Use the actual information provided, don't make up details
        - If information is missing for a section, indicate "Not specified in current deck"
        - Be specific and actionable in your recommendations
        - Format using markdown headers and bullet points

        **REQUIRED STRUCTURE:**

        ## 📊 RESTRUCTURED PITCH DECK

        ### 1. 🎯 PROBLEM
        - What specific pain point are you solving?
        - Who experiences this problem?
        - How urgent/expensive is this problem?

        ### 2. 💡 SOLUTION
        - Your unique approach to solving the problem
        - Key features/capabilities
        - Why your solution is different/better

        ### 3. 🌍 MARKET OPPORTUNITY
        - Total Addressable Market (TAM)
        - Target customer segments
        - Market trends supporting your solution

        ### 4. 📈 TRACTION & VALIDATION
        - Key metrics and milestones achieved
        - Customer testimonials/case studies
        - Revenue/user growth data

        ### 5. 💰 BUSINESS MODEL
        - How you make money
        - Pricing strategy
        - Revenue streams

        ### 6. ⚔️ COMPETITIVE ADVANTAGE
        - Key competitors and how you're different
        - Your unfair advantages
        - Barriers to entry you've built

        ### 7. 👥 TEAM
        - Founder backgrounds and expertise
        - Key team members and advisors
        - Why this team can execute

        ### 8. 📊 FINANCIAL PROJECTIONS
        - Revenue projections (3-5 years)
        - Key financial metrics
        - Path to profitability

        ### 9. 💸 FUNDING ASK
        - How much you're raising
        - Use of funds breakdown
        - Expected milestones with this funding

        **PITCH DECK CONTENT:**
        {deck_text}

        **OUTPUT FORMAT:**
        - Use clear, professional language
        - Include specific numbers/metrics where mentioned
        - Make it investor-focused and compelling
        - Use bullet points for readability
        """

        return self._generate_with_retry(prompt)

    def generate_pitch_script(self, deck_text):
        """Generate compelling pitch script"""
        prompt = f"""
        Create a compelling 2-minute founder pitch script based on this deck content. You are an expert pitch coach helping a startup founder.

        **SCRIPT REQUIREMENTS:**

        **Structure & Timing:**
        - **Hook (0-15 sec)**: Grab attention with compelling opening
        - **Problem (15-30 sec)**: Paint the pain point vividly
        - **Solution (30-60 sec)**: Your unique approach and key benefits
        - **Traction (60-90 sec)**: Proof points and momentum
        - **Ask (90-120 sec)**: Clear funding request and vision

        **Writing Style:**
        - Conversational and confident tone
        - Include specific metrics and numbers from the deck
        - Use storytelling elements
        - End with memorable call-to-action
        - Add timing and emphasis cues

        **FORMAT:**

        # 🎤 YOUR 2-MINUTE PITCH SCRIPT

        ## Opening Hook (0-15 seconds)
        [Your compelling opening that grabs attention...]

        ## Problem Statement (15-30 seconds)
        [Paint the problem vividly with real impact...]

        ## Solution Demo (30-60 seconds)
        [Show your solution and key differentiators...]

        ## Traction Proof (60-90 seconds)
        [Share your momentum and validation...]

        ## The Ask (90-120 seconds)
        [Clear funding request and exciting vision...]

        ---
        **💡 Delivery Tips:**
        - Maintain eye contact with investors
        - Use confident body language
        - Practice timing with a stopwatch
        - End with enthusiasm and clear next steps

        **DECK CONTENT:**
        {deck_text}

        Remember: Use only the information provided in the deck content. If key information is missing, note it as "[Add specific detail about X]" in the script.
        """

        return self._generate_with_retry(prompt)

    def generate_design_suggestions(self, deck_text):
        """Generate modern design recommendations"""
        prompt = f"""
        You are a professional presentation designer. Provide specific, actionable slide design recommendations for this pitch deck based on current 2024-2025 investor presentation best practices.

        **ANALYSIS REQUIRED:**

        ## 🎨 DESIGN ANALYSIS & RECOMMENDATIONS

        ### 1. 📐 VISUAL HIERARCHY & TYPOGRAPHY
        **Font Recommendations:**
        - Header fonts: [Specific font suggestions]
        - Body text fonts: [Readable options]
        - Font sizes for different slide types

        **Layout Principles:**
        - Slide composition guidelines
        - White space usage
        - Visual flow improvements

        ### 2. 🎨 COLOR PALETTE & BRANDING
        **Professional Color Schemes:**
        - Primary brand colors (2-3 max)
        - Supporting colors for charts/data
        - High contrast for readability

        **Industry Standards:**
        - Colors that work in investor presentations
        - Accessibility considerations
        - Print-friendly options

        ### 3. 📊 DATA VISUALIZATION
        **Chart Improvements:**
        - Best chart types for different data
        - Color coding strategies
        - Making numbers more impactful

        **Visual Metaphors:**
        - Icons and illustrations
        - Infographic opportunities

        ### 4. 🖼️ IMAGERY & GRAPHICS
        **Professional Standards:**
        - High-quality imagery guidelines
        - Avoiding cliché stock photos
        - Brand-consistent visual style

        ### 5. 📱 MODERN TRENDS (2024-2025)
        **Current Best Practices:**
        - Minimalist vs detailed approaches
        - Interactive elements for digital presentation
        - Mobile-friendly considerations

        ### 6. 🎯 SLIDE-SPECIFIC RECOMMENDATIONS
        Based on the content provided, give specific suggestions for:
        - Title/cover slides
        - Problem/solution slides
        - Market size visualization
        - Traction/metrics slides
        - Team introduction slides
        - Financial projection slides

        **DECK CONTENT:**
        {deck_text}

        **OUTPUT REQUIREMENTS:**
        - Provide specific, actionable recommendations
        - Include rationale for each suggestion
        - Focus on investor presentation standards
        - Consider both digital and print formats
        """

        return self._generate_with_retry(prompt)

    def generate_benchmark_analysis(self, deck_text, missing_elements, template_name):
        """Generate comprehensive benchmark analysis"""
        prompt = f"""
        You are a seasoned venture capital advisor. Conduct a comprehensive benchmark analysis of this pitch deck against {template_name} investment standards.

        **ANALYSIS FRAMEWORK:**

        ## 📊 BENCHMARK ANALYSIS REPORT

        **Template Standard:** {template_name}
        **Missing Critical Elements:** {', '.join(missing_elements) if missing_elements else 'None identified - Excellent coverage!'}

        ### 1. ✅ STRENGTHS ANALYSIS
        **What's Working Well:**
        - Content areas that meet/exceed VC standards
        - Compelling messaging and positioning
        - Strong data points and metrics

        ### 2. ⚠️ IMPROVEMENT OPPORTUNITIES
        **Content Gaps:**
        - Missing critical information for investors
        - Weak or unclear sections that need strengthening
        - Opportunities for more compelling messaging

        **Structural Issues:**
        - Flow and organization improvements
        - Information hierarchy fixes
        - Slide sequence optimization

        ### 3. 🎯 CRITICAL MISSING ELEMENTS
        For each missing element, provide:
        - Why it's essential for {template_name} standard
        - What specific information should be included
        - Where it should be positioned in the deck
        - Impact on investor decision-making

        ### 4. 📈 CONTENT DEPTH ASSESSMENT
        **Information Sufficiency:**
        - Are key points adequately detailed?
        - What additional data/metrics would strengthen the case?
        - Balance between detail and clarity

        ### 5. 💰 INVESTOR APPEAL EVALUATION
        **Compelling Narrative:**
        - Story strength and emotional appeal
        - Logical flow and persuasiveness
        - Memorable differentiators and hooks

        **Risk Assessment:**
        - How well potential risks are addressed
        - Credibility factors present
        - Trust-building elements

        ### 6. 🚀 PRIORITY ACTION ITEMS
        **High-Impact Quick Fixes:**
        1. [Most critical improvements needed]
        2. [Content additions with biggest ROI]
        3. [Structural changes for better flow]

        **Strategic Enhancements:**
        - Advanced positioning strategies
        - Competitive differentiation opportunities
        - Investor-specific customization

        ### 7. 📊 SCORING vs {template_name} STANDARD
        **Overall Assessment:**
        - Investment readiness score (1-10 with explanation)
        - Category-specific ratings
        - Comparison to successful decks in this template

        **DECK CONTENT TO ANALYZE:**
        {deck_text}

        **REQUIREMENTS:**
        - Be specific and actionable in all recommendations
        - Use actual content from the deck (don't invent details)
        - Focus on {template_name} specific requirements
        - Provide clear rationale for each suggestion
        - Prioritize recommendations by impact and effort
        """

        return self._generate_with_retry(prompt)

    def generate_one_pager(self, deck_text):
        """Generate executive summary one-pager"""
        prompt = f"""
        Create a concise, professional one-page executive summary from this pitch deck content. You are creating this for busy investors who need key information at a glance.

        **EXECUTIVE SUMMARY FORMAT:**

        # [COMPANY NAME]
        **One-Line Pitch:** *[Compelling tagline describing what you do]*

        ## 🎯 THE OPPORTUNITY
        **Problem:** [Brief description of the pain point]
        **Market Size:** [TAM/SAM figures if available]
        **Timing:** [Why now is the right time]

        ## 💡 OUR SOLUTION
        **Product:** [What you've built and core functionality]
        **Key Differentiator:** [What makes you uniquely positioned]
        **Value Proposition:** [Primary benefits to customers]

        ## 📈 TRACTION & VALIDATION
        **Metrics:** [Key performance indicators and growth]
        **Customers:** [Notable clients, user base, or pilot programs]
        **Revenue:** [Financial performance highlights]

        ## 💰 BUSINESS MODEL
        **Revenue Streams:** [How you generate money]
        **Unit Economics:** [Key financial metrics like CAC, LTV]
        **Scalability:** [Growth potential and expansion opportunities]

        ## 👥 FOUNDING TEAM
        **Leadership:** [Brief backgrounds of key founders]
        **Expertise:** [Relevant experience and track record]
        **Advisors:** [Notable advisors or board members if mentioned]

        ## 💸 INVESTMENT OPPORTUNITY
        **Raising:** [Amount seeking to raise]
        **Use of Capital:** [Primary allocation of funds]
        **Key Milestones:** [What you'll achieve with this funding]
        **Next Round:** [Timeline and expected progress]

        ---
        **Contact:** [Founder name] • [Email if provided]

        **REQUIREMENTS:**
        - Maximum 400 words total
        - Use bullet points and clear formatting
        - Include specific numbers and metrics from the deck
        - Professional but engaging tone
        - Scannable for busy investors
        - Only use information actually provided in the deck

        **DECK CONTENT:**
        {deck_text}

        **NOTE:** If critical information is missing from the deck, indicate with [To be added] rather than inventing details.
        """

        return self._generate_with_retry(prompt)
