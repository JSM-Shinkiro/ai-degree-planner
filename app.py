"""Streamlit entry point. Run with: streamlit run app.py."""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import time
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

from src.catalog import ROOT, build_evidence, load_catalog
from src.jobs import search_jobs
from src.models import StudentProfile
from src.profiles import export_profile, import_profile, parse_completions
from src.providers import GeminiProvider, ProviderError
from src.retrieval import project_embeddings
from src.service import recommend

load_dotenv(ROOT / ".env")
st.set_page_config(page_title="ECE Learning Advisor · P07", page_icon="🧭", layout="wide")
st.markdown("""
<style>
.block-container { max-width: 1220px; padding-top: 2.2rem; }
[data-testid="stSidebar"] { border-right: 1px solid #25334a; }
h1 { letter-spacing: -.04em; }
[data-testid="stMetric"] { background: #131e31; border: 1px solid #26344c; padding: .8rem 1rem; border-radius: 12px; }
.stButton button, .stDownloadButton button { border-radius: 9px; }
</style>
""", unsafe_allow_html=True)

catalog = load_catalog()
records = {r.record_id: r for r in catalog.records}
sources = {s.source_id: s for s in catalog.sources}
career_names = {"ai_ml":"AI / Machine Learning", "embedded":"Embedded Systems", "exploring":"Still exploring"}
standings = ["Incoming", "Freshman", "Sophomore", "Junior", "Senior", "Other"]

if "profile" not in st.session_state:
    st.session_state.profile = StudentProfile()
profile = st.session_state.profile

with st.sidebar:
    st.caption("TEAM P07 · ECE 425/525")
    st.title("Your starting point")
    uploaded = st.file_uploader("Restore a saved profile", type=["json"])
    if uploaded:
        payload = uploaded.getvalue()
        digest = hashlib.sha256(payload).hexdigest()
        if digest != st.session_state.get("loaded_profile_hash"):
            try:
                loaded = import_profile(payload)
                st.session_state.profile = loaded
                st.session_state.loaded_profile_hash = digest
                st.session_state.pop("result", None)
                for key in ["standing", "career_id", "catalog_version", "interests", "experience", "course_text", "history_complete", "programming_background", "question"]:
                    st.session_state.pop(key, None)
                st.rerun()
            except (ValueError, TypeError):
                st.error("This file is not a supported profile. Check its contents and try again.")

    with st.form("profile_form"):
        standing = st.selectbox("Academic standing", standings, index=standings.index(profile.standing), key="standing")
        background_names={"new":"Getting started", "some":"Some programming experience", "experienced":"Comfortable with programming"}
        programming_background=st.selectbox("Programming background",list(background_names),
            index=list(background_names).index(profile.programming_background),
            format_func=lambda k:background_names[k],key="programming_background")
        career_id = st.selectbox("Career direction", list(career_names), index=list(career_names).index(profile.career_id),
                                 format_func=lambda k:career_names[k], key="career_id")
        catalog_version = st.text_input("Catalog year", value=profile.catalog_version, placeholder="2026-2027 or Not sure", key="catalog_version")
        interests = st.text_area("What interests you?", value=profile.interests, placeholder="Computer vision, robotics, devices...", key="interests", max_chars=1500)
        course_text = st.text_area(
            "Completed coursework", value=", ".join(c.course_code + (":"+c.grade if c.grade else "") for c in profile.completed),
            placeholder="ECE101:B, MATH129, CSC120:A", key="course_text",
            help="Separate course codes with commas. Grades are optional, following a colon.",
        )
        history_complete = st.checkbox("I listed all my completed courses", value=profile.history_complete, key="history_complete")
        experience = st.text_area("Projects or experience (optional)", value=profile.experience, key="experience", max_chars=2000)
        question = st.text_input("What would you like to learn next?", value="", placeholder="How can I start building smart devices?", key="question", max_chars=1200)
        submitted = st.form_submit_button("Update my roadmap", type="primary", width="stretch")

    with st.expander("AI settings"):
        st.caption("Source exploration works without a key. Live AI sends the submitted profile and selected evidence to Gemini.")
        api_key = st.text_input("Gemini API key", value=os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", ""),
                                type="password", key="gemini_key")
        use_ai = st.checkbox("Generate AI explanations", value=False, disabled=not bool(api_key), key="use_ai")
        method = st.selectbox("Retrieval method", ["hybrid","semantic","keyword"], disabled=not use_ai)
        generation_model = st.text_input("Generation model", value=os.getenv("GENERATION_MODEL","gemini-3.8-flash"))
        embedding_model = st.text_input("Embedding model", value=os.getenv("EMBEDDING_MODEL","gemini-embedding-2"))
        st.caption("Model availability depends on your account. No provider request runs until you update the roadmap.")

    st.caption("Prototype · 5 courses · 2 resources")

