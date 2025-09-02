import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
from pptx import Presentation
import json
import pandas as pd
import plotly.express as px
from utils.gemini_helper import GeminiHelper
from utils.template_checker import TemplateChecker
import os
import io

# Configure Streamlit page
st.set_page_config(
    page_title="Pitch Deck Enhancer",
    page_icon="📊",
    layout="wide"
)

# Available Gemini models in order of preference
GEMINI_MODELS = [
    "gemini-1.5-flash",    # Fast and efficient
    "gemini-1.5-pro",      # More capable
    "gemini-1.0-pro",      # Fallback option
]

@st.cache_resource
def init_gemini():
    """Initialize Gemini with proper error handling and model selection"""
    api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("⚠️ Please set GOOGLE_API_KEY in Streamlit secrets or environment variables")
        st.info("Get your free API key from: https://aistudio.google.com/")
        return None, None

    try:
        genai.configure(api_key=api_key)

        # Try to list available models first
        try:
            available_models = [m.name for m in genai.list_models()]
            st.sidebar.success(f"✅ Connected to Gemini API")
            st.sidebar.info(f"Available models: {len(available_models)}")
        except Exception as e:
            st.sidebar.warning(f"Could not list models: {str(e)}")
            available_models = []

        # Try each model until one works
        for model_name in GEMINI_MODELS:
            try:
                model = genai.GenerativeModel(model_name)
                # Test the model with a simple prompt
                test_response = model.generate_content("Hello, respond with 'OK' if you're working.")
                if test_response.text:
                    st.sidebar.success(f"🤖 Using model: {model_name}")
                    return model, model_name
            except Exception as e:
                st.sidebar.warning(f"Model {model_name} failed: {str(e)}")
                continue

        # If no models work, return error
        st.error("❌ Could not initialize any Gemini model. Please check your API key and try again.")
        return None, None

    except Exception as e:
        st.error(f"Error configuring Gemini: {str(e)}")
        return None, None

def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
        return text
    except Exception as e:
        st.error(f"Error extracting PDF text: {str(e)}")
        return ""

def extract_text_from_pptx(file):
    """Extract text from PowerPoint file"""
    try:
        prs = Presentation(io.BytesIO(file.read()))
        text = ""
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error extracting PPTX text: {str(e)}")
        return ""

def show_api_setup_guide():
    """Show detailed API setup guide"""
    st.markdown("""
    ### 🔑 Google Gemini API Setup Guide

    **Step 1: Get Your Free API Key**
    1. Visit [**Google AI Studio**](https://aistudio.google.com/)
    2. Sign in with your Google account
    3. Click **"Get API Key"** or **"Create API Key"**
    4. Copy the generated key (starts with 'AIza...')

    **Step 2: Add to Streamlit**
    - Go to your app settings
    - Find "Secrets" section  
    - Add: `GOOGLE_API_KEY = "your_actual_key_here"`

    **Step 3: Verify Setup**
    - Refresh this page
    - You should see "✅ Connected to Gemini API" in the sidebar

    **Need Help?**
    - Make sure your API key is active
    - Check for any typos in the key
    - Ensure Gemini API is enabled in your Google Cloud project
    """)

