import streamlit as st

from research import search_web
from extractor import extract_founders
from enrichment import enrich_leads
from personalizer import generate_message


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="ReachPilot",
    page_icon="🚀",
    layout="wide"
)


# --------------------------------
# SESSION STATE
# --------------------------------

if "leads" not in st.session_state:
    st.session_state.leads = []

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "search_completed" not in st.session_state:
    st.session_state.search_completed = False


# --------------------------------
# HEADER
# --------------------------------

st.title("🚀 ReachPilot")

st.caption("AI-Powered LinkedIn Outreach Assistant")

st.divider()


# --------------------------------
# LEAD DISCOVERY
# --------------------------------

if not st.session_state.search_completed:

    st.header("🔍 Discover Leads")

    with st.form("lead_search_form"):

        search_prompt = st.text_area(
            "Describe your target audience",
            placeholder="Find founders or CEOs of AI startups in India who might hire AI interns..."
        )

        col1, col2 = st.columns(2)

        with col1:

            number_of_leads = st.number_input(
                "Number of leads",
                min_value=1,
                max_value=50,
                value=20
            )

        with col2:

            st.write("")
            st.write("")

            st.info("We'll discover founders and their LinkedIn profiles.")

        st.subheader("Your Outreach Message")

        message_template = st.text_area(
            "Message Template",
            height=200,
            placeholder="""Hi [name],

I'm Mahesh, a 3rd-year ECE student at IIT Bhilai.

I'm interested in AI/ML and would love to explore opportunities at [company].

Would love to connect!"""
        )

        submitted = st.form_submit_button(
            "🚀 Find Leads",
            use_container_width=True
        )


    # --------------------------------
    # START RESEARCH
    # --------------------------------

    if submitted:

        if not search_prompt.strip():

            st.error("Please enter a search prompt.")

        elif not message_template.strip():

            st.error("Please enter an outreach message template.")

        else:

            try:

                with st.status(
                    "Researching potential leads...",
                    expanded=True
                ) as status:

                    st.write("🔍 Searching the web using Tavily...")

                    results = search_web(
                        search_prompt,
                        max_results=5
                    )

                    if not results:
                        raise RuntimeError(
                            "No search results found."
                        )

                    st.write(
                        f"Found {len(results)} search results."
                    )

                    st.write("🤖 Extracting founders using Gemini...")

                    leads = extract_founders(
                        results,
                        max_leads=int(number_of_leads)
                    )

                    if not leads:
                        raise RuntimeError(
                            "No founders could be extracted."
                        )

                    st.write(
                        f"Extracted {len(leads)} unique leads."
                    )

                    st.write("🌐 Discovering company websites and LinkedIn profiles...")

                    leads = enrich_leads(leads)

                    st.write("✍️ Generating personalized messages...")

                    for lead in leads:

                        lead["message"] = generate_message(
                            lead,
                            message_template
                        )

                        lead["status"] = "Pending"

                    st.session_state.leads = leads

                    st.session_state.current_index = 0

                    st.session_state.search_completed = True

                    status.update(
                        label="Research completed successfully!",
                        state="complete",
                        expanded=False
                    )

                st.rerun()

            except Exception as e:

                st.error(f"Research failed: {e}")


# --------------------------------
# OUTREACH DASHBOARD
# --------------------------------

else:

    leads = st.session_state.leads

    total = len(leads)

    current_index = st.session_state.current_index

    sent_count = sum(
        lead["status"] == "Sent"
        for lead in leads
    )

    skipped_count = sum(
        lead["status"] == "Skipped"
        for lead in leads
    )

    pending_count = sum(
        lead["status"] == "Pending"
        for lead in leads
    )


    # --------------------------------
    # DASHBOARD SUMMARY
    # --------------------------------

    st.header("📊 Outreach Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Leads", total)
    col2.metric("Sent", sent_count)
    col3.metric("Pending", pending_count)
    col4.metric("Skipped", skipped_count)

    st.progress((sent_count + skipped_count) / total)

    st.divider()


    # --------------------------------
    # LEAD REVIEW
    # --------------------------------

    if current_index >= total:

        st.success("You've reviewed all leads!")

        if st.button("Start New Search"):

            st.session_state.leads = []
            st.session_state.current_index = 0
            st.session_state.search_completed = False

            st.rerun()

    else:

        lead = leads[current_index]

        st.subheader(
            f"Lead {current_index + 1} of {total}"
        )

        # Founder details

        col1, col2 = st.columns([2, 1])

        with col1:

            st.markdown(
                f"## {lead.get('name', 'Unknown')}"
            )

            st.write(
                f"**Company:** {lead.get('company', 'Unknown')}"
            )

            st.write(
                f"**Designation:** {lead.get('designation', 'Unknown')}"
            )

            st.write(
                f"**Relevance:** {lead.get('relevance', 'Not available')}"
            )

        with col2:

            st.write("**Current Status**")

            if lead["status"] == "Sent":

                st.success("Sent")

            elif lead["status"] == "Skipped":

                st.warning("Skipped")

            else:

                st.info("Pending")


        # Company website

        if lead.get("website"):

            st.link_button(
                "🌐 Company Website",
                lead["website"]
            )


        # LinkedIn profile

        if lead.get("linkedin_url"):

            st.link_button(
                "🔗 Open LinkedIn Profile",
                lead["linkedin_url"]
            )

            st.caption(
                "Verify the person's identity before contacting them."
            )

        else:

            st.warning("LinkedIn profile not found.")


        st.divider()


        # --------------------------------
        # PERSONALIZED MESSAGE
        # --------------------------------

        st.subheader("✉️ Personalized Outreach Message")

        st.text_area(
            "Review your message",
            value=lead.get("message", ""),
            height=200,
            disabled=True,
            key=f"message_{current_index}"
        )


        st.divider()


        # --------------------------------
        # OUTREACH ACTIONS
        # --------------------------------

        st.subheader("Manage Outreach")

        col1, col2, col3 = st.columns(3)

        with col1:

            if st.button(
                "⏭️ Skip",
                use_container_width=True
            ):

                lead["status"] = "Skipped"

                st.session_state.current_index += 1

                st.rerun()


        with col2:

            if st.button(
                "✅ Mark as Sent",
                use_container_width=True
            ):

                lead["status"] = "Sent"

                st.session_state.current_index += 1

                st.rerun()


        with col3:

            if st.button(
                "Next ➡️",
                use_container_width=True
            ):

                st.session_state.current_index = min(
                    current_index + 1,
                    total - 1
                )

                st.rerun()


        # Previous navigation

        if current_index > 0:

            if st.button("⬅️ Previous Lead"):

                st.session_state.current_index -= 1

                st.rerun()


        st.divider()

        st.caption(
            "LinkedIn messaging and sending are performed manually. "
            "Chrome extension integration will be added separately."
        )


    # --------------------------------
    # RESET SEARCH
    # --------------------------------

    st.divider()

    if st.button("🔄 Start New Search"):

        st.session_state.leads = []

        st.session_state.current_index = 0

        st.session_state.search_completed = False

        st.rerun()