st.caption("ECE LEARNING & CAREER ADVISOR")
st.title("Plan your next step.")
st.write("Connect what you have learned with where you want to go.")
st.caption("A starter collection for AI/ML and embedded systems. Course relevance and academic eligibility are shown separately.")

if submitted:
    try:
        profile = StudentProfile(
            standing=standing, career_id=career_id, catalog_version=catalog_version.strip() or "Not sure",
            interests=interests, experience=experience,
            completed=parse_completions(course_text), history_complete=history_complete,
            programming_background=programming_background,
        )
        st.session_state.profile = profile
        st.session_state.pop("job_result", None)
        provider = None
        try:
            if use_ai and api_key:
                provider = GeminiProvider(
                    api_key, embedding_model=embedding_model,
                    generation_model=generation_model,
                    dimensions=int(os.getenv("EMBEDDING_DIMENSION","768")),
                )
            with st.spinner("Finding supporting courses and resources..."):
                result = recommend(catalog, profile, question, provider=provider,
                                   method=method if provider else "keyword", cache_dir=ROOT/".cache"/"embeddings")
            st.session_state.result = result
        finally:
            if provider is not None:
                provider.close()
    except ValueError as exc:
        st.error("Please check your profile: " + str(exc))
    except (ProviderError, ImportError):
        st.error("The AI provider could not be initialized. Try source exploration or check the configuration.")

with st.sidebar:
    st.download_button("Download my profile", export_profile(st.session_state.profile),
                       file_name="ece_profile.json", mime="application/json", width="stretch")

roadmap, collection, opportunities = st.tabs(["My Roadmap", "Source Collection", "Opportunities"])