# Main App
def main():
    st.title("📊 Pitch Deck Enhancer Agent")
    st.markdown("*Transform your pitch deck with AI-powered insights*")

    # Sidebar info
    st.sidebar.header("🚀 Features")
    st.sidebar.markdown("""
    - **Structure Analysis**: Reorganize content into investor-ready format
    - **Pitch Script**: Generate compelling 2-minute presentation
    - **Design Tips**: Modern slide design improvements
    - **Benchmark Check**: Compare vs YC/Sequoia templates
    - **One-Pager**: Auto-generate investor summary
    """)

    st.sidebar.markdown("---")
    st.sidebar.markdown("**💡 How to use:**")
    st.sidebar.markdown("""
    1. Set up your Google Gemini API key
    2. Upload your pitch deck (PDF or PPT)
    3. Click on any feature tab
    4. Get AI-powered insights instantly!
    """)

    # Initialize Gemini with better error handling
    model, model_name = init_gemini()
    if not model:
        show_api_setup_guide()
        return

    # File upload section
    st.markdown("### 📄 Upload Your Pitch Deck")
    uploaded_file = st.file_uploader(
        "Choose your pitch deck file",
        type=["pdf", "pptx"],
        help="Supported formats: PDF, PowerPoint (.pptx)"
    )

    if uploaded_file:
        # Extract text based on file type
        with st.spinner("🔍 Extracting content from your deck..."):
            if uploaded_file.type == "application/pdf":
                deck_text = extract_text_from_pdf(uploaded_file)
            else:  # pptx
                deck_text = extract_text_from_pptx(uploaded_file)

        if len(deck_text.strip()) < 50:
            st.warning("⚠️ Limited text detected. Please ensure your deck contains readable text content.")
            st.info("💡 Tip: Image-only slides won't be analyzed. Add text content for better results.")

            # Show a sample format
            with st.expander("📋 See example format that works well"):
                st.markdown("""
                **Good Format Example:**
                ```
                Problem: 73% of small businesses struggle with 24/7 customer support
                Solution: AI-powered chatbot that handles 90% of inquiries automatically
                Market: $15B customer service automation market, growing 25% annually
                Traction: 150 customers, $45K MRR, 95% satisfaction
                ```
                """)
            return

        st.success(f"✅ Successfully extracted {len(deck_text)} characters from your deck")

        # Show preview of extracted text
        with st.expander("👁️ Preview extracted content"):
            preview_text = deck_text[:800] + "..." if len(deck_text) > 800 else deck_text
            st.text_area("Extracted Content", preview_text, height=200, disabled=True)

        # Initialize AI helper
        helper = GeminiHelper(model, model_name)
        checker = TemplateChecker()

        # Analysis tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📑 Structure", "🎤 Pitch Script", "🎨 Design", "📊 Benchmark", "📄 One-Pager"
        ])

        with tab1:
            st.header("📑 Structured Outline")
            st.markdown("Get your deck reorganized into investor-ready sections")

            if st.button("🚀 Generate Structure", key="structure", type="primary"):
                with st.spinner("🤖 AI is analyzing your deck structure..."):
                    try:
                        outline = helper.generate_structure(deck_text)
                        if outline and "Error" not in outline:
                            st.markdown("### Your Restructured Pitch Deck")
                            st.markdown(outline)

                            # Download option
                            st.download_button(
                                "📥 Download Structure",
                                outline,
                                file_name="pitch_structure.md",
                                mime="text/markdown"
                            )
                        else:
                            st.error("Failed to generate structure. Please try again or check your API key.")
                    except Exception as e:
                        st.error(f"Error generating structure: {str(e)}")
                        st.info("💡 Try refreshing the page or check your internet connection.")

        with tab2:
            st.header("🎤 2-Minute Pitch Script")
            st.markdown("Transform your deck into a compelling presentation script")

            if st.button("🎯 Generate Script", key="script", type="primary"):
                with st.spinner("✍️ Crafting your pitch script..."):
                    try:
                        script = helper.generate_pitch_script(deck_text)
                        if script and "Error" not in script:
                            st.markdown("### Your Pitch Script")
                            st.markdown(script)

                            # Download option
                            st.download_button(
                                "📥 Download Script",
                                script,
                                file_name="pitch_script.md",
                                mime="text/markdown"
                            )
                        else:
                            st.error("Failed to generate script. Please try again.")
                    except Exception as e:
                        st.error(f"Error generating script: {str(e)}")

        with tab3:
            st.header("🎨 Design Suggestions")
            st.markdown("Get modern design recommendations for your slides")

            if st.button("🎨 Get Design Tips", key="design", type="primary"):
                with st.spinner("🎨 Analyzing design improvements..."):
                    try:
                        design_tips = helper.generate_design_suggestions(deck_text)
                        if design_tips and "Error" not in design_tips:
                            st.markdown("### Design Recommendations")
                            st.markdown(design_tips)

                            # Download option
                            st.download_button(
                                "📥 Download Design Guide",
                                design_tips,
                                file_name="design_suggestions.md",
                                mime="text/markdown"
                            )
                        else:
                            st.error("Failed to generate design suggestions. Please try again.")
                    except Exception as e:
                        st.error(f"Error generating design suggestions: {str(e)}")

        with tab4:
            st.header("📊 Benchmark Analysis")
            st.markdown("Compare your deck against top-tier investor templates")

            col1, col2 = st.columns([2, 1])
            with col1:
                template_choice = st.selectbox(
                    "📋 Compare against template:", 
                    ["Y Combinator", "Sequoia Capital"],
                    help="Choose which top-tier template to benchmark against"
                )

            if st.button("📊 Run Benchmark Analysis", key="benchmark", type="primary"):
                with st.spinner("📈 Comparing against best practices..."):
                    try:
                        template_key = template_choice.lower().replace(" ", "_")
                        gaps = checker.check_template_gaps(deck_text, template_key)
                        benchmark_analysis = helper.generate_benchmark_analysis(deck_text, gaps, template_choice)

                        if benchmark_analysis and "Error" not in benchmark_analysis:
                            # Results display
                            col1, col2 = st.columns([1, 1])

                            with col1:
                                st.subheader("✅ Template Coverage")
                                if gaps:
                                    missing_count = len(gaps)
                                    total_sections = len(checker.templates[template_key]['required_sections'])
                                    coverage = ((total_sections - missing_count) / total_sections) * 100

                                    st.metric("Coverage Score", f"{coverage:.0f}%")
                                    st.error(f"❌ Missing {missing_count} key sections")

                                    for gap in gaps:
                                        st.error(f"• Missing: **{gap}**")
                                else:
                                    st.success("🎉 All key elements present!")
                                    st.metric("Coverage Score", "100%")

                            with col2:
                                st.subheader("📊 Template Requirements")
                                template_info = checker.templates[template_key]
                                st.info(f"**Required sections:** {len(template_info['required_sections'])}")
                                st.info(f"**Optional sections:** {len(template_info['optional_sections'])}")

                            st.subheader("🔍 Detailed Analysis")
                            st.markdown(benchmark_analysis)

                            # Download option
                            st.download_button(
                                "📥 Download Benchmark Report",
                                benchmark_analysis,
                                file_name=f"benchmark_{template_key}.md",
                                mime="text/markdown"
                            )
                        else:
                            st.error("Failed to generate benchmark analysis. Please try again.")
                    except Exception as e:
                        st.error(f"Error running benchmark: {str(e)}")

        with tab5:
            st.header("📄 One-Page Executive Summary")
            st.markdown("Generate a concise investor-ready summary")

            if st.button("📝 Generate One-Pager", key="onepager", type="primary"):
                with st.spinner("📋 Creating executive summary..."):
                    try:
                        summary = helper.generate_one_pager(deck_text)
                        if summary and "Error" not in summary:
                            st.markdown("### Executive Summary")
                            st.markdown(summary)

                            # Download option
                            st.download_button(
                                "📥 Download One-Pager",
                                summary,
                                file_name="executive_summary.md",
                                mime="text/markdown"
                            )
                        else:
                            st.error("Failed to generate one-pager. Please try again.")
                    except Exception as e:
                        st.error(f"Error generating one-pager: {str(e)}")

    else:
        # Welcome screen with better guidance
        st.markdown("## 👋 Welcome to Pitch Deck Enhancer")
        st.markdown("""
        Upload your pitch deck above to get started with AI-powered analysis and improvements.

        ### 🌟 What you'll get:
        - **Structured outline** following investor best practices
        - **2-minute pitch script** for presentations
        - **Modern design suggestions** for visual appeal
        - **Benchmark analysis** vs top VC templates
        - **One-page summary** for investors

        ### 📊 Supported formats:
        - **PDF files** (.pdf)
        - **PowerPoint presentations** (.pptx)

        ### 💡 Tips for best results:
        - Include text content (not just images)
        - Use clear section headers
        - Add specific metrics and numbers
        """)

        # Sample content section
        with st.expander("📝 Try with sample content"):
            st.markdown("""
            **Sample Pitch Content to Test:**

            Create a simple PDF/PPT with this text:

            ---

            **Problem:** Small businesses struggle with 24/7 customer support. 73% expect immediate responses.

            **Solution:** AI chatbot handling 90% of inquiries with seamless human handoff.

            **Market:** $15B customer service automation market growing 25% annually.

            **Traction:** 150+ customers, $45K MRR, 95% satisfaction, 40% monthly growth.

            **Ask:** Raising $1.5M seed for engineering, sales, and operations expansion.

            ---

            Upload this as a test document to see the AI analysis in action!
            """)

if __name__ == "__main__":
    main()
