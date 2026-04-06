import streamlit as st
from scraper import get_clean_seo_data, generate_schema

st.set_page_config(page_title="AI SEO Schema Generator", page_icon="🔍", layout="centered")

st.title("🔍 AI SEO Schema Generator")
st.markdown("Enter a URL below and let Gemini generate the JSON-LD schema markup for the page.")

url = st.text_input("Website URL", placeholder="https://example.com")

if st.button("Generate Schema", type="primary"):
    if not url.strip():
        st.warning("Please enter a URL first.")
    else:
        with st.spinner("Scraping page and generating schema..."):
            seo_data = get_clean_seo_data(url)

            if isinstance(seo_data, str) and seo_data.startswith("Error"):
                st.error(seo_data)
            else:
                # Show scraped SEO metadata in an expander
                with st.expander("📄 Scraped SEO Data", expanded=False):
                    st.json(seo_data)

                schema = generate_schema(seo_data)

                if schema.startswith("Error"):
                    st.error(schema)
                else:
                    st.subheader("✅ Generated JSON-LD Schema")
                    st.code(schema, language="json")

                    st.download_button(
                        label="⬇️ Download schema.json",
                        data=schema,
                        file_name="schema.json",
                        mime="application/json",
                    )
