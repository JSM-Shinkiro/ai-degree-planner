import pytest
from pathlib import Path
from streamlit.testing.v1 import AppTest


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setattr("dotenv.load_dotenv",lambda *a,**k:False)
    for name in ["GEMINI_API_KEY","GOOGLE_API_KEY","ADZUNA_APP_ID","ADZUNA_APP_KEY"]:
        monkeypatch.delenv(name,raising=False)
    return AppTest.from_file(Path(__file__).resolve().parents[1]/"app.py",default_timeout=20).run()


def submit(app):
    next(b for b in app.button if b.label=="Update my roadmap").click()
    return app.run()


def test_profile_to_roadmap_and_goal_change(app):
    assert not app.exception
    submit(app)
    assert not app.exception
    assert any("ECE425" in h.value for h in app.subheader)
    assert app.session_state["result"].context.allowed_record_ids[0]=="uofa:ECE101:2026-2027"
    app.selectbox(key="career_id").set_value("embedded")
    app.selectbox(key="programming_background").set_value("experienced")
    submit(app)
    assert not app.exception
    assert app.session_state["profile"].career_id=="embedded"
    assert app.session_state["profile"].programming_background=="experienced"
    assert app.session_state["result"].context.allowed_record_ids[0]=="uofa:ECE372A:2026-2027"
    assert not app.session_state["result"].generation_complete


def test_completed_course_updates_ui(app):
    app.selectbox(key="career_id").set_value("embedded")
    app.text_area(key="course_text").set_value("ECE372A:B")
    submit(app)
    assert not app.exception
    assert "uofa:ECE372A:2026-2027" not in app.session_state["result"].context.allowed_record_ids


def test_invalid_profile_is_visible_error(app):
    app.text_area(key="course_text").set_value("ECE101, ECE 101")
    submit(app)
    assert not app.exception
    assert app.error


def test_unconfigured_jobs_have_clear_state(app):
    next(b for b in app.button if b.label=="Available Opportunities").click()
    app.run()
    assert not app.exception
    assert any("not configured" in x.value for x in app.info)


def test_live_ui_with_controlled_provider(app,monkeypatch,fake_provider):
    import src.providers
    original=fake_provider.generate
    def with_multiple_reasons(context):
        answer=original(context)
        answer.recommendations[0].reasons.append(answer.recommendations[0].reasons[0].model_copy())
        return answer
    fake_provider.generate=with_multiple_reasons
    fake_provider.close=lambda:None
    monkeypatch.setattr(src.providers,"GeminiProvider",lambda *a,**k:fake_provider)
    app.text_input(key="gemini_key").set_value("fixture-key")
    app.run()
    app.checkbox(key="use_ai").set_value(True)
    app.run()
    submit(app)
    assert not app.exception
    assert app.session_state["result"].generation_complete
    assert fake_provider.context is app.session_state["result"].context