with roadmap:
    result = st.session_state.get("result")
    if result is None:
        st.info("Start with your background in the sidebar, then select Update my roadmap.")
        left, right = st.columns(2)
        with left, st.container(border=True):
            st.subheader("AI / Machine Learning")
            st.write("Explore neural networks, programming foundations, and practical model-building resources.")
        with right, st.container(border=True):
            st.subheader("Embedded Systems")
            st.write("Explore C programming, microcontrollers, computer architecture, and hardware interfaces.")
    else:
        live = result.generation_complete
        columns = st.columns(3)
        columns[0].metric("Direction", career_names[result.context.profile.career_id])
        columns[1].metric("Completed courses", len(result.context.profile.completed))
        columns[2].metric("Last response", f"{result.timings['total']:.2f} s")
        if live:
            st.success("RAG explanation generated. Source references passed validation.")
        else:
            st.info(f"Source exploration · {result.retrieval_mode} retrieval and reviewed summaries. No generated AI explanation is being shown.")
        for issue in result.issues:
            st.warning(issue)
        if result.answer and result.answer.clarification:
            st.info(result.answer.clarification)
        explanations = {r.record_id:r for r in result.answer.recommendations} if result.answer else {}
        evidence_map = {e.chunk_id:e for e in result.context.evidence}
        course_ids = [rid for rid in result.context.allowed_record_ids if records[rid].kind=="course"]
        resource_ids = [rid for rid in result.context.allowed_record_ids if records[rid].kind=="resource"]
        st.subheader("Suggested courses")
        if not course_ids:
            st.info("No additional courses matched within this small collection. Try another question or inspect the source collection.")
        for rid in course_ids:
            record = records[rid]
            evaluation = result.context.rule_results[rid]
            labels = {"unknown":"Requirements need review", "unsatisfied":"Requirements missing", "satisfied":"Recorded prerequisites satisfied"}
            with st.container(border=True):
                st.caption("LATER LEARNING GOAL" if result.context.suggested_phases.get(rid)=="later" else "NEXT LEARNING STEP")
                title, badge = st.columns([3,2])
                title.subheader(f"{record.code} · {record.title}")
                badge.caption(labels[evaluation.status])
                st.caption(f"{record.credits:g} credits · Catalog {record.catalog_version}")
                st.write(record.summary)
                if rid in explanations:
                    for reason_index, reason in enumerate(explanations[rid].reasons):
                        st.write(reason.text)
                        for citation in reason.evidence_ids:
                            for sid in evidence_map[citation].source_ids:
                                source = sources[sid]
                                st.link_button("Evidence: "+source.title,source.url,
                                               key=f"course_{rid}_{reason_index}_{citation}_{sid}")
                st.caption(" ".join(evaluation.reasons))
                for sid in record.source_ids:
                    st.link_button("Official course source",sources[sid].url)
        if resource_ids:
            st.subheader("Learn alongside your courses")
            for rid in resource_ids:
                record = records[rid]
                with st.container(border=True):
                    st.markdown("**"+record.title+"**")
                    st.write(record.summary)
                    if rid in explanations:
                        for reason_index, reason in enumerate(explanations[rid].reasons):
                            st.write(reason.text)
                            for citation in reason.evidence_ids:
                                for sid in evidence_map[citation].source_ids:
                                    source=sources[sid]
                                    st.link_button("Evidence: "+source.title,source.url,
                                                   key=f"resource_{rid}_{reason_index}_{citation}_{sid}")
                    st.link_button("Open learning resource",sources[record.source_ids[0]].url)
        with st.expander("How these recommendations were made"):
            st.caption("The current catalog exposes internal enrollment requirement IDs. All five academic rules remain unknown pending review.")
            hits = [h for h in result.hits if records[h.record_id].kind!="career"][:8]
            if hits:
                figure = go.Figure(go.Bar(
                    x=[h.score for h in hits], y=[records[h.record_id].code or records[h.record_id].title for h in hits],
                    orientation="h",marker_color="#78B8FF",
                ))
                figure.update_layout(template="plotly_dark",height=330,margin=dict(l=5,r=10,t=10,b=10),
                                     xaxis_title=result.retrieval_mode+" ranking score",yaxis=dict(autorange="reversed"))
                st.plotly_chart(figure,width="stretch")
            if result.vectors is not None:
                points, query_point = project_embeddings(result.vectors,result.query_vector)
                chunks = build_evidence(catalog)
                labels = [records[e.record_id].code or records[e.record_id].title for e in chunks]
                chart = go.Figure(go.Scatter(x=points[:,0],y=points[:,1],mode="markers",text=labels,
                    marker=dict(size=11,color="#78B8FF"),hovertemplate="%{text}<extra></extra>",name="Records"))
                if query_point is not None:
                    chart.add_trace(go.Scatter(x=[query_point[0]],y=[query_point[1]],mode="markers",
                        marker=dict(size=17,symbol="star",color="#FFD17A"),name="Your query"))
                chart.update_layout(template="plotly_dark",height=350,xaxis_title="PCA 1",yaxis_title="PCA 2")
                st.plotly_chart(chart,width="stretch")
                st.caption("A 2D projection of real embedding vectors. Ranking uses the full vectors. Similarity is not probability.")
                selected_index=st.selectbox("Inspect a record vector",range(len(chunks)),format_func=lambda i:labels[i])
                record_vector=result.vectors[selected_index]
                query_vector=result.query_vector
                dot=float(np.dot(query_vector,record_vector))
                query_norm=float(np.linalg.norm(query_vector))
                record_norm=float(np.linalg.norm(record_vector))
                st.latex(r"\operatorname{cosine}(q,d)=\frac{q\cdot d}{\|q\|\|d\|}")
                st.write(f"{len(record_vector)} dimensions · dot product {dot:.5f} · query norm {query_norm:.5f} · record norm {record_norm:.5f}")
                st.json({"query_first_12_dimensions":query_vector[:12].tolist(),
                         "record_first_12_dimensions":record_vector[:12].tolist(),
                         "cosine_similarity":dot/(query_norm*record_norm)})
            else:
                st.caption("The embedding map becomes available after a successful semantic retrieval request.")
            for chunk in result.context.evidence:
                st.markdown("**"+chunk.chunk_id+"**")
                st.text(chunk.text)
                for sid in chunk.source_ids:
                    source=sources[sid]
                    st.link_button(source.title,source.url,key="trace_"+chunk.chunk_id+"_"+sid)
            st.json(result.trace)
            st.download_button("Download request trace",json.dumps(result.trace,indent=2),file_name="request_trace.json",mime="application/json")

