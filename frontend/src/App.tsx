import { useEffect, useState } from "react";
import "./App.css";

type Topic = {
  topic: string;
  minutes: number;
};

type ActivityBlock = {
  start: string;
  end: string;
  topic: string;
  category: string;
  duration_minutes: number;
  evidence: string[];
};

type DailySummary = {
  date: string;
  total_tracked_minutes: number;
  total_sessions: number;
  top_topics: Topic[];
  major_activity_blocks: ActivityBlock[];
};

type WeeklyReview = {
  date: string;
  review_window_days: number;
  active_tracked_days: number;
  total_summarized_minutes: number;
  top_weekly_topics: Topic[];
  recurring_themes: string[];
};

type Tab = "today" | "weekly" | "ai";

type AIRecap = {
  source_file: string;
  recap: string;
};

type AskResponse = {
  question: string;
  answer: string;
  model: string;
};

function App() {
  const [activeTab, setActiveTab] = useState<Tab>("today");
  const [summary, setSummary] = useState<DailySummary | null>(null);
  const [weekly, setWeekly] = useState<WeeklyReview | null>(null);
  const [loading, setLoading] = useState(true);
  const [aiRecap, setAiRecap] = useState<AIRecap | null>(null);
  const [loggerStatus, setLoggerStatus] = useState("unknown");

  async function startLogger() {
    const res = await fetch("http://127.0.0.1:8000/logger/start", {
      method: "POST",
    });
    const data = await res.json();
    setLoggerStatus(data.status);

    await refreshDashboard();
  }

  async function stopLogger() {
    const res = await fetch("http://127.0.0.1:8000/logger/stop", {
      method: "POST",
    });
    const data = await res.json();
    setLoggerStatus(data.status);

    await refreshDashboard();
  }

  async function refreshDashboard() {
    const [dailyData, weeklyData, aiData] = await Promise.all([
      fetch("http://127.0.0.1:8000/daily-summary").then((res) => res.json()),
      fetch("http://127.0.0.1:8000/weekly-review").then((res) => res.json()),
      fetch("http://127.0.0.1:8000/ai-recap").then((res) => res.json()),
    ]);

    setSummary(dailyData);
    setWeekly(weeklyData);
    setAiRecap(aiData);
  }

  useEffect(() => {
    refreshDashboard()
      .then(() => setLoading(false))
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <main className="page">Loading Chronicle...</main>;
  }

  return (
    <main className="page">
      <section className="hero">
        <div>
          <p className="eyebrow">Local AI Workflow Memory</p>
          <h1>Chronicle</h1>
          <p className="subtitle">
            Reconstructing your work sessions, themes, and context from local activity data.
          </p>
        </div>

        <div className="logger-controls">
          <div className="status-pill">API Connected</div>
          <button onClick={startLogger}>Start Logger</button>
          <button onClick={stopLogger}>Stop Logger</button>
          <button onClick={refreshDashboard}>Refresh Dashboard</button>
          <span>Logger: {loggerStatus}</span>
        </div>
      </section>



      <nav className="tabs">
        <button
          className={activeTab === "today" ? "tab active" : "tab"}
          onClick={() => setActiveTab("today")}
        >
          Today
        </button>

        <button
          className={activeTab === "weekly" ? "tab active" : "tab"}
          onClick={() => setActiveTab("weekly")}
        >
          Weekly Review
        </button>

        <button
          className={activeTab === "ai" ? "tab active" : "tab"}
          onClick={() => setActiveTab("ai")}
        >
          AI Recap
        </button>
      </nav>

      {activeTab === "today" && summary && <TodayView summary={summary} />}
      {activeTab === "weekly" && weekly && <WeeklyView weekly={weekly} />}
      {activeTab === "ai" && <AIView aiRecap={aiRecap} />}
    </main>
  );
}

function TodayView({ summary }: { summary: DailySummary }) {
  return (
    <>
      <section className="stats-grid">
        <div className="stat-card">
          <span>Date</span>
          <strong>{summary.date}</strong>
        </div>

        <div className="stat-card">
          <span>Tracked Time</span>
          <strong>{summary.total_tracked_minutes} min</strong>
        </div>

        <div className="stat-card">
          <span>Sessions</span>
          <strong>{summary.total_sessions}</strong>
        </div>
      </section>

      <section className="content-grid">
        <div className="panel">
          <h2>Top Topics</h2>

          <div className="topic-list">
            {summary.top_topics.map((topic) => (
              <div className="topic-row" key={topic.topic}>
                <span>{topic.topic}</span>
                <strong>{topic.minutes} min</strong>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <h2>System Notes</h2>
          <p className="note">
            Chronicle is currently running as a local-first activity intelligence system using
            SQLite, FastAPI, React, and local AI-ready summaries.
          </p>
        </div>
      </section>

      <section className="panel">
        <h2>Major Activity Blocks</h2>

        <div className="activity-stack">
          {summary.major_activity_blocks.map((block, index) => (
            <article className="activity-card" key={index}>
              <div className="activity-header">
                <div>
                  <h3>{block.topic}</h3>
                  <p>
                    {block.start} - {block.end}
                  </p>
                </div>

                <span className="duration">{block.duration_minutes} min</span>
              </div>

              <div className="tag-row">
                <span>{block.category}</span>
              </div>

              <ul className="evidence-list">
                {block.evidence.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}

function WeeklyView({ weekly }: { weekly: WeeklyReview }) {
  return (
    <>
      <section className="stats-grid">
        <div className="stat-card">
          <span>Review Date</span>
          <strong>{weekly.date}</strong>
        </div>

        <div className="stat-card">
          <span>Window</span>
          <strong>{weekly.review_window_days} days</strong>
        </div>

        <div className="stat-card">
          <span>Total Time</span>
          <strong>{weekly.total_summarized_minutes} min</strong>
        </div>
      </section>

      <section className="content-grid">
        <div className="panel">
          <h2>Top Weekly Topics</h2>

          <div className="topic-list">
            {weekly.top_weekly_topics.map((topic) => (
              <div className="topic-row" key={topic.topic}>
                <span>{topic.topic}</span>
                <strong>{topic.minutes} min</strong>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <h2>Recurring Themes</h2>

          <div className="theme-stack">
            {weekly.recurring_themes.length > 0 ? (
              weekly.recurring_themes.map((theme) => (
                <span className="theme-pill" key={theme}>
                  {theme}
                </span>
              ))
            ) : (
              <p className="note">No recurring themes detected yet.</p>
            )}
          </div>
        </div>
      </section>
    </>
  );
}

function AIView({ aiRecap }: { aiRecap: AIRecap | null }) {
  const [question, setQuestion] = useState("");
  const [answers, setAnswers] = useState<AskResponse[]>([]);
  const [asking, setAsking] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function askChronicle() {
    if (!question.trim()) return;

    setAsking(true);
    setError(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }

      const data: AskResponse = await response.json();

      setAnswers((prev) => [data, ...prev]);
      setQuestion("");
    } catch (err) {
      console.error(err);
      setError("Chronicle could not answer that question.");
    } finally {
      setAsking(false);
    }
  }

  return (
    <section className="panel">
      <h2>Ask Chronicle</h2>

      <p className="note">
        Ask questions about your recent activity, weekly patterns, context switching, or project focus.
      </p>

      <div className="ask-box">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Example: What did I focus on most today?"
          rows={3}
        />

        <button onClick={askChronicle} disabled={asking || !question.trim()}>
          {asking ? "Thinking..." : "Ask Chronicle"}
        </button>
      </div>

      {error && <p className="error-text">{error}</p>}

      <div className="suggestion-row">
        {[
          "What did I focus on most today?",
          "What did I focus on this week?",
          "Was I context switching a lot?",
          "What should I revisit tomorrow?",
        ].map((suggestion) => (
          <button
            className="suggestion-chip"
            key={suggestion}
            onClick={() => setQuestion(suggestion)}
          >
            {suggestion}
          </button>
        ))}
      </div>

      <div className="answer-stack">
        {answers.map((item, index) => (
          <article className="answer-card" key={index}>
            <p className="question-label">You asked:</p>
            <h3>{item.question}</h3>

            <p className="question-label">Chronicle answered:</p>
            <pre className="ai-recap-text">{item.answer}</pre>

            <p className="model-label">Model: {item.model}</p>
          </article>
        ))}
      </div>

      {aiRecap && (
        <div className="ai-recap-box">
          <h3>Latest Daily AI Recap</h3>
          <p className="note">Source: {aiRecap.source_file}</p>
          <pre className="ai-recap-text">{aiRecap.recap}</pre>
        </div>
      )}
    </section>
  );
}

export default App;