with collection:
    st.subheader("A small, inspectable starting collection")
    st.write("Five current catalog summaries and two complementary resources. Career connections are team annotations.")
    for record in catalog.records:
        if record.kind=="career":
            continue
        with st.expander((record.code+" · " if record.code else "")+record.title):
            st.write(record.summary)
            for sid in record.source_ids:
                source=sources[sid]
                st.link_button(source.title,source.url,key="collection_"+record.record_id+"_"+sid)
                st.caption("Retrieved "+source.retrieved_at.date().isoformat()+" · "+source.review_note)

with opportunities:
    st.subheader("Explore available opportunities")
    st.write("Search current provider listings for your selected direction.")
    with st.form("jobs_form"):
        location = st.text_input("Location", value="Tucson, AZ")
        internship = st.checkbox("Focus the search on internships")
        requested = st.form_submit_button("Available Opportunities")
    if requested:
        st.session_state.pop("job_result", None)
        job_key=(st.session_state.profile.career_id,location,internship)
        cached=st.session_state.get("jobs_cache")
        try:
            if cached and cached["key"]==job_key and time.time()-cached["created"]<1200:
                job_result=cached["result"]
            else:
                with st.spinner("Searching opportunities..."):
                    job_result=search_jobs(
                        os.getenv("ADZUNA_APP_ID",""),os.getenv("ADZUNA_APP_KEY",""),
                        st.session_state.profile.career_id,location,internship)
                st.session_state.jobs_cache={"key":job_key,"created":time.time(),"result":job_result}
            st.session_state.job_result=job_result
        except ValueError:
            st.info("Job search is not configured for this prototype yet. The team needs to enable its provider connection.")
        except RuntimeError:
            st.warning("The provider could not complete this search. Try again later.")
    jobs=st.session_state.get("job_result")
    if jobs:
        st.caption(f"Query: {jobs.query} · Location: {jobs.location} · Retrieved: {jobs.retrieved_at}")
        if not jobs.listings:
            st.info("No listings were returned for these filters.")
        for job in jobs.listings:
            with st.container(border=True):
                st.markdown("**"+job["title"]+"**")
                st.caption(job["employer"]+" · "+job["location"])
                if job["posted_at"]:
                    st.caption("Provider posting date: "+str(job["posted_at"]))
                st.write(re.sub("<[^>]+>","",html.unescape(job["description_snippet"]))[:700])
                st.link_button("View original opportunity",job["url"])
        st.caption("Descriptions may be snippets. A relevant match does not establish eligibility or continuing availability.")
